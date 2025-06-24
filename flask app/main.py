import cv2
from face_utils import load_model, recognize_face, add_user
from utils import ensure_dirs, log_attendance
from config import DB_PATH, CSV_FILE


attendance_log = {}
ensure_dirs(DB_PATH, CSV_FILE)
model = load_model()

cap = cv2.VideoCapture(0)
print("[INFO] Press 'n' to add user, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    name = recognize_face(frame)
    color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
    text = f"{name} logged!" if name != "Unknown" else "Face not recognized"

    if name != "Unknown":
        log_attendance(name, CSV_FILE, attendance_log)

    cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Face Attendance", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key == ord('n'):
        uname = input("Enter name: ").strip().lower()
        if uname:
            add_user(frame, uname)

cap.release()
cv2.destroyAllWindows()
