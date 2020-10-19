from library.models import Book
import django_filters
from django import forms

class BookFilter(django_filters.FilterSet):

    start_date = django_filters.DateFilter(field_name='date_of_public',lookup_expr='gt', widget=forms.SelectDateWidget(years=range(1700,2025)), label='Publication date since')
    end_date = django_filters.DateFilter(field_name='date_of_public', lookup_expr='lt', widget=forms.SelectDateWidget(years=range(1700,2025)), label='Publication date till')
    title = django_filters.CharFilter(lookup_expr='icontains',)
    lang = django_filters.CharFilter(label='Language')
    date_of_public = django_filters.DateFromToRangeFilter(label='Publication date range')
    class Meta:
        model = Book

        fields = ['title', 'date_of_public', 'start_date', 'end_date', 'author', 'lang']
        widgets = {
            'date_of_public': django_filters.DateTimeFromToRangeFilter(),
        }
