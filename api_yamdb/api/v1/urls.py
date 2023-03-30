from django.urls import include, path


app_name = 'api_v1'

urlpatterns = [
    path('auth/', include('api.v1.users.urls', namespace='api_users_v1')),
]
