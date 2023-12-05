from rest_framework import serializers
from .models import *


 # just in case Serialization = The process whereby an object or data structure 
 # is translated into a format suitable for transfer over a network, or storage (e.g. in an array buffer or file format)
class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'

