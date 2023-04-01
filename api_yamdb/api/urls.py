
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.routers import DefaultRouter



urlpatterns = [
    # path('v1/', include(router.urls)),
    path('v1/', include('api.v1.urls', namespace='api_v1')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

