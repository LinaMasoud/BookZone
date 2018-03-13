from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
#from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Book,Author,Category,rateBook
from django.db.models import Q,Avg,Count
from bookZone.forms import SignUpForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

def checkAll(request):
    if request.user.is_authenticated:
        categs = Category.objects.filter(users=request.user)
        auths = Author.objects.filter(users=request.user)
        books1 = Book.objects.filter(users_read=request.user)
        books2 = Book.objects.filter(users_wishlist=request.user)
        userName = request.user.username
        context = {'uCategs':categs,'uAuths':auths,'uRBooks':books1,'uWBooks':books2,'userName':userName}
        return context
    else:    
        return False

# Builds Welcome page
def welcome(request):
    context = checkAll(request)
    if context:
        return redirect('bookZone/')
    else:
        return render(request,'bookZone/welcome.html')

# Builds index page
def index(request):
    context = checkAll(request)
    if context:
        topRated = rateBook.objects.values('book_id').annotate(avgRate=Avg('rate')).order_by('-avgRate')[:5]
        books = []
        for topR in topRated:
            book = {}
            book['id'] = topR['book_id']
            book['title'] = Book.objects.get(pk=topR['book_id']).title
            book['rate'] = topR['avgRate']
            books.append(book)
        topFollowed = Author.objects.values('name','id').annotate(numFollowers=Count('users')).order_by('-numFollowers')[:5]
        topFavourited = Category.objects.values('title','id').annotate(numFavs=Count('users')).order_by('-numFavs')[:5]
        
        latestPub = Book.objects.order_by('-published_at')[:3]
        for book in latestPub:
            book.pic = book.book_pic.url.replace("bookZone/","/",1)
            book.isRead = book.users_read.filter(pk=request.user.id)
            book.isWish = book.users_wishlist.filter(pk=request.user.id)

        context['topRated'] = books
        context['topFollowed'] = topFollowed
        context['topFavourited'] = topFavourited
        context['latestPub'] = latestPub
        return render(request,'bookZone/index.html',context)
    else:
        return redirect('/')

# Builds Sign Up page
def signup(request):
    context = checkAll(request)
    if context:
        return redirect("bookZone/")
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('bookZone/')
        else:
            form = SignUpForm()
            return render(request, 'registration/signup.html', {'form': form})

# Builds User Profile page
def userProfile(request,**kwargs):
    context = checkAll(request)
    if context:
        if len(kwargs) == 0:
            u = User.objects.get(pk=request.user.id)
            context['user'] = u;
            return render(request, 'bookZone/userProfile.html',context)
        else:
            if kwargs['status'] == "edit":
                u = User.objects.get(pk=request.user.id)
                context['user'] = u;
                return render(request, 'bookZone/userProfileEdit.html',context)
            elif kwargs['status'] == "save":
                username = request.GET.get('username', None)
                firstname = request.GET.get('firstname', None)
                lastname = request.GET.get('lastname', None)
                email = request.GET.get('email', None)
                u = User.objects.get(pk=request.user.id)
                u.username = username
                u.first_name = firstname
                u.last_name = lastname
                u.email = email
                u.save()
                return HttpResponse("/bookZone/user")
            elif kwargs['status'] == "pass":
                if request.method == 'POST':
                    form = PasswordChangeForm(request.user, request.POST)
                    if form.is_valid():
                        user = form.save()
                        update_session_auth_hash(request, user)  # Important!
                        messages.success(request, 'Your password was successfully updated!')
                        return redirect('users')
                    else:
                        messages.error(request, 'Please correct the error below.')
                else:
                    form = PasswordChangeForm(request.user)
                
                context['form'] = form;
                return render(request, 'bookZone/userPassEdit.html', context)
    else:
        return redirect('/')

# Builds Category page
def category(request,**kwargs):
    context = checkAll(request)
    if context:
        if(len(kwargs) == 0):
            category = Category.objects.all()
            for cat in category:
                cat.pic = cat.cat_pic.url.replace("bookZone/","/",1)
                cat.isFav = cat.users.filter(pk=request.user.id)
            context['categories'] = category
            return render(request, 'bookZone/category.html',context)
        else:
            books = Book.objects.filter(categories=kwargs['category_id'])
            for book in books:
                book.pic = book.book_pic.url.replace("bookZone/","/",1)
                book.isRead = book.users_read.filter(pk=request.user.id)
                book.isWish = book.users_wishlist.filter(pk=request.user.id)
            context['books'] = books
            return render(request, 'bookZone/book.html',context)
    else:
        return redirect('/')

# Does the Favourite an Un Favourite functions
def fav(request,**kwargs):
    context = checkAll(request)
    if context:
        category = Category.objects.get(pk=kwargs['category_id'])
        categs = Category.objects.all()
        if kwargs['fav'] == "fav":
            category.users.add(request.user.id)
        elif kwargs['fav'] == "unfav":
            category.users.remove(request.user)
        context['categories'] = categs
        return redirect('/bookZone/category',context)
    else:
        return redirect('/')

