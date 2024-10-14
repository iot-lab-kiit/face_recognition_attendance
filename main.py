import tkinter as tk
from tkinter import messagebox
import cv2
import os
import pandas as pd
from datetime import datetime
from deepface import DeepFace

# Directories
image_dir = os.path.join('images')
log_dir = os.path.join('log')
model_name = 'Facenet512'
camera_index = 1

# Load face data
face_data_path = os.path.join(log_dir, 'face_data.csv')
if not os.path.exists(face_data_path):
    pd.DataFrame(columns=['Name', 'ImagePath']).to_csv(face_data_path, index=False)

face_data = pd.read_csv(face_data_path)

# Attendance log function
def log_attendance(name, status):
    log_path = os.path.join(log_dir, 'attendance_log.csv')
    if not os.path.exists(log_path):
        log_df = pd.DataFrame(columns=['Name', 'Time', 'Status'])
    else:
        log_df = pd.read_csv(log_path)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_entry = {'Name': name, 'Time': current_time, 'Status': status}
    log_df = log_df._append(new_entry, ignore_index=True)
    log_df.to_csv(log_path, index=False)
    messagebox.showinfo("Attendance", f"{status} logged for {name} at {current_time}.")

# Face registration function
def register_face():
    name = entry_name.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    messagebox.showinfo("Info", "Press 's' to capture the image.")
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image.")
            break

        # Reduce the resolution of the frame
        frame = cv2.resize(frame, (640, 480))

        cv2.imshow('Register Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            image_path = os.path.join(image_dir, f"{name}.jpg")
            cv2.imwrite(image_path, frame)

            # Update CSV
            new_data = pd.DataFrame({'Name': [name], 'ImagePath': [image_path]})
            face_data = pd.read_csv(face_data_path)
            face_data = face_data._append(new_data, ignore_index=True)
            face_data.to_csv(face_data_path, index=False)
            
            messagebox.showinfo("Success", f"Face for {name} registered successfully.")
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Face recognition function
def recognize_face(status):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image.")
            break

        # Reduce the resolution of the frame
        frame = cv2.resize(frame, (640, 480))

        img_path = 'temp.jpg'
        cv2.imwrite(img_path, frame)

        try:
            detected_faces = DeepFace.extract_faces(img_path, detector_backend='opencv', enforce_detection=False)
            if detected_faces:
                for face in detected_faces:
                    x, y, w, h = face['facial_area']['x'], face['facial_area']['y'], face['facial_area']['w'], face['facial_area']['h']
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    for idx, row in face_data.iterrows():
                        registered_img_path = row['ImagePath']
                        result = DeepFace.verify(img1_path=img_path, img2_path=registered_img_path, model_name=model_name, enforce_detection=False)
                        
                        if result['verified']:
                            name = row['Name']
                            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                            log_attendance(name, status)
                            break

            cv2.imshow('Face Recognition', frame)
            cv2.waitKey(5000)
            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# GUI Setup
window = tk.Tk()
window.title("Face Recognition Attendance System")
window.geometry("400x200")

# Name Entry for registration
tk.Label(window, text="Enter Name (For Registeration Only):").pack(pady=10)
entry_name = tk.Entry(window)
entry_name.pack()

# Register button
register_button = tk.Button(window, text="Register", command=register_face)
register_button.pack(pady=5)

# In and Out buttons
in_button = tk.Button(window, text="In", command=lambda: recognize_face("In"))
in_button.pack(pady=5)

out_button = tk.Button(window, text="Out", command=lambda: recognize_face("Out"))
out_button.pack(pady=5)

window.mainloop()
