import cv2
import os
from datetime import datetime
import time

def capture_dataset(name, student_id, dataset_path="dataset", num_images=100, camera_index=1, delay=0.2):
    folder_name = f"{name}_{student_id}"
    save_path = os.path.join(dataset_path, folder_name)
    os.makedirs(save_path, exist_ok=True)

    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return

    print("⏳ Warming up camera...")
    for _ in range(25):
        cap.read()

    print(f"📷 Ready to capture {num_images} grayscale images for {name} (ID: {student_id}).")
    print(" ▶ Press 's' to start | 'g' to pause/resume | 'q' to quit")

    count = 0
    capturing = False
    paused = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to capture frame")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        display_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

        status_text = f"Image {count}/{num_images}" if capturing else "Press 's' to start"
        cv2.putText(display_frame, status_text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if paused:
            cv2.putText(display_frame, "⏸️ Paused - Press 'g' to resume", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Capture Dataset", display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and not capturing:
            capturing = True
            paused = False
            print("▶️ Capture started...")

        elif key == ord('g') and capturing:
            paused = not paused
            state = "resumed" if not paused else "paused"
            print(f"⏸️ Capture {state} (glasses switch)")

        elif key == ord('q'):
            print("⏹️ Capture stopped early by user.")
            break

        if capturing and not paused and count < num_images:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"{name}_{student_id}_{timestamp}.jpg"
            filepath = os.path.join(save_path, filename)
            cv2.imwrite(filepath, gray_frame)
            print(f"✅ Saved {filepath}")
            count += 1
            time.sleep(delay)

        if count >= num_images:
            print(f"🎉 Finished capturing {count} grayscale images for {name} (ID: {student_id}).")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"📂 Images saved in {save_path}")

if __name__ == "__main__":
    capture_dataset("Test", "999", num_images=20, delay=0.2)
