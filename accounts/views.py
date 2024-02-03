from django.shortcuts import render

from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import AccountRegisterSerializer, AccountSerializer, AccountUpdateSerializer
from .models import Account

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token


# this will include user related information inside the token.
# so when the token is decoded, we are able to access the user's identifications
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST', ])
def register(request):
    context = {} 
    if request.method == 'POST':
        serializer = AccountRegisterSerializer(data=request.data)
        print(request.data)

        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            
            user_token = get_tokens_for_user(serializer.instance)
            token = Token.objects.get(user=serializer.instance)
          
        else:
            print('Error')
            emsg = serializer.error_messages
            context['error'] = emsg
            
        context['success'] = True
        context['message'] = 'User has been registered'
        context['user_token'] = user_token
        context['token'] = token.key
        return Response(context)

# will generate for newly registered users
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST', ])
def login(request):
    
    if request.method == 'POST':
        pass
    pass

@api_view(['GET',])
def userList(request):
    
    users = Account.objects.all()
    
    # when retrieving a list, set the many param to True, when only getting one instance, set it to false
    serializer = AccountSerializer(users, many=True)
    
    return Response(serializer.data)
    
class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'username'
    def get(self, request, *args, **kwargs):
        #print('request: ',request)
        return self.retrieve(request, *args, **kwargs)
        
        
class EditAccountView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    
    parser_classes = (FormParser, MultiPartParser)
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer
    
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'head', 'patch']
    
    def get_object(self, username):
        
        obj = Account.objects.get(username=username)
        return obj
    
    
    def get(self, request, *args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)
    
    # need to override this damn function to save the damn img for an existing user model for fucks sake
    def partial_update(self, request, *args, **kwargs):
        user = self.get_object(request.GET.get('username'))
        img = request.FILES['image']
        user.profile_pic = img
        user.save()
        
        serializer = AccountUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400, data="Error msg")
         
    
    def patch(self, request, *args, **kwargs):
        
        return self.partial_update(request, *args, **kwargs)
        
    
    
    