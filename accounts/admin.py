from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    # this is what we want to display in the admin, 
    # which fields do we want to see as soon as we visit the list
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_staff')

    # this is going to create a search bar in the admin console and 
    # we specify which fields we want to query the database for, so in this case,
    # we want to search by email or firstname
    search_fields = ('email', 'first_name')

    # these are read only fields and cannot be changed
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()

    # it is important to put in fieldsets, if this is not included, then django would throw an error
    fieldsets = ()

# when registering an app to the admin panel, we should put in the model_name and the class admin_name
admin.site.register(Account, AccountAdmin)