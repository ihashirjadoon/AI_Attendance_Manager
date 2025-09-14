import streamlit as st
from pathlib import Path
from recognize import recognize_faces
from dashboard import render_dashboard
from register import register

BASE_DIR = Path(".").resolve()
DATASET_DIR = BASE_DIR / "dataset"
ATTENDANCE_DIR = BASE_DIR / "attendance"
ENCODINGS_PATH = BASE_DIR / "../encodings_arcface.pkl"

st.set_page_config(page_title="AI Attendance Manager", layout="wide")

DATASET_DIR.mkdir(exist_ok=True)
ATTENDANCE_DIR.mkdir(exist_ok=True)

page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Register Student",
    "Run Recognition"
])

if page == "Dashboard":
    render_dashboard()

elif page == "Register Student":
    register()

elif page == "Run Recognition":
    st.title("📷 Real-Time Recognition")
    st.write("This will start the webcam and log attendance into the `attendance/` folder.")

    camera_choice = st.selectbox(
        "Select Camera",
        options=[("Front Camera", 0), ("Rear Camera", 1)],
        format_func=lambda x: x[0]
    )
    selected_camera = camera_choice[1]

    if st.button("Start Recognition"):
        st.info("A new window will open. Press 'q' to stop recognition.")
        recognize_faces(camera_index=selected_camera)
        st.success("Recognition session ended. Attendance updated.")

st.markdown("---")
st.caption("AI Attendance Manager | Built for Techwiz 6")
