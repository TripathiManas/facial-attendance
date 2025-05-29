import cv2
import os
from datetime import datetime
from deepface import DeepFace
import uuid

# --- Config ---
db_path = "data/known_faces"
model_name = "Facenet"
csv_file = "attendance.csv"

# --- Setup ---
os.makedirs(db_path, exist_ok=True)
if not os.path.exists(csv_file):
    with open(csv_file, 'w') as f:
        f.write("Name,Time\n")

# --- Runtime state ---
attendance_log = {}
known_embeddings = []
known_names = []

# --- Add new user function ---
def add_new_user(image, name, model_name="Facenet"):
    filename = f"{name}_{uuid.uuid4().hex[:6]}.png"
    save_path = os.path.join(db_path, filename)
    cv2.imwrite(save_path, image)
    print(f"[SAVED] Face image saved as {filename}")

    try:
        embedding = DeepFace.represent(img_path=save_path, model_name=model_name, enforce_detection=True)[0]["embedding"]
        known_embeddings.append(embedding)
        known_names.append(name)
        print(f"[INFO] {name} added to known embeddings.")
    except Exception as e:
        print(f"[ERROR] Could not add user: {e}")

# --- Start ---
print("[INFO] Starting DeepFace model...")
model = DeepFace.build_model(model_name)
print("[INFO] Model loaded.")

# --- Check for known faces ---
valid_extensions = ('.jpg', '.jpeg', '.png')
valid_images = [f for f in os.listdir(db_path) if f.lower().endswith(valid_extensions)]

if not valid_images:
    print("[INFO] No known face images found in the database.")
    print("Press 'n' to add the first user.")
    enable_recognition = False
else:
    enable_recognition = True

# --- Start webcam and process frames ---
cap = cv2.VideoCapture(0)
print("[INFO] Press 'n' to add user, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        name = "Unknown"
        if enable_recognition:
            results = DeepFace.find(
                img_path=frame,
                db_path=db_path,
                model_name=model_name,
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )

            if len(results) > 0 and len(results[0]) > 0:
                match = results[0].iloc[0]
                identity_path = match['identity']
                name = os.path.splitext(os.path.basename(identity_path))[0].split("_")[0]
                distance = match['distance']
                threshold = 0.4  # for Facenet

                if distance <= threshold:
                    if name not in attendance_log:
                        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        attendance_log[name] = time_now
                        print(f"[LOGGED] {name} at {time_now}")
                        with open(csv_file, 'a') as f:
                            f.write(f"{name},{time_now}\n")
                else:
                    name = "Unknown"

            # Display result
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            text = f"{name} logged successfully!" if name != "Unknown" else "No Face Recognised"

        else:
            color = (255, 255, 0)
            text = "Press 'n' to add your face"

        cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    except Exception as e:
        print(f"[ERROR] {e}")

    cv2.imshow("Attendance System", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

    elif key == ord('n'):
        print("[INFO] Attempting to add new user...")
        name = input("[INPUT] Enter name for new user: ").strip().lower()

        if name:
            try:
                faces = DeepFace.extract_faces(img_path=frame, detector_backend='opencv', enforce_detection=True)
                if faces:
                    face_img = faces[0]["face"]
                    filename = f"{name}_{uuid.uuid4().hex[:6]}.png"
                    save_path = os.path.join(db_path, filename)
                    cv2.imwrite(save_path, (face_img * 255).astype("uint8"))
                    print(f"[SAVED] Face image saved as {filename}")

                    embedding = DeepFace.represent(img_path=save_path, model_name=model_name)[0]["embedding"]
                    known_embeddings.append(embedding)
                    known_names.append(name)
                    print(f"[INFO] {name} added to known embeddings.")
                    enable_recognition = True  # Enable recognition after first user is added
                else:
                    print("[WARNING] No face detected.")
            except Exception as e:
                print(f"[ERROR] Could not add user: {e}")
        else:
            print("[WARNING] Name cannot be empty.")

cap.release()
cv2.destroyAllWindows()
print("[INFO] System exited.")
