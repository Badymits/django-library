from django.shortcuts import render

from .models import Book
from .serializers import BookSerializer

from rest_framework import mixins
from rest_framework import generics


# Create your views here.
class BookListView(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        print(request)
        return self.retrieve(request, *args, **kwargs)