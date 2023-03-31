from rest_framework import serializers
from reviews.models import Category, Genre, Title
from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории (типы)."""
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = datetime.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value
