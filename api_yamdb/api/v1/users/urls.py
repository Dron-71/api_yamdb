from django.urls import path

from .views import SignUpView, TokenGenerationView


app_name = 'api_users_v1'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', TokenGenerationView.as_view(), name='get_token'),
]
