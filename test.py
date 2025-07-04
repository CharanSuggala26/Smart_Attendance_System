from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str1)

with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)

min_samples = min(len(FACES), len(LABELS))
FACES = np.array(FACES[:min_samples])
LABELS = np.array(LABELS[:min_samples])

print(f'Shape of Faces matrix: {FACES.shape} | Labels count: {len(LABELS)}')

# Training model with KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("background.png")

# Configurating webcam for face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

COL_NAMES = ['NAME', 'TIME']

while True:
    ret, frame = video.read()
    if not ret:
        continue

    frame_resized = cv2.resize(frame, (640, 421))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    attendance = None

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist = os.path.isfile(f"Attendance/Attendance_{date}.csv")

        
        cv2.rectangle(frame_resized, (x, y), (x+w, y+h), (50, 50, 255), 2)

        text = str(output[0])
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.9
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

        label_y = y - 10 if y - 10 > 20 else y + h + 30
        cv2.putText(frame_resized, text, (x, label_y), font, font_scale, (50, 50, 255), thickness)

        attendance = [text, timestamp]

    # Frame+Background Intersection(i.e merging into background image)
    imgBackground_copy = imgBackground.copy()
    imgBackground_copy[162:162 + 421, 55:55 + 640] = frame_resized

    cv2.imshow("Frame", imgBackground_copy)

    k = cv2.waitKey(1)
    if k == ord('o') and attendance:
        speak("Attendance Taken..")
        time.sleep(2)
        with open(f"Attendance/Attendance_{date}.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(COL_NAMES)
            writer.writerow(attendance)

    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
