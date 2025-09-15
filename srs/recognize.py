import cv2
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
import pandas as pd
from deepface import DeepFace

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR.parent / "dataset"
ATTENDANCE_DIR = BASE_DIR.parent / "attendance"
ATTENDANCE_DIR.mkdir(exist_ok=True)

ENCODINGS_PATH = BASE_DIR / "../encodings_arcface.pkl"
with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

if "embeddings" in data:
    known_embeddings = np.array(data["embeddings"])
else:
    known_embeddings = np.array(data["encodings"])
known_names = data["names"]
known_ids = [str(i).zfill(3) for i in data["ids"]]

today = datetime.now().strftime("%Y-%m-%d")
attendance_file = ATTENDANCE_DIR / f"attendance_{today}.csv"


def initialize_attendance():
    if attendance_file.exists():
        try:
            df = pd.read_csv(attendance_file)
            if df.empty:  # file exists but has no rows
                raise pd.errors.EmptyDataError
            return df
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            # reset file if empty or corrupted
            attendance_file.unlink(missing_ok=True)
    # rebuild attendance file
    records = []
    for folder in DATASET_DIR.iterdir():
        if folder.is_dir():
            try:
                name, sid = folder.name.rsplit("_", 1)
                sid = str(sid).zfill(3)
                records.append({
                    "Date": today,
                    "Name": name,
                    "ID": sid,
                    "In-Time": "Absent",
                    "Out-Time": "Absent"
                })
            except ValueError:
                continue
    df = pd.DataFrame(records)
    df.to_csv(attendance_file, index=False)
    return df


def save_attendance(df):
    df.to_csv(attendance_file, index=False)


def get_facial_area(det):
    fa = det.get("facial_area", None)
    if fa is None:
        return None
    if isinstance(fa, dict):
        return fa["x"], fa["y"], fa["w"], fa["h"]
    if isinstance(fa, (list, tuple)) and len(fa) == 4:
        return fa
    return None


def recognize_faces(camera_index=0):
    df = initialize_attendance()
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        try:
            detections = DeepFace.extract_faces(frame, detector_backend="opencv")
        except Exception:
            detections = []
        for det in detections:
            coords = get_facial_area(det)
            if coords is None:
                continue
            x, y, w, h = coords
            face_crop = frame[y:y+h, x:x+w]
            try:
                emb = DeepFace.represent(face_crop, model_name="ArcFace", enforce_detection=False)[0]["embedding"]
                emb = np.array(emb, dtype=np.float32)
                sims = np.dot(known_embeddings, emb) / (np.linalg.norm(known_embeddings, axis=1) * np.linalg.norm(emb) + 1e-6)
                idx = np.argmax(sims)
                if sims[idx] > 0.45:
                    name, sid = known_names[idx], known_ids[idx]
                    mask = df["ID"].astype(str).str.zfill(3) == sid
                    if mask.any():
                        row = df.loc[mask].iloc[0]
                        if row["In-Time"] == "Absent":
                            df.loc[mask, "In-Time"] = datetime.now().strftime("%H:%M:%S")
                        else:
                            df.loc[mask, "Out-Time"] = datetime.now().strftime("%H:%M:%S")
                        save_attendance(df)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{name} ({sid})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            except Exception:
                continue
        cv2.imshow("Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    save_attendance(df)


if __name__ == "__main__":
    recognize_faces()
