from rest_framework import viewsets
from core.cache.mixins import ListCacheMixin
from core.models import Content
from core.serializers import ContentSerializer, ContentDetailSerializer
from core.tenancy.mixins import SiteFilteredQuerysetMixin
class ContentViewSet(ListCacheMixin, SiteFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = Content.objects.select_related("campaign","creator").all()
    serializer_class = ContentSerializer
    site_field_path = "campaign__company__site"
    filterset_fields = ["campaign", "creator", "type", "is_approved", "categories"]
    ordering_fields = ["created_at", "updated_at", "id"]
    ordering = ["-created_at"]
    def get_serializer_class(self):
        return ContentDetailSerializer if self.action in ["retrieve"] else super().get_serializer_class()
