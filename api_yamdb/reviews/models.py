import os

from dotenv import load_dotenv

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import NameSlugModel, PublicationModel

from .validators import validate_year


load_dotenv()


User = get_user_model()


STR_LENGTH: int = int(os.getenv('MODEL_STR_LENGTH', default=15))


class Category(NameSlugModel):
    """Model for a category."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    """Model for a genre."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Model for a title."""

    name = models.CharField(_('Название'), max_length=256, db_index=True)
    year = models.IntegerField(
        _('Год выпуска'),
        validators=[validate_year],
        db_index=True,
    )
    description = models.TextField(_('Описание'), blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ['pk']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_LENGTH]


class Review(PublicationModel):
    """Model for a review."""

    title = models.ForeignKey(
        Title,
        verbose_name=_('Произведение'),
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        _('Оценка'),
        validators=[
            MinValueValidator(1, _('Оценка не может быть меньше 1')),
            MaxValueValidator(10, _('Оценка не должна превышать 10')),
        ]
    )

    class Meta(PublicationModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='author_title_unique',
            ),
        ]


class Comment(PublicationModel):
    """Model for a comment."""

    review = models.ForeignKey(
        Review,
        verbose_name=_('Отзыв'),
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta(PublicationModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
