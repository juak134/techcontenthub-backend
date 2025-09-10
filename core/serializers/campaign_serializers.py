from rest_framework import serializers
from core.models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id","company","name","description","start_date","end_date","budget","state","creators","categories"]

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        profile = getattr(user, "profile", None)
        if self.instance is None:
            if profile and profile.role == "BRAND":
                if attrs.get("state", 1) != 1:
                    raise serializers.ValidationError("Las marcas solo pueden crear campañas en estado borrador.")
        else:
            if "state" in attrs:
                if not (profile and profile.role == "ADMIN"):
                    raise serializers.ValidationError("Solo el admin puede cambiar el estado de la campaña.")
        return attrs

class CampaignDetailSerializer(CampaignSerializer):
    pass
