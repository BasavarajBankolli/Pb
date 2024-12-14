import os
import numpy as np
from PIL import Image
import cv2


def train_classifier(data_dir):
    """
    Train the LBPH face recognizer on the images in the given directory.

    :param data_dir: Directory containing the face images.
    """
    # collect all images names in list
    paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith((".jpg", ".jpeg", ".png"))]

    # list to store face data
    faces = []
    # list to store corresponding student id's
    ids = []

    for image_path in paths:
        try:
            # open the image in grayscale mode
            img = Image.open(image_path).convert("L")

            # Convert the image into a NumPy array
            image_np = np.array(img, 'uint8')

            # Extract the ID from the filename (format: <student>.<id>.<extension>)
            filename = os.path.split(image_path)[1]  # Get the filename
            id = int(filename.split(".")[1])  # read id and convert that into int()

            # Append the face data and corresponding ID
            faces.append(image_np)
            ids.append(id)

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    # convert the ids list to a NumPy array
    ids = np.array(ids)

    # Train the classifier file and save it.
    clf = cv2.face.LBPHFaceRecognizer_create()  # Recognizer: Create LBPH face recognizer
    clf.train(faces, ids)  # Train on the collected data
    clf.write("classifier.xml")  # Save the trained model to a file

    print("Training completed. Classifier saved as 'classifier.xml'.")


# call the func
train_classifier("data")
