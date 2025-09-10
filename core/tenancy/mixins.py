from django.contrib.sites.shortcuts import get_current_site
class SiteFilteredQuerysetMixin:
    site_field_path = None
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.site_field_path: return qs
        site = get_current_site(self.request)
        return qs.filter(**{self.site_field_path: site})
