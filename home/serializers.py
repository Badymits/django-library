from rest_framework import serializers
from .models import *


 # just in case Serialization = The process whereby an object or data structure 
 # is translated into a format suitable for transfer over a network, or storage (e.g. in an array buffer or file format)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    
    # this fixes the problem where it only shows the foreignkey ID, not the returned name string
    author          = AuthorSerializer(read_only=True)
    genre           = GenreSerializer(read_only=True, many=True)
    
    class Meta:
        model = Book
        fields = '__all__'

