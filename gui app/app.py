import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import cv2
import threading
from datetime import datetime, date
from face_utils import recognize_face, add_user, load_model
from utils import ensure_setup, has_already_logged_today
from config import DB_PATH, CSV_FILE
import os
import platform
import subprocess

# Setup
ensure_setup(DB_PATH, CSV_FILE)
model = load_model()
cap = cv2.VideoCapture(0)
latest_frame = None
running = True

# Attendance Log
attendance_log = {}

def log_attendance(name, csv_file):
    today_str = date.today().isoformat()
    if has_already_logged_today(name, csv_file):
        print(f"[SKIPPED] {name} already logged today.")
        return False, f"{name} already marked present today."

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(csv_file, 'a') as f:
        f.write(f"{name},{time_now}\n")
    print(f"[LOGGED] {name} at {time_now}")
    return True, f"{name} logged successfully!"

def update_frame():
    global latest_frame
    while running:
        success, frame = cap.read()
        if success:
            latest_frame = frame.copy()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        video_label.after(10, lambda: None)

def mark_attendance():
    global latest_frame
    if latest_frame is None:
        toast("No webcam frame available", success=False)
        return

    frame = latest_frame.copy()
    name = recognize_face(frame)
    if name == "Unknown":
        toast("Face not recognized", success=False)
        return

    success, message = log_attendance(name, CSV_FILE)
    toast(message, success=success)

def toast(message, success=True):
    toast_label.config(text=message, bg="green" if success else "red")
    toast_label.pack()
    root.after(3000, lambda: toast_label.pack_forget())

def stop_app():
    global running
    running = False
    cap.release()
    root.destroy()

def open_logs():
    try:
        csv_path = os.path.abspath(CSV_FILE)
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', csv_path], check=True)
        elif platform.system() == 'Windows':
            os.startfile(csv_path)
        else:  # Linux
            subprocess.run(['xdg-open', csv_path], check=True)
    except Exception as e:
        print(f"[ERROR] Failed to open CSV: {e}")
        messagebox.showerror("Error", f"Could not open attendance.csv:\n{e}")

def add_user_ui():
    global latest_frame
    if latest_frame is None:
        toast("No webcam frame available", success=False)
        return

    name = name_entry.get().strip().lower()
    if not name:
        toast("Enter a valid name", success=False)
        return

    frame = latest_frame.copy()
    success = add_user(frame, name)
    if success:
        toast(f"{name} added successfully!", success=True)
    else:
        toast("Failed to add user", success=False)

# GUI Setup
root = tk.Tk()
root.title("Facial Attendance System")

video_label = tk.Label(root)
video_label.pack()

toast_label = tk.Label(root, fg="white", font=("Helvetica", 12))
toast_label.pack_forget()

controls = tk.Frame(root)
controls.pack(pady=10)

tk.Button(controls, text="Mark Attendance", command=mark_attendance, width=20).grid(row=0, column=0, padx=5)
tk.Button(controls, text="View Logs", command=open_logs, width=20).grid(row=0, column=1, padx=5)
tk.Button(controls, text="Exit", command=stop_app, width=20).grid(row=0, column=2, padx=5)

name_frame = tk.Frame(root)
name_frame.pack(pady=10)

tk.Label(name_frame, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(name_frame)
name_entry.grid(row=0, column=1, padx=5)
tk.Button(name_frame, text="Add User", command=add_user_ui).grid(row=0, column=2, padx=5)

# Start video thread
threading.Thread(target=update_frame, daemon=True).start()

# Run GUI
root.mainloop()

