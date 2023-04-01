import os
from datetime import datetime as dt

from dotenv import load_dotenv

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import NameSlugModel


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

    name = models.CharField(_('Название'), max_length=256)
    year = models.IntegerField(
        _('Год выпуска'),
        validators=[MaxValueValidator(dt.now().year)]
    )
    description = models.TextField(_('Описание'), blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_LENGTH]


class GenreTitle(models.Model):
    """Tile-Genre connection table."""

    title = models.ForeignKey(
        Title,
        verbose_name=_('Произведение'),
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name=_('Жанр'),
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Произведение-Жанр'
        verbose_name_plural = 'Произведения-Жанры'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='title_genre_unique',
            ),
        ]

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """Model for a review."""

    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(_('Дата публикации'), auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        verbose_name=_('Произведение'),
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        _('Оценка'),
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['author']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:STR_LENGTH]


class Comment(models.Model):
    """Model for a comment."""

    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(_('Дата публикации'), auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        related_name='comments',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        verbose_name=_('Отзыв'),
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['author']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:STR_LENGTH]
