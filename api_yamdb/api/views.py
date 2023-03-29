from django.shortcuts import render


from rest_framework import permissions, mixins, filters
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet, GenericViewSet)

from api_yamdb.reviews.models import (
    Review, Comment, Category, Genre, User, Title)
from api_yamdb.api.serializers import (
    ReviewSerializer, CommentSerializer)


class ReviewViewSet(ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

