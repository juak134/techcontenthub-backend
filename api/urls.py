from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from core.views.company_views import CompanyViewSet, CompanyConfigViewSet, EmailConfigViewSet
from core.views.category_views import CategoryViewSet
from core.views.campaign_views import CampaignViewSet
from core.views.content_views import ContentViewSet
from core.views.metrics_views import ContentMetricsView
from core.views.user_views import CreatorViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"company-configs", CompanyConfigViewSet, basename="company-config")
router.register(r"email-configs", EmailConfigViewSet, basename="email-config")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"campaigns", CampaignViewSet, basename="campaign")
router.register(r"content", ContentViewSet, basename="content")
router.register(r"creators", CreatorViewSet, basename="creator")

urlpatterns = [
    path("", include(router.urls)),
    re_path(r"^metrics/content/(?P<content_id>\d+)/$", ContentMetricsView.as_view(), name="content-metrics"),
]
