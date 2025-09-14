import streamlit as st
from pathlib import Path
from train_new_student import train_new_student
from capture_dataset import capture_dataset

DATASET_PATH = Path("dataset")
ENCODINGS_PATH = "../encodings_arcface.pkl"

def get_next_student_id():
    max_id = 0
    for folder in DATASET_PATH.iterdir():
        if folder.is_dir():
            try:
                _, sid = folder.name.rsplit("_", 1)
                sid = int(sid)
                if sid > max_id:
                    max_id = sid
            except ValueError:
                continue
    return str(max_id + 1).zfill(3)

def save_uploaded_images(folder, uploaded_files):
    folder.mkdir(parents=True, exist_ok=True)
    for file in uploaded_files:
        file_path = folder / file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
    return folder

def register():
    st.title("📝 Student Registration")
    student_name = st.text_input("Enter Student Name (e.g., Iman)")

    if not student_name.strip():
        st.warning("⚠️ Please enter a valid name before continuing.")
        return

    mode = st.radio("Choose Registration Method", ["Upload Images", "Capture via Webcam"])
    student_id = get_next_student_id()
    folder_name = f"{student_name.strip()}_{student_id}"
    folder = DATASET_PATH / folder_name

    if mode == "Upload Images":
        uploaded_files = st.file_uploader(
            "Upload Student Images", type=["jpg", "png"], accept_multiple_files=True
        )
        if uploaded_files and st.button("Register Student"):
            save_uploaded_images(folder, uploaded_files)
            st.success(f"✅ Student **{student_name}** registered as **{folder_name}** "
                       f"with {len(uploaded_files)} images.")
            train_new_student(str(folder), encodings_path=ENCODINGS_PATH)
            st.info("🔄 Encodings updated successfully! You can now recognize this student.")

    elif mode == "Capture via Webcam":
        num_images = st.number_input("Number of images to capture", min_value=20, max_value=200, value=100, step=10)
        camera_choice = st.selectbox(
            "Select Camera", options=[("Front Camera", 0), ("Rear Camera", 1)],
            format_func=lambda x: x[0]
        )
        selected_camera = camera_choice[1]

        if st.button("Start Capturing"):
            capture_dataset(
                student_name.strip(),
                student_id,
                dataset_path=str(DATASET_PATH),
                num_images=num_images,
                camera_index=selected_camera,
                delay=0.2
            )
            st.success(f"✅ Student **{student_name}** registered as **{folder_name}** "
                       f"with {num_images} images.")
            train_new_student(str(folder), encodings_path=ENCODINGS_PATH)
            st.info("🔄 Encodings updated successfully! You can now recognize this student.")

if __name__ == "__main__":
    register()
