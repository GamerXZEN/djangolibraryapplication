from django.contrib import admin
from .models import Book, Hold, Account


class UserAdmin(admin.ModelAdmin):
	list_display = ("library_number", "first_name", "last_name", "book_name", "book_author_last_name")
	list_filter = ("book_author_last_name",)
	ordering = ("first_name", "last_name", "book_name", "book_author_last_name")
	readonly_fields = ("first_name", "last_name", "book_name", "book_author_last_name")


class BookAdmin(admin.ModelAdmin):
	list_display = ("book_name", "book_author_last_name", "book_author_first_name")
	list_filter = ("book_author_last_name",)
	ordering = ("book_name", "book_author_last_name", "book_author_first_name")


class AccountAdmin(admin.ModelAdmin):
	list_display = ("library_number", "email", "phone")
	ordering = ("email", "phone")
	readonly_fields = ("email", "phone", "address")


admin.site.register(Hold, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Account, AccountAdmin)
