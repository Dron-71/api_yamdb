from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, mixins, filters
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet, GenericViewSet)

from api_yamdb.reviews.models import (
    Review, Comment, Category, Genre, User, Title)
from .serializers import (
    ReviewSerializer, CommentSerializer)


class ReviewViewSet(ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer