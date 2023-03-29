from django.contrib.auth import get_user_model
from rest_framework import serializers
from api_yamdb.reviews.models import (
    Review, Title, Genre, Comment, Category)

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
