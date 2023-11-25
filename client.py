import requests

# Replace with the actual path to your image file
image_path = 'D:\OCR_API\Image\sherin.jpg'

# Upload the image to the API
files = {'file': open(image_path, 'rb')}
response = requests.post('http://127.0.0.1:5000/upload', files=files)

# Print the API response
print(response.json())