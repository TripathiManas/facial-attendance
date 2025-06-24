# 📸 Facial Attendance System

A real-time facial recognition attendance system built with Python and DeepFace.

This repository includes two implementations:
- 🌐 **Web App** using Flask
- 🖥 **Desktop GUI App** using Tkinter

---

## 📁 Project Structure

facial-attendance/
├── flask_app/ # Flask-based web application
│ ├── app.py
│ ├── templates/
│ ├── static/
│ └── ...
├── gui_app/ # Tkinter desktop GUI version
│ ├── app.py
│ ├── face_utils.py
│ ├── utils.py
│ └── ...
├── data/
│ ├── known_faces/
│ └── attendance.csv
└── README.md

## ✅ Features

- Real-time webcam-based face detection
- Face recognition with DeepFace
- Attendance logging into a CSV file
- Only logs one entry per user per day
- Toast notifications and visual feedback
- Add new users with live face capture
- Works offline once set up

---

## 🌐 Flask Web App

### 🔧 Setup

```bash
cd flask_app
pip install -r requirements.txt
```
---

### ▶️ Run the App
bash
Copy
Edit
python app.py
Then visit: http://127.0.0.1:5000

---

### 🌟 Features: 
- View live webcam feed in browser
- Add users via input form
- Mark attendance via button
- View attendance logs
- Shut down server from UI

---
## 🖥 Native GUI App (Tkinter)

### Features
- Simple Tkinter interface
- Live webcam feed
- Buttons for:
    - Mark Attendance
    - Add User
    - View Logs
    - Exit App
- Opens CSV logs with default system viewer

---

## 🗃 Attendance Log
Attendance is stored in data/attendance.csv in this format:

Name,Timestamp
Example,2025-06-24 10:45:12

---
## 🚫 Limitations
- Accuracy may vary depending on lighting and camera quality
- Face must be clearly visible during registration and recognition
- DeepFace models are large and may need initial download

---

## 🤝 Contributions
Pull requests are welcome! Suggestions, bug reports, and improvements are appreciated.
---
## 📄 License
This project is licensed under the MIT License.
---


