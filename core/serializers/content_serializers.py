from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.models import Content

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id","campaign","creator","title","description","url","type","is_approved","categories","created_at","updated_at"]
        read_only_fields = ["created_at","updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        profile = getattr(user, "profile", None)
        campaign = attrs.get("campaign") if self.instance is None else self.instance.campaign
        creator = attrs.get("creator") if self.instance is None else self.instance.creator

        if campaign.state != 2:
            raise ValidationError("Solo campañas ACTIVAS pueden recibir contenido.")

        if profile and profile.role == "CREATOR":
            if creator != profile:
                raise ValidationError("Un creador solo puede subir su propio contenido.")
            if not campaign.creators.filter(id=profile.id).exists():
                raise ValidationError("El creador no está agregado a esta campaña.")

        if profile and profile.role == "ADMIN":
            if not campaign.creators.filter(id=creator.id).exists():
                raise ValidationError("El creador no está agregado a esta campaña.")

        if profile and profile.role == "BRAND" and self.instance is None:
            raise ValidationError("Las marcas no pueden subir contenido.")

        return attrs

class ContentDetailSerializer(ContentSerializer):
    pass
