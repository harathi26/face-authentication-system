from flask import Flask, request, jsonify, send_from_directory
import face_recognition
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file size
STUDENTS_DIR = os.getenv('STUDENTS_DIR', 'students')

# Ensure students directory exists
os.makedirs(STUDENTS_DIR, exist_ok=True)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    image_data = data['current_image'].split(",")[1]
    email = data['email']

    with open("image.png", "wb") as f:
        f.write(base64.b64decode(image_data))

    try:
        got_image = face_recognition.load_image_file("image.png")
        existing_image = face_recognition.load_image_file(os.path.join(STUDENTS_DIR, email + ".jpg"))

        got_encoding = face_recognition.face_encodings(got_image)[0]
        existing_encoding = face_recognition.face_encodings(existing_image)[0]

        result = face_recognition.compare_faces([existing_encoding], got_encoding)
        return jsonify({"match": result[0]})
    except Exception as e:
        return jsonify({"match": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)