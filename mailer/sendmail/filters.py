import django_filters

from .models import Email


class EmailFilter(django_filters.FilterSet):
    not_sent = django_filters.BooleanFilter(
        field_name='sent_date',
        lookup_expr='isnull'
    )
    date = django_filters.DateFilter(lookup_expr='date')

    class Meta:
        model = Email
        fields = ['date',]