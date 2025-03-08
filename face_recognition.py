import cv2
import os
import time
from deepface import DeepFace

# Define absolute paths
db_path = "D:\\project_finalyear\\backend\\database"
temp_image_path = "D:\\project_finalyear\\backend\\temp_face.jpg"  # Temporary image for recognition

# Ensure database folder exists
if not os.path.exists(db_path):
    os.makedirs(db_path)

# Load OpenCV's Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open webcam
cap = cv2.VideoCapture(0)

print("📸 Capturing images... Please stay in front of the camera!")

start_time = time.time()
image_count = 1  # Counter for saved images
recognized = False  # Flag to track recognition success

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_region = frame[y:y+h, x:x+w]  # Crop the detected face

        # Save face every 5 seconds
        if time.time() - start_time >= 5:
            img_path = f"{db_path}\\person_{image_count}.jpg"
            cv2.imwrite(img_path, face_region)
            print(f"✅ Saved: {img_path}")
            image_count += 1
            start_time = time.time()  # Reset timer

    # Save frame for recognition
    cv2.imwrite(temp_image_path, frame)

    try:
        # Run DeepFace face recognition
        result = DeepFace.find(img_path=temp_image_path, db_path=db_path, model_name="Facenet", enforce_detection=False)

        if len(result) > 0 and len(result[0]) > 0:
            recognized = True
            print("✅ Match Found!")
            cv2.putText(frame, "Match Found!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            print("❌ No Match Found.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    cv2.imshow("Face Detection & Recognition - Press 'q' to Exit", frame)

    # Stop after capturing 2 images or if 'q' is pressed
    if image_count > 2 or cv2.waitKey(1) & 0xFF == ord("q") or recognized:
        break

cap.release()
cv2.destroyAllWindows()

if recognized:
    print("🎉 Face recognized successfully!")
else:
    print("❌ No match found in database.")
