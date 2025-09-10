from rest_framework import viewsets, status
from core.cache.mixins import ListCacheMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from core.models import Campaign, UserProfile
from core.serializers import CampaignSerializer, CampaignDetailSerializer
from core.tenancy.mixins import SiteFilteredQuerysetMixin

class CampaignViewSet(ListCacheMixin, SiteFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = Campaign.objects.select_related("company").prefetch_related("creators","categories").all()
    serializer_class = CampaignSerializer
    site_field_path = "company__site"
    filterset_fields = ["company", "state", "categories", "creators"]
    ordering_fields = ["start_date", "end_date", "budget", "id"]
    ordering = ["-id"]

    def get_serializer_class(self):
        return CampaignDetailSerializer if self.action in ["retrieve"] else super().get_serializer_class()

    @action(detail=True, methods=["post"], url_path="add-creators")
    def add_creators(self, request, pk=None):
        campaign = self.get_object()
        if campaign.state != 2:
            return Response({"detail": "Solo campañas ACTIVAS pueden agregar creadores."}, status=400)
        if not hasattr(request.user, "profile") or request.user.profile.role != "ADMIN":
            return Response({"detail": "Solo ADMIN puede modificar creadores en campañas."}, status=403)

        creator_ids = request.data.get("creator_ids", [])
        creators = UserProfile.objects.filter(id__in=creator_ids, role="CREATOR")
        with transaction.atomic():
            campaign.creators.add(*creators)
        return Response({"added": [c.id for c in creators]})
