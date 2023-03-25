import filestack


class FileSharer:
	def __init__(self, filepath=f"download.jpg", api_key="AmJkWTGMSxSKoGxC3EWHdz"):
		self.filepath = filepath
		self.api_key = api_key

	def upload(self):
		client = filestack.Client(self.api_key)
		new_file = client.upload(filepath=self.filepath)
		return new_file.url


if __name__ == "__main__":
	filepath = input("Enter the filepath of the image (leave blank for download.jpg): ")
	if filepath == "":
		filepath = "download.jpg"
	url = FileSharer(filepath=filepath).upload()
	print("Link:", url)
