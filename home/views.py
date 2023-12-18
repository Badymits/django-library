from django.shortcuts import render

from .models import Book
from .serializers import BookSerializer

from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q


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
        #print('request: ',request)
        return self.retrieve(request, *args, **kwargs)
    
# create class that would get books based on genre
class BookSearchListView(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    
    def get(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()

        # the query set needs to be serialized first so that it can be sent  to the frontend
        serializer_class = BookSerializer(queryset, many=True, context={'request': request}) # include request for the method in serializer  
        #print(serializer_class.data)
        data={'search_results': serializer_class.data, 'message': 'Successfully filtered'}
        
        return Response(data=data)
        
    # this method is called inside of get, we just need to override it
    def get_queryset(self):
        
        # retrieve url parameter
        query_param = self.request.query_params.get('key')
        
        # use the url paramter to filter books based on url param
        qs_filtered = Book.objects.filter(
            Q(title__icontains=query_param) |
            Q(author__name__icontains=query_param) |
            Q(genre__name__icontains=query_param)
        )
    
        
        return qs_filtered
    
        
    
    
    