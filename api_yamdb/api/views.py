from django.shortcuts import render, get_list_or_404, get_object_or_404

from rest_framework import permissions, mixins, filters, pagination
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet, GenericViewSet)

from reviews.models import (
    Review, Comment, Category, Genre, User, Title)
from api.serializers import (
    ReviewSerializer, CommentSerializer)


class ReviewViewSet(ReadOnlyModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = (pagination.LimitOffsetPagination,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = (pagination.LimitOffsetPagination,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        review = get_list_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
        pass
