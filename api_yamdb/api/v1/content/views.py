from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from api.v1.users.permissions import IsAdmin
from api.v1.users.views import HTTP_METHOD_NAMES
from reviews.models import Category, Genre, Title

from .filters import TitleFilterset
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset to preform list, create, destroy methods.

    All users (both anonymyos and authenticated) can read data, only admin
    can add and delete data.
    """

    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return super().get_permissions()


class CategoryViewSet(ListCreateDeleteViewSet):
    """Viewset for Category model."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """Viewset for Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset for Title model."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterset
    permission_classes = [IsAdmin]
    http_method_names = HTTP_METHOD_NAMES

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()
