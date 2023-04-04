from rest_framework import serializers

from reviews.models import Comment, Review


class AuthorCurrentUserSeralizer(serializers.ModelSerializer):
    """
    Base serializer for reviews and comments.

    Author is SlugRelatedField for read only with current user as default
    value.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )


class ReviewSerializer(AuthorCurrentUserSeralizer):
    """Serializer for Review model."""

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(AuthorCurrentUserSeralizer):
    """Serializer for Comment model."""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
