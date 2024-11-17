
import os
import json
import requests
from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, request, render_template, jsonify
from PIL import Image
import io

# Initialize Flask app
app = Flask(__name__)

# Initialize Google Vision Client
client = vision.ImageAnnotatorClient()

# Path to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy e-commerce API endpoint for clothing suggestions (you can replace it with a real API)
ECOMMERCE_API_URL = "https://api.ecommerce.com/v1/products"

# Function to analyze the selfie using Google Vision API
def analyze_selfie(image_path):
    """Analyze a selfie to provide dating and hairstyle advice."""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.face_detection(image=image)

    # Analyze facial expressions (e.g., smiling, joy, sorrow)
    faces = response.face_annotations
    advice = []

    for face in faces:
        if face.sorrowLikelihood == 'LIKELY' or face.sorrowLikelihood == 'VERY_LIKELY':
            advice.append("Try to showcase a positive and cheerful expression for a more inviting look!")
        elif face.joyLikelihood == 'LIKELY' or face.joyLikelihood == 'VERY_LIKELY':
            advice.append("You look great with that smile! Confidence is key.")

        # You could also analyze other aspects of facial features like gender, age, etc., for better customization.
    return advice

# Function to analyze the outfit using image analysis (simplified for now)
def analyze_outfit(image_path):
    """Analyze the outfit from the image and suggest clothing items."""
    # For simplicity, let's assume a dummy analysis (you can use a fashion-specific model for more detailed suggestions).
    product_suggestions = [
        {"product_name": "Trendy T-shirt", "url": "https://www.example.com/product/1"},
        {"product_name": "Stylish Jeans", "url": "https://www.example.com/product/2"},
    ]
    return product_suggestions

# Function to provide hairstyle suggestions based on the user's selfie
def suggest_hairstyles(image_path):
    """Suggest hairstyles based on the analysis of the selfie."""
    # This would require a hair-detection model or API, but for simplicity, we provide dummy suggestions here.
    return [
        {"hairstyle": "Curly Bob", "url": "https://www.example.com/hairstyle/1"},
        {"hairstyle": "Long Wavy Hair", "url": "https://www.example.com/hairstyle/2"},
    ]

# Route for uploading selfie and fashion images
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the uploaded images
        selfie = request.files['selfie']
        outfit = request.files['outfit']

        # Save images temporarily
        selfie_path = os.path.join(app.config['UPLOAD_FOLDER'], "selfie.jpg")
        outfit_path = os.path.join(app.config['UPLOAD_FOLDER'], "outfit.jpg")
        selfie.save(selfie_path)
        outfit.save(outfit_path)

        # Analyze selfie and outfit
        selfie_advice = analyze_selfie(selfie_path)
        outfit_suggestions = analyze_outfit(outfit_path)
        hairstyle_suggestions = suggest_hairstyles(selfie_path)

        # Return the analysis and suggestions to the user
        return render_template('result.html', selfie_advice=selfie_advice, 
                               outfit_suggestions=outfit_suggestions, 
                               hairstyle_suggestions=hairstyle_suggestions)

    return render_template('index.html')

# Route for viewing the result (will display the suggestions)
@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)
```

### **HTML Templates**

#### `templates/index.html` (Upload Form)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Your Selfie and Outfit</title>
</head>
<body>
    <h1>Upload Your Selfie and Outfit</h1>
    <form action="/" method="POST" enctype="multipart/form-data">
        <label for="selfie">Upload Your Selfie:</label>
        <input type="file" name="selfie" accept="image/*" required><br><br>
        <label for="outfit">Upload Your Outfit:</label>
        <input type="file" name="outfit" accept="image/*" required><br><br>
        <input type="submit" value="Get Dating Advice">
    </form>
</body>
</html>
```

#### `templates/result.html` (Display Results)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Dating Advice Results</title>
</head>
<body>
    <h1>Your Dating Advice Based on Your Uploads</h1>

    <h2>Selfie Advice:</h2>
    <p>Based on your selfie, here’s some advice:</p>
    <ul>
        {% for advice in selfie_advice %}
            <li>{{ advice }}</li>
        {% endfor %}
    </ul>

    <h2>Outfit Suggestions:</h2>
    <p>Here are some product suggestions for your outfit:</p>
    <ul>
        {% for suggestion in outfit_suggestions %}
            <li><a href="{{ suggestion.url }}" target="_blank">{{ suggestion.product_name }}</a></li>
        {% endfor %}
    </ul>

    <h2>Hairstyle Suggestions:</h2>
    <p>Based on your selfie, here are some hairstyle suggestions:</p>
    <ul>
        {% for hairstyle in hairstyle_suggestions %}
            <li><a href="{{ hairstyle.url }}" target="_blank">{{ hairstyle.hairstyle }}</a></li>
        {% endfor %}
    </ul>

    <br><br>
    <a href="/">Go Back</a>
</body>
</html>
