from deepface import DeepFace
import os
import uuid
import cv2

from config import DB_PATH, MODEL_NAME, THRESHOLD

def load_model():
    print("[INFO] Loading model...")
    model = DeepFace.build_model(MODEL_NAME)
    print("[INFO] Model ready.")
    return model

def recognize_face(frame):
    try:
        results = DeepFace.find(img_path=frame, db_path=DB_PATH, model_name=MODEL_NAME, enforce_detection=False, detector_backend='opencv', silent=True)
        if results and len(results[0]) > 0:
            match = results[0].iloc[0]
            name = os.path.basename(match['identity']).split("_")[0]
            distance = match['distance']
            if distance <= THRESHOLD:
                return name
    except Exception as e:
        print(f"[ERROR-recognition] {e}")
    return "Unknown"

def add_user(frame, name):
    try:
        faces = DeepFace.extract_faces(img_path=frame, detector_backend='opencv', enforce_detection=True)
        if faces:
            face_img = faces[0]['face']
            filename = f"{name}_{uuid.uuid4().hex[:6]}.png"
            save_path = os.path.join(DB_PATH, filename)
            cv2.imwrite(save_path, (face_img * 255).astype("uint8"))
            print(f"[ADDED] {name} saved as {filename}")
            return True
    except Exception as e:
        print(f"[ERROR-add] {e}")
    return False
