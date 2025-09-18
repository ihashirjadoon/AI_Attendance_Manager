# AI Attendance Manager

> # **Important Note about the Demonstration Video**  
> The video was recorded in one continuous Zoom session. After the first part (ending at **4:15**), I stepped away to bring in students for the recognition demonstration, assuming the recording was paused. However, Zoom continued recording during this idle period.  
> For convenience, please use the guide below:  
> - **0:00 – 4:15** → Project introduction and walkthrough  
> - **4:15 – 16:25** → Idle section (can be skipped)  
> - **16:25 – 17:45** → Main face recognition demonstration  
>   
> We recommend skipping directly to **16:25** to see the core functionality in action.  

AI Attendance Manager is a face-recognition-based attendance system built with **Streamlit**, **OpenCV**, and **DeepFace**.  
It allows you to register students, recognize faces in real-time, and automatically log attendance.

**Developed by MSG Strickers for Techwiz 6**

---

## Features
-  Register Students (via webcam or by uploading images)  
-  Real-Time Recognition with ArcFace embeddings  
-  Dashboard to view daily and overall attendance  
-  Attendance saved automatically in CSV files  

---

## Installation

 **Python version requirement:** This project has been tested with **Python 3.10.11**.  
Using a different version may cause compatibility issues with some libraries.

1. **Clone this repository**
   ```bash
   git clone https://github.com/ihashirjadoon/AI_ATTENDANCE_MANAGER.git
   cd AI_ATTENDANCE_MANAGER
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate    # On Windows
   source venv/bin/activate # On Linux/Mac
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the Streamlit app:
```bash
streamlit run srs/app.py
```

The sidebar will show three options:

1. **Dashboard** – View today’s attendance, past records, and student profiles  
2. **Register Student** – Add yourself or others (upload images or use webcam)  
3. **Run Recognition** – Start the webcam and mark attendance automatically  

 Attendance records will be stored inside the `attendance/` folder as daily CSV files.

---

## Project Structure

```
AI_ATTENDANCE_MANAGER/
├── attendance/        # Auto-generated attendance logs (CSV)
├── dataset/           # Student images (auto-created when registering)
├── documentation/     # Local documentation (ignored in Git)
├── notebooks/         # Training and evaluation notebooks
├── srs/               # Core source code
│   ├── app.py         # Main entry point
│   ├── dashboard.py   # Attendance dashboard
│   ├── recognize.py   # Real-time recognition
│   ├── register.py    # Student registration
│   └── ...            # Other utilities
├── requirements.txt   # Dependencies
└── README.md          # Project info
```

---

## Notes
- A new CSV file is created in the `attendance/` folder every day.  
- Student images are stored under the `dataset/` folder.  
- Encodings are stored in `.pkl` files so recognition works across sessions.  

---

## Credits
Developed by **MSG Strickers** for **Techwiz 6**.
