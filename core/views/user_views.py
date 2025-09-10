from rest_framework import viewsets
from core.models import UserProfile
from core.serializers import CreatorSerializer
class CreatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.select_related("user").filter(role="CREATOR")
    serializer_class = CreatorSerializer
