from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('api.v1.urls', namespace='api_v1')),
]
