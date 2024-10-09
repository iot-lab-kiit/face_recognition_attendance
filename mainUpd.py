#updated code
import face_recognition
import cv2
import numpy as np
import time
import pandas as pd
import os
import tkinter as tk
from datetime import datetime, timezone
from multiprocessing import Process

# Start video capture
video_capture = cv2.VideoCapture(0)
logging_file = open('log.txt', "a")
global window
global flag
flag = 0

# Get video frame dimensions
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

counter = 1  # Initialize counter for mouse clicks

# Mouse click function for setting in_time and out_time
def mouse_click(event, x, y, flags, params):
    global time_type, counter, flag, window
    time_type = ""
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if x < 320:
            time_type = "in_time"
        else:
            time_type = "out_time"
        
        if counter % 2 == 0:  # Log time on every second click
            logging_file.write(name + " " + time_type + " " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
        counter += 1
        flag = 1
        window.destroy()

# Load known face encodings and names from the "Images" folder
folderPath = 'Images'
known_face_encodings = []
known_face_names = []

for file in os.listdir(folderPath):
    img_path = os.path.join(folderPath, file)
    image = face_recognition.load_image_file(img_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    
    # Extract name from file name
    name = file.split('.')[0]
    
    # Append face encoding and name to lists
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

# Initialize variables for face recognition
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    if flag == 1:
        time.sleep(2)
        flag = 0

    ret, frame = video_capture.read()
    cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', mouse_click)

    # Resize frame to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Process every other frame to save time
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown or try again...."
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            face_names.append(name)
    
    process_this_frame = not process_this_frame

    # Draw face boxes and names
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        frame = cv2.putText(frame, name, (left + 14, bottom - 6), font, 0.5, (255, 255, 255), 1)

        if counter % 2 == 0:
            frame = cv2.putText(frame, "IN", (int(width / 4), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 5)
            frame = cv2.putText(frame, "OUT", (int(3 * width / 4), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 5)
            frame = cv2.line(frame, (int(width / 2), 0), (int(width / 2), int(height)), (255, 255, 255), 2)
        else:
            frame = cv2.putText(frame, "FACE DETECTED", (int(width / 4), 440), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 5)
            frame = cv2.putText(frame, "CLICK TO CONTINUE", (int(width / 5), 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 5)

        cv2.imshow('Video', frame)

        window = tk.Tk()
        window.withdraw()
        window.geometry("6x6")
        window.mainloop()

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
video_capture.release()
cv2.destroyAllWindows()

logging_file.close()
