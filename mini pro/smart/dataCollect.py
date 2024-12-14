import cv2
import time
import os
import json

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
    file = {}
    with open(r"C:\Users\pvb02\Desktop\mini pro\smart\pairs.json", 'r') as f:
        file = json.load(f)

    # Determine the next student ID
    recent_student_id = 0
    if len(file) == 0:
        recent_student_id = 1
    else:
        recent_student_id = max(map(int, file.keys())) + 1



    s_name = input(f"Enter Student name for Id {recent_student_id}: ")
    new_pairs[str(recent_student_id)] = s_name

    cap = cv2.VideoCapture(0)
    img_cnt = 0

    # Ensure the `data` directory exists
    # if not os.path.exists("data"):
    #    os.makedirs("data")


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

        # if camera won't work or errors in video capturing display this
        if not ret:
            print("Error: Unable to capture video feed.")
            break

        # Detect and crop the face
        face = face_crop(frame)

        if face is not None:
            # If face is detected, reset the timer
            start_time = time.time()
            img_cnt += 1
            face = cv2.resize(face, (250, 250))  # Resize face to 250x250 pixels
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_path = f"datac/Student.{recent_student_id}.{img_cnt}.jpg"
            cv2.imwrite(file_path, face)  # Save the image
            print(f"Saved: {file_path}")
            cv2.putText(face, f"ID: {img_cnt}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Cropped Face", face)

        # Check if 10 seconds have passed without detecting a face
        elapsed_time = time.time() - start_time
        if elapsed_time > 10 and face is None:
            print("Student face not detected.")
            cap.release()
            cv2.destroyAllWindows()
            return "Student face not detected"

        # Stop after collecting specific number of  images
        if img_cnt == 25:
            try:
                with open("pairs.json", "r") as f:
                    pairs = json.load(f)

            # If the file not found this error will display and create new pairs json file
            except FileNotFoundError:
                pairs = {}

            # Merge the new data with existing data
            pairs.update(new_pairs)

            # Write the updated data back to the file
            with open("pairs.json", "w") as f:
                json.dump(pairs, f, indent=4)

            print("Updated pairs.json successfully!")
            break


        # Exit on pressing 'q'
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    cap.release()
    cv2.destroyAllWindows()
    print("Sample collection completed.")


# call func
gen_dataset()
