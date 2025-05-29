## Facial Attendance System (Python)

This is a Python-based facial attendance system that uses a webcam to detect and recognize faces in real-time, logs attendance into a CSV file, and allows adding new users to the system via live capture. It uses [DeepFace](https://github.com/serengil/deepface) for facial recognition and OpenCV for video handling.

---

## Features

- Real-time face detection and recognition
- Logs attendance with timestamps to a CSV file
- Add new users via webcam
- Local storage of face images for offline matching
- Visual feedback on recognition results

---

## How to use
Add images to know_faces with names as [name].png/jpg/jpeg
Or capture new user by pressing 'n'
Exit the program after attendance is logged by pressing 'q'

---

## Dependencies

Install the required packages using:

```bash
pip install opencv-python pandas deepface
```


