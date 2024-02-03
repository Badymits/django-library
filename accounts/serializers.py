from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'last_name', 'bio', 'profile_pic']
        
    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)

class AccountUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['bio', 'profile_pic']
        
    
    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)
    
    
class AccountRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    # this is only to set the password for the user since the set password in the model.py does not work
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    