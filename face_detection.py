import cv2
import time
import os

# Define correct database path
db_path ="D:\\project_finalyear\\backend\\database"

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

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Error: Could not access camera!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Save face every 5 seconds
        if time.time() - start_time >= 5:
            img_path = os.path.join(db_path, f"person_{image_count}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"✅ Saved: {img_path}")
            image_count += 1
            start_time = time.time()  # Reset timer

    cv2.imshow("Face Detection - Press 'q' to Exit", frame)

    # Stop after capturing 2 images or if 'q' is pressed
    if image_count > 2 or cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("🎉 Face images captured and saved!")
