import os
import json
import cv2
import csv

id, prediction, confidence = 0, 0, 0


def draw_bound(img, classifier, scaleFactor, minNeighbor, color, clf, pairs):
    """
    Detect faces in the image, draw bounding boxes, and recognize faces using a trained classifier.
    """
    global id, prediction, confidence
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbor)
    recognized_ids = set()  # To collect recognized IDs

    for (x, y, w, h) in features:
        # Draw rectangle around the face
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

        # Predict ID and calculate confidence
        id, prediction = clf.predict(gray_img[y: y + h, x: x + w])
        confidence = int(100 * (1 - prediction / 300))

        if confidence > 70:
            # Retrieve student name based on the ID from pairs
            student_name = pairs.get(str(id), "Unknown")  # Default to "Unknown"
            recognized_ids.add(str(id))
            cv2.putText(img, student_name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "Unknown", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

    return img, recognized_ids


def capture_frame(video_cap, faceCascade, clf, pairs, save_file):
    """
    Capture a frame and detect recognized IDs.
    """
    while True:
        ret, img = video_cap.read()
        if not ret:
            print("Failed to grab frame from camera")
            return

        # Detect and recognize faces in the frame
        img, recognized_ids = draw_bound(img, faceCascade, 1.1, 10, (255, 255, 255), clf, pairs)

        # Display the processed frame
        cv2.imshow("Capture Frame", img)

        # Press 'Enter' to save the recognized IDs
        if cv2.waitKey(1) == 13:  # Enter key
            # Save recognized IDs to file
            with open(save_file, "w", newline="") as f:
                writer = csv.writer(f)
                for student_id in recognized_ids:
                    writer.writerow([student_id])

            print(f"Saved recognized IDs to {save_file}")
            break


def main():
    # Load the Haar Cascade for face detection
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Initialize and load the trained face recognizer
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    # Read pairs dictionary from main file
    with open("pairs.json", "r") as f:
        pairs = json.load(f)

    print("Loaded pairs from pairs.json:")
    print(json.dumps(pairs, indent=4))

    # Start video capture
    video_cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame from the webcam
        ret, img = video_cap.read()
        if not ret:
            print("Failed to grab frame from camera")
            break

        # Display the webcam feed
        cv2.imshow("Face detection", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('0'):
            print("Capturing start frame...")
            capture_frame(video_cap, faceCascade, clf, pairs, "start_frame.csv")
        elif key == ord('1'):
            print("Capturing end frame...")
            capture_frame(video_cap, faceCascade, clf, pairs, "end_frame.csv")
        elif key == 27:  # Esc key to exit
            break

    # Release video capture and close OpenCV windows
    video_cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

