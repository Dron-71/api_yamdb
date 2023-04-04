from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import SignUpView, TokenGenerationView, UserViewSet


app_name = 'api_users_v1'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenGenerationView.as_view(), name='get_token'),
]
