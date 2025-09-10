from django.db import models
from django.contrib.sites.models import Site

class Company(models.Model):
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="companies")
    def __str__(self): return self.name
