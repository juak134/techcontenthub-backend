from rest_framework.permissions import BasePermission
class IsAdmin(BasePermission):
    def has_permission(self, request, view): return hasattr(request.user, "profile") and request.user.profile.role == "ADMIN"
class IsBrand(BasePermission):
    def has_permission(self, request, view): return hasattr(request.user, "profile") and request.user.profile.role == "BRAND"
class IsCreator(BasePermission):
    def has_permission(self, request, view): return hasattr(request.user, "profile") and request.user.profile.role == "CREATOR"
