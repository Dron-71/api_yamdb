from django.db.migrations import serializer
from django.shortcuts import render, get_list_or_404, get_object_or_404

from rest_framework import permissions, mixins, filters, pagination
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet, GenericViewSet)

from reviews.models import (
    Review, Comment, Category, Genre, Title)
from reviews.permissions import IsAdminOrReadOnly
from api.serializers import (
    ReviewSerializer, CommentSerializer,
    TitleSerializer, CategorySerializer, GenreSerializer)
from api.v1.users.permissions import IsAdmin



class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (
        IsAdminOrReadOnly,
    )


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAdmin,
    )


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (
        IsAdmin,

    )


class ReviewViewSet(ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

