# Face Recognition Attendance System
The Face Recognition Attendance System is a Python-based project that utilizes face recognition techniques to automate the attendance process. It provides an efficient and convenient way of marking attendance by recognizing and verifying faces of individuals. 

## Table of Content
- [Face Recognition Attendance System](#face-recognition-attendance-system)
  - [Table of Content](#table-of-content)
  - [Features](#features)
  - [Technology used](#technology-used)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Future Scope](#future-scope)

## Features

- Face detection and recognition: The system detects faces in images or video streams and recognizes them by comparing them with known faces in the database.
- Attendance logging: It maintains a log of attendance records, including the date, time, and individual's name or identifier.
- Real-time processing: The system can perform face recognition in real-time, making it suitable for live attendance management.
- User-friendly interface: It provides a simple and intuitive interface to interact with the system, allowing users to easily enroll new faces, update the database, and view attendance records.

## Technology used
- Technology used in this project is Python, OpenCV, and [deepface library](https://pypi.org/project/deepface/) for facial recognition & face verification. Pandas for data manipulation and maintaing records in csv files. Tkinter for GUI.

## Usage
- Install all the requirements, ```pip install -r requirements.txt```
- Launch the application by running main.py: ```python main.py```
- Use the provided user interface to perform various tasks such as enrolling new faces, updating the face database, and viewing attendance records.
- 
- For registering the face Enter the Name in Specified Block, then click on register button, then the camera will open and the user will be asked to look at the camera. The system will capture the face and save it in the database.
  
- When the user clicks In button, the camera will open and the user will be asked to look at the camera. The system will recognize the user and mark the attendance of the user as IN.
  
- When the user clicks Out button, the camera will open and the user will be asked to look at the camera. The system will recognize the user and mark the attendance of the user as OUT.
  
- Attendance records will be logged in the specified file, including the date, time, and the name or identifier of the individual.
- The system can be used to automate the attendance process in various settings, such as schools, colleges, offices, and events.

## Contributing

If you would like to contribute to this project, please read our [Contributing Guidelines](contributing.md).

## Future Scope

- As this code is developed, new features will be added, The main one being authenticity in face recognition. This application will be connected with an OxyMeter
made with IoT technology, which will authenticate the user being present in real time by reading their fingerprint and displaying their oxygen level.


This project is done and is in use in **IoT lab. KIIT**

