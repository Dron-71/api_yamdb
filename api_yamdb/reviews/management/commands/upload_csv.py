from typing import Any, Dict, Optional

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

from ._utils import upload_csv_file


FILES_ATTRS: Dict[str, Dict[str, Any]] = {
    'category.csv': {
        'model': Category,
        'exclude_fields': ()
    },
    'genre.csv': {
        'model': Genre,
        'exclude_fields': ()
    },
    'users.csv': {
        'model': User,
        'exclude_fields': ('password',)
    },
    'titles.csv': {
        'model': Title,
        'exclude_fields': ()
    },
    'genre_title.csv': {
        'model': Title.genre.through,
        'exclude_fields': ()
    },
    'review.csv': {
        'model': Review,
        'exclude_fields': ()
    },
    'comments.csv': {
        'model': Comment,
        'exclude_fields': ()
    },
}


class Command(BaseCommand):
    """Command to upload_data from csv files."""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        for file_name, attrs in FILES_ATTRS.items():
            try:
                errors, total, valid = upload_csv_file(
                    file_name=file_name,
                    model=attrs['model'],
                    exclude_fields=attrs['exclude_fields'],
                )
                self.stdout.write(
                    f'{file_name} - загружено {valid} из {total} объектов',
                    ending=' ',
                )
                if total == valid:
                    self.stdout.write(self.style.SUCCESS('OK'))
                else:
                    self.stdout.write(self.style.ERROR('FAILED'))
                    for error in errors:
                        self.stderr.write(
                            f'Строка {error["id"]}:',
                            ending=' ',
                        )
                        for key, value in error.items():
                            if key != 'id':
                                self.stderr.write(
                                    f'поле {key} - {value[0]}',
                                    ending=' ',
                                )
                        self.stderr.write()
            except ValueError as e:
                self.stderr.write(
                    f'{file_name} - ошибка при загрузке данных: '
                    f'{e}'
                )
                self.stderr.write(
                    'Если в таблице есть значения из связанных таблиц, '
                    'то добавьте в имя столбца суффикс "_id". Например, '
                    '"title_id".'
                )