# Builds the Author page
def author(request,**kwargs):
    context = checkAll(request)
    if context:
        if len(kwargs) == 0:
            authors = Author.objects.all()
            one = "many";
            for author in authors:
                author.pic = author.author_pic.url.replace("bookZone/","/",1)
                author.isFollowed = author.users.filter(pk=request.user.id)
            context['authors'] = authors
            context['one'] = one
            return render(request, 'bookZone/authors.html',context)
        else:
            authors = Author.objects.filter(id=kwargs['id'])
            books = Book.objects.filter(author_id=kwargs['id'])
            one = "one"
            for author in authors:
                author.pic = author.author_pic.url.replace("bookZone/","/",1)
                author.isFollowed = author.users.filter(pk=request.user.id)
            context['authors'] = authors
            context['one'] = one
            context['authorBook'] = books
            return render(request, 'bookZone/authors.html',context)
    else:
        return redirect('/')

# Does the Follow an Un Follow functions
def follow(request,**kwargs):
    context = checkAll(request)
    if context:
        author = Author.objects.get(pk=kwargs['author_id'])

        if kwargs['follow'] == "follow":
            author.users.add(request.user.id)
        elif kwargs['follow'] == "unfollow":
            author.users.remove(request.user)
        context['authors'] = author
        
        return redirect('/bookZone/authors/'+str(kwargs['author_id']),context)
    else:
        return redirect('/')

# Builds the Book page
def book(request):
    context = checkAll(request)
    if context:
        books = Book.objects.all()
        for book in books:
            book.pic = book.book_pic.url.replace("bookZone/","/",1)
            book.isRead = book.users_read.filter(pk=request.user.id)
            book.isWish = book.users_wishlist.filter(pk=request.user.id)
        context['books'] = books
        return render(request, 'bookZone/book.html',context)
    else:
        return redirect('/')

# Builds the Book Details page
def bookDetails(request,book_id):
    context = checkAll(request)
    if context:
        details = Book.objects.filter(pk=book_id)
        categories = []
        for det in details:
            det.pic = det.book_pic.url.replace("bookZone/","/",1)
            categories = Category.objects.filter(book=det)
        try:
            b = Book.objects.get(pk=book_id, users_read= request.user.id)
            readStatus = "yes"
        except ObjectDoesNotExist:
            readStatus = "no"

        try:
            b = Book.objects.get(pk=book_id, users_wishlist= request.user.id)
            wishStatus = "yes"
        except ObjectDoesNotExist:
            wishStatus = "no"

        try:
            r= rateBook.objects.get(user_id=request.user,book_id=book_id)
        except ObjectDoesNotExist:
            r=0

        context['bookDetails'] = details
        context['readStatus'] = readStatus
        context['wishStatus'] = wishStatus
        context['rate'] = r
        context['categories'] = categories
        return render(request, 'bookZone/bookDetails.html',context)
    else:
        return redirect('/')

# Does the Read , WishList and Rate Functions
def status(request,**kwargs):
    context = checkAll(request)
    if context:
        book =Book.objects.get(pk=kwargs['book_id'])
        if kwargs['status'] == "wishlist":
            book.users_wishlist.add(request.user)
            book.users_read.remove(request.user)
            book.save()
        elif kwargs['status'] == "nowishlist":
            book.users_wishlist.remove(request.user)
        elif kwargs['status'] == "read":
            book.users_read.add(request.user)
            book.users_wishlist.remove(request.user)
            book.save()
        elif kwargs['status'] == "noread":
            book.users_read.remove(request.user)
        elif kwargs['status'] == "rate":
            try:
                r=rateBook.objects.get(user_id=request.user,book_id=book)
                r.rate=kwargs['rate_id']
                r.save()
            except ObjectDoesNotExist:
                r=rateBook(user_id=request.user,book_id=book,rate=kwargs['rate_id'])
                r.save()

        context['books'] = book
        return redirect('/bookZone/book/'+str(kwargs['book_id']),context)
    else:
        return redirect('/')


def search(request):
    context = checkAll(request)
    if context:
        if request.method == 'GET':
            resAuthors = Author.objects.filter(Q(name__icontains=request.GET['q']) | Q(bio__icontains=request.GET['q']))
            resCategs = Category.objects.filter(Q(title__icontains=request.GET['q']) | Q(desciption__icontains=request.GET['q']))
            resBooks = Book.objects.filter(Q(title__icontains=request.GET['q']) | Q(desciption__icontains=request.GET['q']))

            for author in resAuthors:
                author.pic = author.author_pic.url.replace("bookZone/","/",1)
                author.isFollowed = author.users.filter(pk=request.user.id)

            for categ in resCategs:
                categ.pic = categ.cat_pic.url.replace("bookZone/","/",1)
                categ.isFavourite = categ.users.filter(pk=request.user.id)

            for book in resBooks:
                book.pic = book.book_pic.url.replace("bookZone/","/",1)
                book.isRead = book.users_read.filter(pk=request.user.id)
                book.isWish = book.users_wishlist.filter(pk=request.user.id)
            
            context['authors'] = resAuthors
            context['categories'] = resCategs
            context['books'] = resBooks
            return render(request, 'bookZone/search.html',context)
    else:
        return redirect('/')

