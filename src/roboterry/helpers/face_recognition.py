# ----------------------------------------
# Face recognition module
# 
# ----------------------------------------

import os
import cv2
import numpy as np

# Image libraries
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from matplotlib.image import imread


class FaceRecognizer:
    def __init__(self, debug=False):
        self.debug = debug
        self.face_recog = None
        self.haar_path = ""
        self.model_filepath = ""
        self.training_folder = ""
        self.people = ["kieran", "franka", "carlos"]

        self._initialize_face_recognizer()

    def _initialize_face_recognizer(self):
        """Initialize several objects and paths"""
        self.face_recog = cv2.face.LBPHFaceRecognizer_create()

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(cur_dir)
        self.model_filepath = os.path.join(parent_dir, "data", "model", "face_recog_trained.yml")
        self.haar_path = os.path.join(parent_dir, "data", "model", "haarcascade_frontalface_alt2.xml")
        # self.haar_path = os.path.join(parent_dir, "data", "model", "haarcascade_frontalface_default.xml")
        self.training_folder = os.path.join(parent_dir, "data", "training_data")

        if os.path.isfile(self.model_filepath):
            # We already have a model!
            print(f"[+] Found saved model: {self.model_filepath}")
            self.face_recog.read(self.model_filepath)
        else:
            print(f"[-] Training model from scratch...")
            self.train_classifier()

    def detect_face(self, img, scale=1.05, nb=5):
        """Finds a face within a given image"""

        face_detector = cv2.CascadeClassifier(self.haar_path)

        # We'll use detectMultiScale since all images are at different
        # distances from the camera...
        # NOTE: this expects the `img` to be gray-scale already
        face_list = face_detector.detectMultiScale(
            img,
            scaleFactor=scale,
            minNeighbors=nb,
            minSize=(128, 128),
            flags=cv2.CASCADE_SCALE_IMAGE
            )

        # Faces are actually the coordinate information of a rectangle
        # containing the face's pixels
        if self.debug:
            for (x, y, w, h) in face_list:
                # Draw a rectangle around the faces
                cv2.rectangle(
                    img,
                    (x, y),
                    (x + w, y + h),
                    (0xFF, 0xFF, 0xFF),  # white rectangle
                    3
                )

                plt.imshow(img, cmap='gray')
                plt.show()

        return face_list, img

    def get_training_data(self, scale=1.05, nb=5):
        """Training data contains images
           for each person labeled: <person_name>.<N>.jpg,
           e.g. "kieran.0.jpg", "franka.1.jpg", etc.
        """

        idx_training_files = 0
        cropped_faces = []
        identifiers = []

        for filename in os.listdir(self.training_folder):
            if filename.startswith("."):
                continue

            idx_training_files += 1

            filepath = os.path.join(self.training_folder, filename)
            person_name = filename.split(".")[0]
            face_id = self.people.index(person_name)  # {0, 1, 2, ...}

            # PIL image, processed
            PIL_image = Image.open(filepath).convert('L')  # gray-scale
            np_image = np.array(PIL_image, 'uint8')  # byte-array
            face_list, _ = self.detect_face(np_image, scale=scale, nb=nb)

            if len(face_list) > 1:
                print(f"[-] Warning: File {filename} contains more than one face! Skipping...")
                continue

            if len(face_list) == 0:
                print(f"[-] Warning: File {filename} did NOT contain any face! Skipping...")
                continue

            (x, y, w, h) = face_list[0]
            cropped_faces.append(np_image[y: y+h, x: x+w])
            identifiers.append(face_id)

        print(f"[+] scale: {scale}, neighbours: {nb} -> Found faces on {len(cropped_faces)} / {idx_training_files} images")

        return cropped_faces, identifiers

    def train_classifier(self, scale=1.05, nb=5):
        """Train the classifier algorithm"""

        face_imgs, face_ids = self.get_training_data(scale=scale, nb=nb)
        self.face_recog.train(
            face_imgs,              # Inputs
            np.array(face_ids)      # Labeled outputs
            )

        # Save the face recognizer for later use. 
        # This has several advantages:
        #  - only have to train the model once
        #  - can train the model on a more powerful machine
        print(f"[+] Saved model as {self.model_filepath}")
        self.face_recog.save(self.model_filepath)

        return self.face_recog

    def who_is(self, img_filepath):
        """Given an image, returns the person's name"""

        initial_image = cv2.imread(img_filepath)
        gray_image = cv2.cvtColor(initial_image, cv2.COLOR_RGB2GRAY)
        face_list, _ = self.detect_face(gray_image)

        if len(face_list) > 1:
            # TODO: deal with several faces
            print("[-] Too many faces. Skipping...")
            return -1, 0

        (x, y, w, h) = face_list[0]
        cropped_gray = gray_image[y: y+h, x: x+w]

        # Finally, we can make a prediction :)
        label, confidence = self.face_recog.predict(cropped_gray)
        person_name = self.people[label]
        print(f"[+] {img_filepath} -> {person_name} (confidence: {confidence})")

        return self.people[label]

