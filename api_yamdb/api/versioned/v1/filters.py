from django_filters import rest_framework as filters
from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class GenreFilterSet(filters.FilterSet):
    genre = CharFilterInFilter(
        field_name='genre__slug',
        lookup_expr='in'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = [
            'genre',
            'category',
            'year',
            'name'
        ]
