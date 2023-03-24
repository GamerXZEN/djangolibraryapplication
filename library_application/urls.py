from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("about", views.about, name="about"),
	path("book_list", views.book_list, name="book_list"),
	path("signup", views.signup, name="signup")
]
