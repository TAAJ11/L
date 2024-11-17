# -*- coding: utf-8 -*-
"""DL_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KxQjfD0R7Wno2VRU-_JvGd0T3L1FZt8R
"""

import os
import numpy as np
os.environ['KAGGLE_USERNAME'] = "Harita"
os.environ['KAGGLE_KEY'] = "28739d1288d2cf227bb6aa942bee9820"

!kaggle datasets download imrankhan77/autistic-children-facial-data-set
!unzip /content/autistic-children-facial-data-set.zip

import os
import numpy as np
import cv2
from sklearn.preprocessing import LabelEncoder

# Function to detect face in an image
def detect_face(image_path, face_cascade):
  img = cv2.imread(image_path)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
  return [(x,y,w,h) for (x,y,w,h) in faces]

# Function to extract face from an image
def extract_face(image_path, face_cascade):
  faces = detect_face(image_path, face_cascade)
  if len(faces) == 0:
    return None
  img = cv2.imread(image_path)
  x,y,w,h = faces[0]
  face_img = img[x:x + w, y:y + h]
  return face_img

# Function to prepare data: load, detect and extract
def prepare_data(data_directory, face_cascade):
  labels = []
  faces = []
  label_names = os.listdir(data_directory)
  for label_name in label_names:
    label_dir = os.path.join(data_directory, label_name)
    for img_name in os.listdir(label_dir):
      img_dir = os.path.join(label_dir, img_name)
      face_img = extract_face(img_dir, face_cascade)
      if face_img is not None:
        faces.append(cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY))
        labels.append(label_name)

  return faces, labels, label_names

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

data_directory = '/content/train'
faces, labels, label_names = prepare_data(data_directory, face_cascade)

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(encoded_labels))

def recognize_face(image_path, recognizer, face_cascade, label_encoder):
  face_img = extract_face(image_path, face_cascade)
  if face_img is not None:
    gray_image = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    label, confidence = recognizer.predict(gray_image)
    name = label_encoder.inverse_transform([label])[0]
    return name, confidence
  return None, None

image_path = '/content/Sad_Person.jpeg'
name, confidence = recognize_face(image_path, recognizer, face_cascade, label_encoder)
print(f"Predicted name: {name}, Confidence: {confidence}")

import cv2

# Initialize face detector
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Detect faces and draw rectangles
    faces = faceCascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()