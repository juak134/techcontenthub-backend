from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (("CREATOR","Creator"),("BRAND","Brand"),("ADMIN","Admin"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="CREATOR")
    phone = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True)
    companies = models.ManyToManyField("Company", related_name="users", blank=True)
    def __str__(self): return f"{self.user.username} ({self.role})"
