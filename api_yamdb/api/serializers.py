import json
from unicodedata import category

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.forms import model_to_dict

from django.shortcuts import get_list_or_404
from rest_framework import serializers

from reviews.models import (
    Review, Title, Genre, Comment, Category)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')

class TitleSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    # genre = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Genre.objects.all(),
    #     many=True
    # )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'rating', 'year', 'genre', 'category', 'description'
        )
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return rating if rating else None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
    score = serializers.IntegerField(
        validators=[MinValueValidator(limit_value=1),
                    MaxValueValidator(limit_value=10)]
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'author', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'author', 'pub_date', 'title', 'review')
