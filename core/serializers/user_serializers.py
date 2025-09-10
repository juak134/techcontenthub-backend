from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ["id", "user", "role", "phone", "bio", "avatar_url", "social_links", "companies"]

class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ["id", "user", "role", "bio", "avatar_url"]
