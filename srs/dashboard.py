import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image

BASE_DIR = Path(".").resolve()
DATASET_DIR = BASE_DIR / "dataset"
ATTENDANCE_DIR = BASE_DIR / "attendance"

def load_all_attendance():
    files = sorted(ATTENDANCE_DIR.glob("*.csv"), reverse=True)
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, dtype=str) 
            dfs.append(df)
        except Exception:
            continue
    if dfs:
        all_df = pd.concat(dfs, ignore_index=True)
        return all_df
    return pd.DataFrame(columns=["Date", "Name", "ID", "In-Time", "Out-Time"])

def get_registered_students():
    students = []
    for folder in DATASET_DIR.iterdir():
        if folder.is_dir():
            try:
                name, sid = folder.name.rsplit("_", 1)
                students.append((name, str(sid).zfill(3), folder)) 
            except ValueError:
                continue
    return students

def get_student_photo(folder_path):
    for img_file in folder_path.iterdir():
        if img_file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            return Image.open(img_file)
    return None

def render_dashboard():
    st.title("Attendance Dashboard")

    df = load_all_attendance()
    if df.empty:
        st.info("No attendance records found yet.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    today = datetime.now().strftime("%Y-%m-%d")
    today_df = df[df["Date"].dt.strftime("%Y-%m-%d") == today]

    st.subheader("Today's Attendance")
    if today_df.empty:
        st.info("No records for today yet.")
    else:
        st.dataframe(today_df)
        total_students = today_df.shape[0]
        present = (today_df["In-Time"] != "Absent").sum()
        absent = total_students - present
        st.write(f"Present: {present} | Absent: {absent} | Total: {total_students}")

    st.subheader("View Previous Records")
    available_dates = sorted(df["Date"].dt.strftime("%Y-%m-%d").unique(), reverse=True)

    if len(available_dates) > 1:
        selected_date = st.selectbox(
            "Select a date to view attendance", 
            [d for d in available_dates if d != today]
        )
        prev_df = df[df["Date"].dt.strftime("%Y-%m-%d") == selected_date]
        st.dataframe(prev_df)
        total_students = prev_df.shape[0]
        present = (prev_df["In-Time"] != "Absent").sum()
        absent = total_students - present
        st.write(f"Present: {present} | Absent: {absent} | Total: {total_students}")
    else:
        st.info("No previous attendance records found.")

    st.subheader("Attendance Count per Student (Overall)")
    present_df = df[df["In-Time"] != "Absent"]
    counts = present_df.groupby("Name").size().reset_index(name="Present Days")
    st.bar_chart(counts.set_index("Name"))

    st.subheader("Attendance Share (Overall)")
    if not counts.empty:
        fig, ax = plt.subplots()
        counts.set_index("Name").plot.pie(y="Present Days", ax=ax, autopct='%1.1f%%', legend=False)
        st.pyplot(fig)

    st.subheader("Student Profile")
    students = get_registered_students()
    if students:
        student_options = {f"{name} ({sid})": (name, sid, folder) for name, sid, folder in students}
        selected = st.selectbox("Select a student", list(student_options.keys()))
        name, sid, folder = student_options[selected]

        photo = get_student_photo(folder)
        if photo:
            st.image(photo, caption=f"{name} ({sid})", width=200)

        student_history = df[df["ID"].astype(str).str.zfill(3) == str(sid).zfill(3)]
        if student_history.empty:
            st.info("No records for this student yet.")
        else:
            st.write(f"### Attendance History for {name} ({sid})")
            st.dataframe(student_history)
            total_days = len(student_history["Date"].dt.date.unique())
            present_days = (student_history["In-Time"] != "Absent").sum()
            absent_days = total_days - present_days
            st.write(f"Present: {present_days} days")
            st.write(f"Absent: {absent_days} days")
            csv = student_history.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Attendance CSV",
                data=csv,
                file_name=f"attendance_{name}_{sid}.csv",
                mime="text/csv"
            )
