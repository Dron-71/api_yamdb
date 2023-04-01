from rest_framework import permissions, serializers, viewsets

from django.shortcuts import get_object_or_404

from reviews.models import Review, Title

from .permissions import IsAuthorOrStaff
from .serializers import CommentSerializer, ReviewSerializer


class IsAuthorOrStaffViewSet(viewsets.ModelViewSet):
    """
    Base viewset for reviews and comments.

    Change permission classes based on request method:
    - GET: AllowAny (all users)
    - POST: IsAuthenticated (only users with JWT-token)
    - PATCH, DELETE: IsAuthorOrStaff (only authenticated author or staff
    (moderator, admin, superuser))
    """

    permission_classes = [IsAuthorOrStaff]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (permissions.AllowAny(),)
        if self.action == 'create':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()


class ReviewViewSet(IsAuthorOrStaffViewSet):
    """Viewset for Review model."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.select_related('author').all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        author = self.request.user
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                {
                    'non-field-errors': (
                        'Вы уже оставляли отзыв на это произведение. '
                        'Пожалуйста, используйте PATCH-запрос для '
                        'его изменения.'
                    )
                }
            )
        serializer.save(author=author, title=title)


class CommentViewSet(IsAuthorOrStaffViewSet):
    """Viewset for Comment model."""

    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id'],
        )
        return review.comments.select_related('author').all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id'],
        )
        serializer.save(author=self.request.user, review=review)
