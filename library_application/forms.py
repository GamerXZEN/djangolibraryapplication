from django import forms


class CheckoutForm(forms.Form):
	library_number = forms.CharField(max_length=20)
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	book_name = forms.CharField(max_length=255)
	book_author_last_name = forms.CharField(max_length=100)
	ISBN = forms.CharField(max_length=255)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


class AccountForm(forms.Form):
	email = forms.EmailField()
	phone = forms.CharField(max_length=17)
	address = forms.CharField(max_length=255)

	def __str__(self):
		return "Hello there"
