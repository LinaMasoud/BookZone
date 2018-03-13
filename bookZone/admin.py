from django.contrib import admin
from .models import Book,Author,Category,rateBook

# Register your models here.

admin.site.register(Book)
admin.site.register(rateBook)
admin.site.register(Author)
admin.site.register(Category)