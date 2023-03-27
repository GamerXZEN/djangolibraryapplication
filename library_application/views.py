from django.shortcuts import render
from .forms import CheckoutForm, AccountForm
from .models import Hold, Account, Book
from django.contrib import messages
from django.core.mail import EmailMessage
from random import randint
from fpdf import FPDF
import time
from upload import FileSharer


def index(request):

	if request.method == 'POST':
		form = CheckoutForm(request.POST)
		if form.is_valid():
			library_number = form.cleaned_data["library_number"]
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			book_name = form.cleaned_data["book_name"]
			book_author_last_name = form.cleaned_data["book_author_last_name"]
			isbn = form.cleaned_data["ISBN"]

			Hold.objects.create(library_number=library_number, first_name=first_name, last_name=last_name,
			                    book_name=book_name, book_author_last_name=book_author_last_name, ISBN=isbn)

			messages.success(request, "Hold successfully placed!")

			message_body = f"Was it you, {first_name.capitalize()} {last_name.capitalize()} who checked out " \
			               f"{book_name.title()}. If yes, please reply to this email with YES (in uppercase). " \
			               f"If no, immediately contact newsgsnc@gmail.com to revoke the hold or change it. For any " \
			               f"questions, contact the mentioned email. We will reach out to you as soon as possible.\n" \
			               f"Current Data:\n" \
			               f"Library Number: {library_number}\n" \
			               f"Name: {last_name.capitalize()}, {first_name.capitalize()}\n" \
			               f"Book Name: {book_name}\n" \
			               f"Author's Last Name: {book_author_last_name.capitalize()}\n" \
			               f"ISBN: {isbn.capitalize()}\n"

			email_var = ""
			res_dict = None
			email_dict = None
			library_data = Account.objects.values_list('library_number', flat=True)
			email_data = Account.objects.all().values_list('email', flat=True)
			for i in range(0, len(library_data), 2):
				res_dict = dict({f"{i + 1}": library_data[i]})
				email_dict = dict({f"{i + 1}": email_data[i]})

			for index in range(0, len(library_data)):
				if library_number == res_dict[f"{index+1}"]:
					email_var += email_dict[f"{index+1}"]
					break

			email_message = EmailMessage("Hold Confirmation Email", message_body, to=[email_var])
			email_message.send()

	return render(request, "index.html")


def about(request):
	return render(request, "about.html")


def book_list(request):
	data = Book.objects.all()
	return render(request, "book_list.html", {"data": data})


def signup(request):
	if request.method == "POST":
		form = AccountForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email"]
			phone = form.cleaned_data["phone"]
			address = form.cleaned_data["address"]
			library_number = _read_txt()

			Account.objects.create(library_number=library_number, phone=phone, address=address)

			messages.success(request, "Account successfully created!")
			time_current_formatted = time.strftime('%H:%M:%S-%d/%m%Y')
			time_current = time.strftime("%H%M%S_%d%m%Y")
			pdf = FPDF()
			pdf.add_page()
			pdf.set_font('Arial', 'B', 24)
			pdf.cell(40, 10, txt=f"Account Information", ln=3)
			pdf.set_font('Helvetica', 'B', 12)
			pdf.cell(70, 10, f"Library Number: {library_number}: ", border=True, ln=1)
			pdf.cell(70, 10, f"Email: {email}: ", border=True, ln=1)
			pdf.cell(70, 10, f"Phone: {phone}: ", border=True, ln=1)
			pdf.cell(200, 10, f"Address: {address.title()}: ", border=True, ln=1)
			pdf.cell(40, 10, txt=f"Created at {time_current_formatted}.")
			print(time_current)
			pdf.output(f"././misc_files/{time_current}")
			file_upload = FileSharer(f"././misc_files/{time_current}")
			url = file_upload.upload()

			message_body = f"Here is your library number: {library_number}\n" \
			               f"Here is your account data: {url}"
			email_message = EmailMessage("Account Confirmation Email", message_body, to=[email])
			email_message.send()

	return render(request, "signup.html")


def _read_txt():
	current_line = None
	with open("././text_files/current_line.txt") as lines:
		current_line = int(lines.read())

	with open("././text_files/library_numbers.txt") as file:
		data = file.readlines()[current_line]

	with open("././text_files/current_line.txt", "w") as lines:
		lines.write(str(current_line+1))

	return str(data)
