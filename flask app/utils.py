import os
from datetime import datetime
from datetime import date

def ensure_setup(db_path, csv_file):
    os.makedirs(db_path, exist_ok=True)
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as f:
            f.write("Name,Time\n")


def log_attendance(name, csv_file, attendance_log):
    if name not in attendance_log:
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attendance_log[name] = time_now
        with open(csv_file, 'a') as f:
            f.write(f"{name},{time_now}\n")
        print(f"[LOGGED] {name} at {time_now}")
        

def has_already_logged_today(name, csv_file):
    today = date.today().isoformat()  # e.g., "2025-06-24"
    try:
        with open(csv_file, 'r') as f:
            lines = f.readlines()[1:]  # skip header
            for line in lines:
                n, timestamp = line.strip().split(',')
                if n == name and timestamp.startswith(today):
                    return True
    except FileNotFoundError:
        return False  # No file yet = no logs yet
    return False

