from django.db import models


class Hold(models.Model):

	library_number = models.CharField(max_length=20)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	book_name = models.CharField(max_length=255)
	book_author_last_name = models.CharField(max_length=100)
	ISBN = models.CharField(max_length=255)

	def __str__(self):
		return f"Hello, {self.first_name} {self.last_name}"


class Book(models.Model):
	book_name = models.CharField(max_length=255)
	book_author_last_name = models.CharField(max_length=100)
	book_author_first_name = models.CharField(max_length=100)
	ISBN = models.CharField(max_length=255)
	pic_url = models.CharField(max_length=255)


class Account(models.Model):
	library_number = models.CharField(max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=17)
	address = models.CharField(max_length=255)
