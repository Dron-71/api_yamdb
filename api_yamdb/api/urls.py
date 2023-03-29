
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from api_yamdb.api.views import (
    ReviewViewSet, CommentViewSet)

router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/',
    ReviewViewSet,
    basename='reviews-detail'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    ReviewViewSet,
    basename='comments'
)


urlpatterns = [
    path(r'v1/', include(router.urls)),
    path(r'v1/', include('djoser.urls')),  # Работа с пользователями
]

urlpatterns += [
    path(r'v1/jwt/create/',
         views.TokenObtainPairView.as_view(), name="jwt-create"),
    path(r'v1/jwt/refresh/',
         views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path(r'v1/jwt/verify/',
         views.TokenVerifyView.as_view(), name="jwt-verify"),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
