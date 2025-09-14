import os
import pickle
import numpy as np
from deepface import DeepFace

def train_new_student(student_folder, encodings_path="../encodings_arcface.pkl", model_name="ArcFace"):
    if not os.path.isdir(student_folder):
        print(f"❌ Folder not found: {student_folder}")
        return

    try:
        name, student_id = os.path.basename(student_folder).rsplit("_", 1)
        student_id = str(student_id).zfill(3)
    except ValueError:
        print(f"⚠️ Invalid folder name {student_folder}. Expected format: Name_ID")
        return

    if os.path.exists(encodings_path):
        with open(encodings_path, "rb") as f:
            data = pickle.load(f)
    else:
        data = {"encodings": [], "names": [], "ids": []}

    known_encodings = list(data["encodings"])
    known_names = list(data["names"])
    known_ids = list(data["ids"])

    cleaned_encodings, cleaned_names, cleaned_ids = [], [], []
    for enc, n, sid in zip(known_encodings, known_names, known_ids):
        if sid != student_id:
            cleaned_encodings.append(enc)
            cleaned_names.append(n)
            cleaned_ids.append(sid)

    processed, failed = 0, 0
    for filename in os.listdir(student_folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(student_folder, filename)
        try:
            embedding = DeepFace.represent(
                img_path=img_path,
                model_name=model_name,
                enforce_detection=False
            )[0]["embedding"]

            cleaned_encodings.append(np.array(embedding, dtype=np.float32))
            cleaned_names.append(name)
            cleaned_ids.append(student_id)
            processed += 1
        except Exception as e:
            print(f"⚠️ Error processing {img_path}: {e}")
            failed += 1

    data = {"encodings": cleaned_encodings, "names": cleaned_names, "ids": cleaned_ids}
    with open(encodings_path, "wb") as f:
        pickle.dump(data, f)

    print(f"✅ Student {name} ({student_id}) added/updated in {encodings_path}")
    print(f"   Images processed: {processed}, failed: {failed}")
    