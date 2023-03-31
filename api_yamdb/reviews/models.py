from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=150)
    year = models.DateField()
    description = models.TextField(blank=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name


def validate_score(score):
    if score not in range(1, 10):
        raise ValidationError('Score must be between 1 and 10')


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        blank=True,
        validators=[validate_score]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text[:15]
