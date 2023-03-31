
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from api.views import (
    ReviewViewSet, CommentViewSet)

app_name = 'api'
router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    ReviewViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('api.v1.urls', namespace='api_v1')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

