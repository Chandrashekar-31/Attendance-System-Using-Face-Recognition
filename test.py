from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

COL_NAMES = ['NAME', 'TIME']

while True:
    ret, frame = video.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        
        file_path = f"C:/Users/LENOVO/Downloads/face_recognition_project-main1/face_recognition_project-main/Attendance/Attendance_{date}.csv"
        exist = os.path.isfile(file_path)
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        
        attendance = [str(output[0]), str(timestamp)]
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    
    if k == ord('o'):
        speak("Attendance Taken.")
        time.sleep(5)
        
        # Combined logic for writing to the CSV file
        with open(file_path, 'a', newline='') as csvfile:  # Changed mode to 'a' for append
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(COL_NAMES)  # Write header if file doesn't exist
            writer.writerow(attendance)      # Write attendance regardless

    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
