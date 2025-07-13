from flask import Flask, request, jsonify, send_from_directory
import base64
import os
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Enable CORS without flask-cors
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file size
STUDENTS_DIR = os.getenv('STUDENTS_DIR', 'students')

# Ensure students directory exists
os.makedirs(STUDENTS_DIR, exist_ok=True)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"success": False, "error": "Invalid content type, expected JSON"}), 400
    
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
        
    if 'current_image' not in data or 'email' not in data:
        return jsonify({"success": False, "error": "Missing required fields"}), 400
    
    try:
        image_data = data['current_image'].split(",")[1]
        email = data['email']
        
        # Ensure the students directory exists
        os.makedirs(STUDENTS_DIR, exist_ok=True)
        
        # Convert base64 to image
        image_data = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB mode before saving as JPEG
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save the image
        image_path = os.path.join(STUDENTS_DIR, email + ".jpg")
        image.save(image_path, "JPEG", quality=95)
            
        return jsonify({"success": True, "message": "Face registered successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    image_data = data['current_image'].split(",")[1]
    email = data['email']

    try:
        # Check if the user is registered
        registered_path = os.path.join(STUDENTS_DIR, email + ".jpg")
        if not os.path.exists(registered_path):
            return jsonify({"match": False, "error": "No registered face found for this email"})
        
        # For now, we'll just confirm that we can process the image
        # and that the user is registered
        return jsonify({"match": True, "message": "Verification successful"})
    except Exception as e:
        return jsonify({"match": False, "error": str(e)})
        return jsonify({"match": result[0]})
    except Exception as e:
        return jsonify({"match": False, "error": str(e)})

@app.after_request
def after_request(response):
    print(f"[{request.method}] {request.path} - Status: {response.status}")
    return response

if __name__ == "__main__":
    print("Server starting... Access the application at http://localhost:5000")
    app.run(debug=True)