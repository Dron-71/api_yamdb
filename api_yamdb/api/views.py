from django.shortcuts import render, get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, mixins, filters, pagination
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet, GenericViewSet)

from reviews.models import (
    Review, Comment, Category, Genre, Title)
from reviews.permissions import IsAllowedOrReadOnly, IsAdminOrReadOnly
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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('slug', 'name')


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('slug',)
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAllowedOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.select_related('author').all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise ValidationError(
                f'У вас уже оставили  отзыв на {title}'
            )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAllowedOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.prefetch_related('author').all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
