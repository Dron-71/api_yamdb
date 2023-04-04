from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (ReviewViewSet, CommentViewSet,
                       TitleViewSet, CategoryViewSet, GenreViewSet)

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('api.v1.users.urls', namespace='api_users_v1')),
]
