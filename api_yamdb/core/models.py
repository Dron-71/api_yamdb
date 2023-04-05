import os

from dotenv import load_dotenv

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


load_dotenv()


STR_LENGTH: int = int(os.getenv('MODEL_STR_LENGTH', default=15))


User = get_user_model()


class NameSlugModel(models.Model):
    """Abstract model for tables with name and slug fields."""

    name = models.CharField(_('Название'), max_length=256, db_index=True)
    slug = models.SlugField(_('Слаг'), max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ['slug']

    def __str__(self):
        return self.slug[:STR_LENGTH]


class PublicationModel(models.Model):
    """Abstract model for publications (e.g. reviews, comments)."""

    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(
        _('Дата публикации'),
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date', 'author']

    def __str__(self):
        return self.text[:STR_LENGTH]
