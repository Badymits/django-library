from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

# when a new user is created, create token for them
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance=None, created=False, **kwargs):
    
    if created:
        Token.objects.create(user=instance)
        
    
class MyAccountManager(BaseUserManager):
    
    # for create_user, the parameters depend on the Required fields that we declared in the Account model
    # in this case, we pass in email since that is what they need to login, and username since it is
    # required for registering a new account
    def create_user(self, email, username, first_name, last_name, password=None):
        # raise an error if the user did not provide any email, similar function with the username
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError('')
        
        
        # if they have provided a valid username and email, then we can create the user
        # by utilizing the model method and pass the respective parameters
        user = self.model(
            # normalize email isn't available anywhere, it can only be used inside the BaseUsermanager class
            # normalize email converts all of the characters in the email to lower case
            email=self.normalize_email(email), 
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self.db)  # the parameter means we specify which database the manager should operate on
        return user
        
    def create_superuser(self, email,first_name, last_name, username, password):
        # instead of using the model method, we can just refer to the create_user method above
        user = self.create_user(
            email=self.normalize_email(email), 
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        # since by default, we set these fields to False, and we are creating a new superuser
        # we want to give them access 
        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True

        user.save(using=self.db)
        return user

# main model to be used for accounts
# Django implements group relation in PermissionsMixin so you don't have that particular relation
# without mixins inheritance, there will be an error saying 'Group' object has no attribute 'user_set'
class Account(AbstractBaseUser, PermissionsMixin):
    
    email                   = models.EmailField(verbose_name='email', max_length=60,unique=True)
    first_name              = models.CharField(max_length=50, null=True, blank=True)
    last_name               = models.CharField(max_length=50, null=True, blank=True)
    username                = models.CharField(max_length=30)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True) # auto now add refers to the first time that this field was updated
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True) # unlike the auto now add, this refers to each and every time this field was updated, not only the first time
    profile_pic             = models.ImageField(upload_to='images', blank=True, null=True)
    bio                     = models.CharField(max_length=255, null=True, blank=True)
    
    # all these fields are required if using a custom user model
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

    
    # in a customer user model, we can set the field to whatever the user needs to input for them to login
    # in this case, we want the user to login with their email, not username
    USERNAME_FIELD = "email"

    # these are the fields that the user needs to provide whenever they register for an account
    # same goes when creating super user, putting fields in here will be a prompt when creating superuser
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # we tell this Account model where the manager is located in the app or how would the account model use the manager
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    # THE FOLLOWING FUNCTIONS ARE REQUIRED WHEN USING CUSTOM USER MODEL

    # Returns True if the user has each of the specified permissions, 
    # where each perm is in the format "<app label>.<permission codename>". 
    # If the user is inactive, this method will always return False. For an active superuser, 
    # this method will always return True.

    # If obj is passed in, this method won’t check for permissions for the model, 
    # but for the specific object.
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    # checks if the user has permission to use/see the module, in this case, no matter what, it will return True
    # If the user is inactive, this method will always return False. For an active superuser, this method will always return True.
    def has_module_perms(self, app_label):
        return True