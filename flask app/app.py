from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
import threading
from datetime import datetime, date

from face_utils import recognize_face, add_user, load_model
from utils import ensure_setup, has_already_logged_today
from config import DB_PATH, CSV_FILE

app = Flask(__name__)
cap = cv2.VideoCapture(0)
attendance_log = {}
ensure_setup(DB_PATH, CSV_FILE)
model = load_model()

@app.route('/')
def index():
    return render_template('index.html')

def log_attendance(name, csv_file):
    today_str = date.today().isoformat()
    if has_already_logged_today(name, csv_file):
        print(f"[SKIPPED] {name} already logged today.")
        return False, f"{name} already marked present today.", "error"

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(csv_file, 'a') as f:
        f.write(f"{name},{time_now}\n")
    print(f"[LOGGED] {name} at {time_now}")
    return True, f"{name} logged successfully!", "success"

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    try:
        success, frame = cap.read()
        if not success:
            print("[ERROR] Could not read frame from webcam.")
            return redirect(url_for('index', msg="Could not capture frame", type="error"))

        name = recognize_face(frame)

        if not name or name.strip().lower() == "unknown":
            print("[INFO] Face not recognized.")
            return redirect(url_for('index', msg="Face not recognized", type="error"))

        was_logged, message, msg_type = log_attendance(name, CSV_FILE)
        return redirect(url_for('index', msg=message, type=msg_type))

    except Exception as e:
        print(f"[EXCEPTION] mark_attendance error: {e}")
        return redirect(url_for('index', msg="Internal server error", type="error"))

@app.route('/add_user', methods=['POST'])
def add_user_route():
    name = request.form.get('name')
    success, frame = cap.read()
    if name and success:
        if add_user(frame, name):
            return redirect(url_for('index', msg=f"{name} added!", type="success"))
        else:
            return redirect(url_for('index', msg="Error adding user", type="error"))
    return redirect(url_for('index', msg="Invalid input", type="error"))

@app.route('/logs')
def logs():
    with open(CSV_FILE, 'r') as f:
        lines = f.readlines()
    entries = [line.strip().split(',') for line in lines[1:]]
    return render_template("logs.html", entries=entries)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("[INFO] Shutdown requested from UI.")
    cap.release()
    cv2.destroyAllWindows()

    def kill():
        print("[INFO] Exiting app process...")
        os._exit(0)

    threading.Thread(target=kill).start()
    return "Server shutting down..."

def gen_preview():
    while True:
        success, frame = cap.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/preview_feed')
def preview_feed():
    return Response(gen_preview(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/goodbye')
def goodbye():
    shutdown_script = '''
    <script>
        fetch("/shutdown", { method: "POST" });
        setTimeout(() => {
            document.getElementById("msg").innerText = "✅ Server has been shut down. You may close this tab.";
        }, 1500);
    </script>
    '''
    return f"""
    <h2 id="msg" style='text-align:center;margin-top:50px;'>Shutting down server...</h2>
    {shutdown_script}
    """

if __name__ == "__main__":
    app.run(debug=True)
