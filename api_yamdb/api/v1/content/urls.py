from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


app_name = 'api_content_v1'


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls)),
]
