"""Utils functions for management commands."""

import csv
from pathlib import Path
from typing import Any, Dict, List, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Model


STATIC_FILES_DIR = settings.STATICFILES_DIRS[0]
DATA_PATH = Path(STATIC_FILES_DIR, 'data')


def upload_csv_file(
        file_name: str,
        model: Model,
        exclude_fields: Tuple[str]
) -> Dict[str, List[str]]:
    """Read data, validate it and upload it to DB through Django ORM."""
    file_path = Path(DATA_PATH, file_name)
    with open(file_path, encoding='utf-8') as file_obj:
        reader = csv.DictReader(file_obj)
        total_count, valid_count = 0, 0
        model_objs: List[Any] = []
        errors: List[Dict[Any]] = []
        for row in reader:
            total_count += 1
            obj = model(**row)
            try:
                obj.full_clean(exclude=exclude_fields)
                model_objs.append(obj)
                valid_count += 1
            except ValidationError as e:
                errors_dict = e.message_dict
                errors_dict['id'] = row['id']
                errors.append(errors_dict)
        model.objects.bulk_create(model_objs)
        return errors, total_count, valid_count
