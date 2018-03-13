from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=100)
    desciption= models.TextField()
    cat_pic = models.ImageField(upload_to='bookZone/static/images/categories',blank=True)
    users = models.ManyToManyField(User,related_name="Category_Users",blank=True)
    
    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    bio= models.TextField()
    born_at = models.DateField('Born At')
    died_at = models.DateField('Died At')
    author_pic = models.ImageField(upload_to='bookZone/static/images/authors',blank=True)
    users = models.ManyToManyField(User,related_name="Author_Users",blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    desciption= models.TextField()
    published_at = models.DateField('date published')
    book_pic = models.ImageField(upload_to='bookZone/static/images/books',blank=True)
    users_wishlist = models.ManyToManyField(User,related_name="User_Book_Wishlist",blank=True)
    users_read = models.ManyToManyField(User,related_name="User_Book_read",blank=True)
    categories = models.ManyToManyField(Category)
    author_id = models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class rateBook(models.Model):
    rate = models.IntegerField(default=0)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book,on_delete=models.CASCADE)
