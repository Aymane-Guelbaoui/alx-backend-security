import datetime
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from ip_tracking.models import RequestLog, BlockedIP
from django.core.cache import cache
import requests


class IPTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        timestamp = datetime.datetime.now()

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Geolocation (cached for 24h)
        country, city = None, None
        cache_key = f"geo:{ip}"
        geo_data = cache.get(cache_key)
        if not geo_data:
            try:
                res = requests.get(f"https://ipinfo.io/{ip}/json")
                data = res.json()
                country = data.get("country")
                city = data.get("city")
                cache.set(cache_key, (country, city), 86400)  # 24h
            except Exception:
                pass
        else:
            country, city = geo_data

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=timestamp,
            country=country,
            city=city
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
