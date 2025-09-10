from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from core.models import Content
from integrations.elasticsearch.client import get_es, get_index_name
from integrations.elasticsearch.indexes import metrics_doc

class ContentMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def _check_permission(self, request, content):
        role = getattr(getattr(request.user, "profile", None), "role", None)
        if role in ("ADMIN", "CREATOR"):
            if role == "CREATOR" and content.creator_id != request.user.profile.id:
                return False, Response({"detail": "Solo puedes subir métricas para tu propio contenido."}, status=403)
            return True, None
        return False, Response({"detail": "Solo admin y creador pueden subir métricas."}, status=403)

    def get(self, request, content_id: int):
        es = get_es()
        index = get_index_name()
        q = {"query": {"term": {"content_id.keyword": str(content_id)}}}
        res = es.search(index=index, body=q)
        hits = [h.get("_source") for h in res.get("hits", {}).get("hits", [])]
        if not hits:
            return Response({"detail": "No hay métricas para este contenido."}, status=404)
        return Response(hits[0])

    def post(self, request, content_id: int):
        content = get_object_or_404(Content, pk=content_id)
        ok, resp = self._check_permission(request, content)
        if not ok: return resp

        es = get_es(); index = get_index_name()
        data = request.data or {}; metrics = data.get("metrics", {})
        content_info = data.get("content_info", {"title":content.title, "type":content.type, "url":content.url})
        now = timezone.now().isoformat(); site = get_current_site(request)

        doc = metrics_doc(
            content_id=content.id,
            campaign_id=content.campaign_id,
            creator_id=content.creator_id,
            company_id=content.campaign.company_id,
            site_id=site.id,
            metrics={k:int(metrics.get(k,0)) for k in ["views","likes","shares","comments"]},
            content_info=content_info,
            timestamp=now,
            updated_at=now,
        )
        es.index(index=index, id=str(content.id), body=doc, refresh=True)
        return Response(doc, status=201)

    def put(self, request, content_id: int):
        content = get_object_or_404(Content, pk=content_id)
        ok, resp = self._check_permission(request, content)
        if not ok: return resp

        es = get_es(); index = get_index_name()
        try:
            existing = es.get(index=index, id=str(content.id))["_source"]
        except Exception:
            return Response({"detail": "No existe documento de métricas para actualizar. Usa POST primero."}, status=404)

        metrics = request.data.get("metrics", {})
        for k in ["views","likes","shares","comments"]:
            existing["metrics"][k] = int(metrics.get(k, existing["metrics"].get(k, 0)))
        existing["updated_at"] = timezone.now().isoformat()
        es.index(index=index, id=str(content.id), body=existing, refresh=True)
        return Response(existing)
