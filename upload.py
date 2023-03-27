import filestack
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QTextEdit, QLabel
import sys
import threading

API_KEY = os.getenv("FILESTACK_API_KEY")


class FileSharer:
	def __init__(self, filepath=f"download.jpg", api_key=API_KEY):
		self.filepath = filepath
		self.api_key = api_key

	def upload(self):
		client = filestack.Client(self.api_key)
		new_file = client.upload(filepath=self.filepath)
		return new_file.url


class UploadWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Filestack Upload")
		self.setMinimumSize(505, 410)

		self.url_area = QTextEdit(self)
		self.url_area.setGeometry(10, 10, 480, 320)
		self.url_area.setReadOnly(True)
		self.verScrollBar = self.url_area.verticalScrollBar()

		self.input_box = QLineEdit(self)
		self.input_box.returnPressed.connect(self.send_url)
		self.input_box.setGeometry(20, 340, 380, 30)

		send_button = QPushButton("Send", self)
		send_button.clicked.connect(self.send_url)
		send_button.setGeometry(400, 340, 90, 30)

		clear_button = QPushButton("Clear", self)
		clear_button.clicked.connect(self.url_area.clear)
		clear_button.setGeometry(400, 372, 90, 30)

		self.show()

	def send_url(self):
		user_input = self.input_box.text().strip()
		if user_input:
			self.url_area.append(f"<p style='color:#333333'>Filepath: {user_input}\n</p>")
			self.input_box.clear()

			thread = threading.Thread(target=self.get_filestack_response, args=(str(user_input),))
			thread.start()

	def get_filestack_response(self, user_input):
		response = FileSharer(filepath=user_input).upload()
		self.url_area.append(f"URL: <a href={response} style='color:blue; background-color:#E9E9E9'>{response}\n</a>")


try:
	if __name__ == "__main__":
		app = QApplication(sys.argv)
		window = UploadWindow()
		sys.exit(app.exec())
except ValueError:
	raise Exception("PyQt6 Error")
