# config.py

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "known_faces")
CSV_FILE = os.path.join(BASE_DIR, "data", "attendance.csv")

# Model config
MODEL_NAME = "Facenet"
THRESHOLD = 0.4
