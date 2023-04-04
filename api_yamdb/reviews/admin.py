from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class NameSlugAdmin(admin.ModelAdmin):
    """Admin config for abstract NameSlugModel."""

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('slug',)


@admin.register(Category)
class CategoryAdmin(NameSlugAdmin):
    """Admin config for Category model."""


@admin.register(Genre)
class GenreAdmin(NameSlugAdmin):
    """Admin config for Genre model."""


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Admin config for Title model."""

    list_display = ('name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('category', 'genre')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin config for Review model."""

    list_display = ('author', 'title', 'score')
    search_fields = ('author',)
    list_filter = ('author', 'title', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin config for Comment model."""

    list_display = ('author', 'review')
    search_fields = ('author',)
    list_filter = ('author', 'review', 'pub_date')
