from flask import Flask, request, jsonify
import cv2
import easyocr
import matplotlib.pyplot as plt
from flask_cors import CORS  # Optional: Enable CORS if you need to access the API from a different domain

app = Flask(__name__)
CORS(app)  # Optional: Enable CORS if you need to access the API from a different domain

# Load the OCR model for Bengali and English
reader = easyocr.Reader(['bn', 'en'])

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded image file
    file = request.files['file']

    # Save the uploaded image
    file_path = 'uploaded_image.jpg'
    file.save(file_path)

    # Load the uploaded image
    original_image = cv2.imread(file_path)

    # Crop the image (use your specific coordinates)
    cropped_image = original_image[230:800, 260:1000]

    # Perform OCR on the cropped image
    result = reader.readtext(cropped_image)

    # Process the OCR results
    ocr_dict = {}
    current_key = None
    for detection in result:
        text = detection[1].strip()
        if ':' in text:
            current_key, value = text.split(':', 1)
            ocr_dict[current_key.strip()] = value.strip()
        elif current_key is not None:
            ocr_dict[current_key] += ' ' + text

    # Create a dictionary structure as per your example
    output_dict = {
        "নাম": ocr_dict.get("নাম"),
        "Name":ocr_dict.get("Name"),
        "পিতা": ocr_dict.get("পিতা"),
        "মাতা": ocr_dict.get("মাতা"),
        "Date of Birth": ocr_dict.get("Date of Birth"),
        "ID NO": ocr_dict.get("ID NO")
    }

    # Accessing the model value
    x = output_dict.get("model")

    # Printing the formatted output
    for key, value in output_dict.items():
        print(f'{key}: {value}')

    # Return the OCR results as JSON
    return jsonify(output_dict)

if __name__ == '__main__':
    app.run(debug=True)