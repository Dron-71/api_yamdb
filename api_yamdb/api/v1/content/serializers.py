from rest_framework import serializers

from django.forms.models import model_to_dict

from reviews.models import Category, Genre, Title


class DictSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return model_to_dict(obj, fields=['name', 'slug'])


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """serializer for Title model."""

    rating = serializers.IntegerField(default=None, read_only=True)
    genre = DictSlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects,
        many=True,
    )
    category = DictSlugRelatedField(
        slug_field='slug',
        queryset=Category.objects,
        many=False,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = ('rating',)
