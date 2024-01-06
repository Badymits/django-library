from django.db import models
from django.conf import settings

custom_user = settings.AUTH_USER_MODEL


# Create your models here.
    
class Book(models.Model):
    
    STATUS = (
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable')
    )
    
    title               = models.CharField(max_length=255)
    author              = models.ForeignKey('home.Author',  on_delete=models.CASCADE, blank=True, null=True)
    genre               = models.ManyToManyField('home.Genre')
    summary             = models.CharField(max_length=599, null=True, blank=True)
    status              = models.CharField(choices=STATUS, max_length=255)
    book_image          = models.ImageField(upload_to='images', blank=True, null=True)
    rent_price          = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, blank=True, null=True)
    purchase_price      = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, blank=True, null=True) 
    
    def __str__(self):
        return self.title
    
class Author(models.Model):
    
    name                = models.CharField(max_length=255)
    books               = models.ManyToManyField(Book, related_name='+', blank=True)
    
    def __str__(self):
        return str(self.name)
    
class Genre(models.Model):
    
    # A tag to categorize (such as sports, kitchen, cleaning, etc..) the orders
    name                = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.name)
    

# this represents books that have been borrowed/rented by users 
class CheckedOutBooks(models.Model):
    
    STATUS = (
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
        ('Late', 'Late'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered')
    )
    
    book                = models.ForeignKey(Book, on_delete=models.CASCADE)
    user                = models.ForeignKey(custom_user, on_delete=models.CASCADE)
    borrowed_date       = models.DateTimeField(auto_now_add=True)
    
    # this is to keep track of whether the user has been returning it on time or is late
    returned_date       = models.DateTimeField()
    due_date            = models.DateTimeField()
    
    status              = models.CharField(choices=STATUS, max_length=255)
    
    def __str__(self):
        
        return f'{self.book} due date: {self.due_date}'
    

#class BooksInCart(models.Model):

    # customer            = models.ForeignKey(custom_user, on_delete=models.CASCADE)
    # book_in_cart        = models.ForeignKey(Book, on_delete=models.CASCADE)
    

# class CartOrder(models.Model):
    
#     user                 = models.ForeignKey(custom_user, on_delete=models.CASCADE)
#     books                = models.ManyToMany(BooksInCart, on_delete=models.CASCADE)
#     total                = models.CharField()    
