
# from flask import Flask, request, jsonify, render_template
# import cv2
# import os
# import time
# from deepface import DeepFace

# app = Flask(__name__, template_folder="D:\\project_finalyear\\backend\\templates", static_folder="D:\\project_finalyear\\backend\\static")

# # Define paths
# db_path = "D:\\project_finalyear\\backend\\database"
# temp_image_path = "D:\\project_finalyear\\backend\\temp_face.jpg"

# # Ensure database exists
# if not os.path.exists(db_path):
#     os.makedirs(db_path)

# # Load OpenCV Face Detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# # Serve the homepage
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Function to capture an image from the webcam
# def capture_face():
#     cap = cv2.VideoCapture(0)
#     time.sleep(2)  # Allow camera to adjust
#     ret, frame = cap.read()
#     cap.release()

#     if ret:
#         cv2.imwrite(temp_image_path, frame)
#         return temp_image_path
#     else:
#         return None

# @app.route('/detect', methods=['POST'])
# def detect_face():
#     # Check if an image file is uploaded
#     if 'file' in request.files:
#         image = request.files['file']
#         image_path = os.path.join(db_path, "uploaded.jpg")
#         image.save(image_path)
#     else:
#         # No file uploaded, use webcam
#         image_path = capture_face()
#         if image_path is None:
#             return jsonify({"error": "Could not capture image"}), 500

#     # Detect face and store it in the database
#     frame = cv2.imread(image_path)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     if len(faces) == 0:
#         return jsonify({"message": "No face detected!"}), 400

#     x, y, w, h = faces[0]
#     face_region = frame[y:y+h, x:x+w]
#     face_filename = f"{db_path}/person_{int(time.time())}.jpg"
#     cv2.imwrite(face_filename, face_region)

#     return jsonify({"message": "Face detected and stored!", "path": face_filename})

# @app.route('/recognize', methods=['POST'])
# def recognize_face():
#     # Check if an image file is uploaded
#     if 'file' in request.files:
#         image = request.files['file']
#         image_path = os.path.join(db_path, "uploaded.jpg")
#         image.save(image_path)
#     else:
#         # No file uploaded, use webcam
#         image_path = capture_face()
#         if image_path is None:
#             return jsonify({"error": "Could not capture image"}), 500

#     # Run DeepFace Recognition
#     try:
#         result = DeepFace.find(img_path=image_path, db_path=db_path, model_name="Facenet", enforce_detection=False)
#         if len(result) > 0 and len(result[0]) > 0:
#             return jsonify({"message": "Match Found!", "result": result[0].to_dict()})
#         else:
#             return jsonify({"message": "No Match Found!"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import cv2
import os
import time
from deepface import DeepFace

app = Flask(__name__, static_folder="static", template_folder="templates")

# Define Paths
UPLOAD_FOLDER = "D:\\project_finalyear\\backend\\uploads"
TEMP_IMAGE_PATH = "D:\\project_finalyear\\backend\\temp_face.jpg"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to Capture Image from Webcam
def capture_webcam_image():
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # Allow camera to adjust
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        cv2.imwrite(TEMP_IMAGE_PATH, frame)  # Save captured image
        return TEMP_IMAGE_PATH
    else:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["file"]
    upload_path = os.path.join(UPLOAD_FOLDER, "reference.jpg")
    file.save(upload_path)  # Save uploaded image

    return jsonify({"message": "Image Uploaded!", "path": upload_path})

@app.route("/detect", methods=["POST"])
def detect_and_save_face():
    # Capture real-time image from webcam
    webcam_image_path = capture_webcam_image()
    if webcam_image_path is None:
        return jsonify({"error": "Could not capture webcam image!"}), 500

    # Save detected face as reference
    reference_image_path = os.path.join(UPLOAD_FOLDER, "reference.jpg")
    os.rename(webcam_image_path, reference_image_path)  # Move the detected face to reference storage

    return jsonify({"message": "Face Detected & Saved!", "path": reference_image_path})

@app.route("/recognize", methods=["POST"])
def recognize_from_webcam():
    # Ensure there's a reference image (either uploaded or saved from webcam)
    reference_image_path = os.path.join(UPLOAD_FOLDER, "reference.jpg")
    if not os.path.exists(reference_image_path):
        return jsonify({"error": "No reference image available!"}), 400

    # Capture real-time image from webcam
    webcam_image_path = capture_webcam_image()
    if webcam_image_path is None:
        return jsonify({"error": "Could not capture webcam image!"}), 500

    # Perform Face Recognition
    try:
        result = DeepFace.verify(img1_path=reference_image_path, img2_path=webcam_image_path, model_name="Facenet", enforce_detection=False)

        if result["verified"]:
            return jsonify({"message": "Match Found!", "distance": result["distance"]})
        else:
            return jsonify({"message": "No Match Found!", "distance": result["distance"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
