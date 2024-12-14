import cv2
import time
import os
import json
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def gen_dataset():
    # Load the classifier with the correct file path
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Function to crop faces
    def face_crop(img):
        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.2, 5)

        # Check if no faces are detected
        if len(faces) == 0:
            return None

        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
            return cropped_face

    new_pairs = {}
    directory = [d for d in os.listdir(r"C:\Users\pvb02\Desktop\cvv\.ipynb_checkpoints\data")]

    recent_student_id = 0
    if len(directory) == 0:
        recent_student_id = 1
    else:
        arr = directory[-1].split('.')
        recent_student_id = int(arr[1]) + 1

    s_name = input(f"Enter Student name for Id {recent_student_id}: ")
    new_pairs[str(recent_student_id)] = s_name

    cap = cv2.VideoCapture(0)
    img_cnt = 0

    # Wait for Enter key to start capturing
    while True:
        ret, frame = cap.read()

        if not ret:
            return "Error: Unable to capture video feed"

        # Show the live webcam feed
        cv2.imshow("Press Enter to Start", frame)

        # Wait for Enter key to be pressed
        key = cv2.waitKey(1) & 0xFF
        if key == 13:
            print("Starting to capture faces...")
            break

    # Start timer for face detection after Enter is pressed
    start_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to capture video feed.")
            break

        # Detect and crop the face
        face = face_crop(frame)

        if face is not None:
            start_time = time.time()
            img_cnt += 1
            face = cv2.resize(face, (250, 250))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_path = f"data/Student.{recent_student_id}.{img_cnt}.jpg"
            cv2.imwrite(file_path, face)
            print(f"Saved: {file_path}")
            cv2.putText(face, f"ID: {img_cnt}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Cropped Face", face)

        elapsed_time = time.time() - start_time
        if elapsed_time > 10 and face is None:
            print("Student face not detected.")
            cap.release()
            cv2.destroyAllWindows()
            return "Student face not detected"

        if img_cnt == 25:
            try:
                with open("../pairs.json", "r") as f:
                    pairs = json.load(f)
            except FileNotFoundError:
                pairs = {}

            pairs.update(new_pairs)

            with open("../pairs.json", "w") as f:
                json.dump(pairs, f, indent=4)

            print("Updated pairs.json successfully!")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Sample collection completed.")


@app.route("/home")
def home():
    with open("../pairs.json", 'r') as file:
        data = json.load(file)
    return render_template("ide.html", data=data)


@app.route("/run_datacollect")
def run_datacollect():
    # Run the dataset collection function in a separate thread
    threading.Thread(target=gen_dataset).start()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
