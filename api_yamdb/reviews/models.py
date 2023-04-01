from django.db import models


class Category(models.Model):
    """Модель категории (типы)."""
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        verbose_name='Наименование жанра',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        verbose_name='Название произвидения',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска произвидения',
    )
    description = models.TextField(
        verbose_name='Описание произвидения',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произвидения',
        blank=True,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория (типы) произвидения',
        blank=True,
        null=True,
        related_name='categories',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель"""
    title = models.ForeignKey(
        Title,
        verbose_name='Название произвидения',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр произвидения',
        on_delete=models.CASCADE
    )
