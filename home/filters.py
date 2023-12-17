from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Book

# this has been very tiring for me only...
# wont delete for future reference
class BookSearchFilter(filters.FilterSet):

    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    author = filters.CharFilter(field_name="author__name", method="custom_filter")
    genre = filters.CharFilter(field_name="genre__name", method="custom_filter")
    
    class Meta:
        model = Book
        fields = ['title', 'author__name', 'genre__name']
        
    def custom_filter(self, queryset, name, value):
        
        return queryset.filter(
            Q(author__name__icontains=value) |
            Q(genre__name__icontains=value)
        )


