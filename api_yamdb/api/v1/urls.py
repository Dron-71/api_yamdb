from django.urls import include, path


app_name = 'api_v1'

urlpatterns = [
    path('', include('api.v1.users.urls', namespace='api_users_v1')),
    path('', include('api.v1.content.urls', namespace='api_content_v1')),
    path('', include('api.v1.reviews.urls', namespace='api_reviews_v1')),
]
