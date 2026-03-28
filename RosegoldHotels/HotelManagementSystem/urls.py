"""HotelManagementSystem URL Configuration."""

import re
from urllib.parse import urlsplit

from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve


def media_urlpatterns():
    """Serve local media files even when DEBUG is disabled."""
    media_url = getattr(settings, "MEDIA_URL", "")
    if not media_url:
        return []

    parsed_media_url = urlsplit(media_url)
    if parsed_media_url.scheme or parsed_media_url.netloc:
        return []

    media_prefix = media_url.lstrip("/")
    if not media_prefix:
        return []
    if not media_prefix.endswith("/"):
        media_prefix = f"{media_prefix}/"

    return [
        re_path(
            rf"^{re.escape(media_prefix)}(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        )
    ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('HotelApp.urls')),
    path('', include('alerts.urls')),
]

urlpatterns += media_urlpatterns()
