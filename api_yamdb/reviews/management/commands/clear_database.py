from typing import Any, Optional

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    """Delete all database entries."""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        Category.objects.all().delete()
        Comment.objects.all().delete()
        Genre.objects.all().delete()
        Review.objects.all().delete()
        Title.objects.all().delete()
        Title.genre.through.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все данные успешно удалены.'))
