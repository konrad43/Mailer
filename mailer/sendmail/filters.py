import django_filters

from .models import Email


class EmailFilter(django_filters.FilterSet):
    sent_date = django_filters.BooleanFilter(
        lookup_expr='isnull',
        exclude=True
    )
    date = django_filters.DateFilter(lookup_expr='date')

    class Meta:
        model = Email
        fields = ['date',]