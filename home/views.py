from django.shortcuts import render

from .models import Book
from .serializers import BookSerializer

from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response


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
    
# create class that would get books based on genre
class BookGenreListView(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer(queryset, many=True)  
    
    def get(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        
        # the query set needs to be serialized first so that it can be sent  to the frontend
        serializer_class = BookSerializer(queryset, many=True)  
        
        data={'search_results': serializer_class.data, 'message': 'Successfully filtered'}
        
        return Response(data=data)
        
    # this method is called inside of get, we just need to override it
    def get_queryset(self):
        print('Hello')
        queryset = Book.objects.all()
        genre_filter = self.request.query_params.get('genre')
        
        # verify first if not empty
        if genre_filter is not None:
            return Book.objects.filter(genre__name=genre_filter)
        
        return queryset
    
        
    
    
    