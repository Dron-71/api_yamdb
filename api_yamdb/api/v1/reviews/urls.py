from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CommentViewSet, ReviewViewSet


app_name = 'api_reviews_v1'


router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/((?P<review_id>\d+))/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router.urls)),
]
