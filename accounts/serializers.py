from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'last_name']

# class AccountLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
        
#         email = serializers.CharField(max_length=255)
#         password = serializers.CharField(
#             label=("Password"),
#             style={'input_type': 'password'},
#             trim_whitespace=False,
#             max_length=128,
#             read_only=True
        
#         )
        
#     def validate(self, data):
#         user_email = data.get('email')
#         user_password = data.get('password')
        
#         # validation goes thru if user has provided/entered their credentials
#         if user_email and user_password:
#             user = authenticate(email=user_email, password=user_password)
            
#             # display error
#             if not user:
#                 msg = ('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
        
#         else:
#             msg = ('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')
        
#         # return authenticated user
#         data['user'] = user
#         return data

class AccountRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    