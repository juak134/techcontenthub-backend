from rest_framework import serializers
from core.models import Company, CompanyConfig, EmailConfig

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id","name","legal_name","email","phone","website","address","is_active","site"]

class CompanyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyConfig
        fields = "__all__"

class EmailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfig
        fields = "__all__"
