import os

from dotenv import load_dotenv

from django.db import models
from django.utils.translation import gettext_lazy as _


load_dotenv()


STR_LENGTH: int = int(os.getenv('MODEL_STR_LENGTH', default=15))


class NameSlugModel(models.Model):
    """Abstract model for tables with name and slug fields."""

    name = models.CharField(_('Название'), max_length=256)
    slug = models.SlugField(_('Слаг'), max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ['slug']

    def __str__(self):
        return self.slug[:STR_LENGTH]
