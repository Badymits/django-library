from django.contrib import admin

from .models import *

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'genre__name', 'author__name',)
    
class AuthorAdmin(admin.ModelAdmin):
    
    search_fields = ('books__title',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(CheckedOutBooks)

