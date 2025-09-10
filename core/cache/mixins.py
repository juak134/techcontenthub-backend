from django.core.cache import cache
from django.utils.encoding import force_str

class ListCacheMixin:
    cache_timeout = 60  # seconds
    def _cache_key(self):
        request = self.request
        user_part = f"user={getattr(request.user, 'id', 'anon')}"
        query_part = force_str(request.get_full_path())
        return f"listcache:{self.__class__.__name__}:{user_part}:{query_part}"
    def list(self, request, *args, **kwargs):
        key = self._cache_key()
        cached = cache.get(key)
        if cached is not None:
            return cached
        response = super().list(request, *args, **kwargs)
        try:
            cache.set(key, response, timeout=self.cache_timeout)
        except Exception:
            pass
        return response
