from rest_framework import viewsets
from core.models import Company, CompanyConfig, EmailConfig
from core.serializers import CompanySerializer, CompanyConfigSerializer, EmailConfigSerializer
from core.tenancy.mixins import SiteFilteredQuerysetMixin

class CompanyViewSet(SiteFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    site_field_path = "site"

class CompanyConfigViewSet(SiteFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = CompanyConfig.objects.all()
    serializer_class = CompanyConfigSerializer
    site_field_path = "company__site"

class EmailConfigViewSet(SiteFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = EmailConfig.objects.all()
    serializer_class = EmailConfigSerializer
    site_field_path = "company__site"
