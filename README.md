<<<<<<< HEAD
# Face Authentication System

A web-based face authentication system built with Flask and face_recognition library.

## Features
- Real-time face capture using webcam
- Face verification against stored images
- Simple email-based user identification

## Setup
1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `students` directory to store face images
6. Run the application:
   ```
   python app.py
   ```

## Usage
1. Open browser and go to `http://localhost:5000`
2. Enter email address
3. Click "Capture & Verify" to authenticate

## Directory Structure
- `app.py`: Main Flask application
- `index.html`: Frontend interface
- `requirements.txt`: Project dependencies
- `students/`: Directory for storing face images (*.jpg)
=======
# face-authentication-system
A web-based face authentication system using Flask
>>>>>>> f260a5876b048df50c81b9f11d78aa137a0dbcae
