import cv2
import mediapipe as mp
import threading
from tkinter import Tk, Button, Label, messagebox
import winsound

# Initialize face detection and drawing modules
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")

        self.start_button = Button(root, text="Start Detection", command=self.start_detection)
        self.start_button.pack(pady=10)

        self.stop_button = Button(root, text="Stop Detection", command=self.stop_detection, state="disabled")
        self.stop_button.pack(pady=10)

        self.status_label = Label(root, text="Status: Idle", fg="blue")
        self.status_label.pack(pady=10)

        self.running = False
        self.thread = None

    def start_detection(self):
        self.running = True
        self.status_label.config(text="Status: Running", fg="green")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.thread = threading.Thread(target=self.run_detection)
        self.thread.start()

    def stop_detection(self):
        self.running = False
        self.status_label.config(text="Status: Stopping", fg="orange")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        if self.thread:
            self.thread.join()
        self.status_label.config(text="Status: Idle", fg="blue")

    def show_alert(self):
        # Show a dialog box and play a sound alert
        messagebox.showwarning("Alert", "No person detected!")
        winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 milliseconds

    def run_detection(self):
        cap = cv2.VideoCapture(0)
        with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
            while self.running and cap.isOpened():
                success, frame = cap.read()
                if not success:
                    continue

                height, width, _ = frame.shape
                frame = cv2.flip(frame, 1)

                # Convert the frame to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(frame_rgb)

                if results.detections:
                    for detection in results.detections:
                        # Extract bounding box
                        bboxC = detection.location_data.relative_bounding_box
                        x_min = int(bboxC.xmin * width)
                        y_min = int(bboxC.ymin * height)
                        bbox_width = int(bboxC.width * width)
                        bbox_height = int(bboxC.height * height)

                        # Add margins around the face
                        margin_x = int(bbox_width * 0.5)
                        margin_y = int(bbox_height * 0.5)

                        x_min = max(0, x_min - margin_x)
                        y_min = max(0, y_min - margin_y)
                        x_max = min(width, x_min + bbox_width + 2 * margin_x)
                        y_max = min(height, y_min + bbox_height + 2 * margin_y)

                        # Crop and resize the face region
                        cropped_face = frame[y_min:y_max, x_min:x_max]
                        resized_face = cv2.resize(cropped_face, (width, height))

                        cv2.imshow('Centre Face', resized_face)

                else:
                    # Display a prompt if no person is detected
                    cv2.putText(frame, 'No person detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    self.show_alert()

                # Display the original frame with bounding box
                frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                if results.detections:
                    for detection in results.detections:
                        mp_drawing.draw_detection(frame, detection)

                cv2.imshow('Normal View', frame)

                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()
        cv2.destroyAllWindows()
        self.running = False

if __name__ == "__main__":
    root = Tk()
    app = FaceDetectionApp(root)
    root.mainloop()