from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from bookZone import views

urlpatterns = [
	path('', views.index, name='index'),
	#===============================#
	path('category/', views.category, name='category'),
	path('category/<int:category_id>/', views.category, name='categoryBooks'),
	path('category/<str:fav>/<int:category_id>', views.fav, name='favourite'),
	#===============================#
	path('book/', views.book, name='books'),
	path('book/<int:book_id>', views.bookDetails, name='bookDetails'),
	path('book/<str:status>/<int:book_id>', views.status, name='bookStatus'),
	path('book/<str:status>/<int:book_id>/<int:rate_id>', views.status, name='bookRate'),
	#===============================#
	path('authors', views.author, name='authors'),
	path('authors/<int:id>', views.author, name='author'),
	path('authors/<str:follow>/<int:author_id>', views.follow, name='follow'),
	#===============================#
	path('search', views.search),
	#===============================#
	path('user/', views.userProfile, name='users'),
 	path('user/<str:status>', views.userProfile, name='userProfile'),
]
