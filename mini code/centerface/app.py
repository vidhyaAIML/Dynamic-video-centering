import cv2
import mediapipe as mp
import threading
from tkinter import Tk, Button, Label, messagebox
import winsound

# NEW MediaPipe API
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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
        self.alert_shown = False

        # Load MediaPipe model
        base_options = python.BaseOptions(model_asset_path='face_detection_short_range.tflite')
        options = vision.FaceDetectorOptions(base_options=base_options)
        self.detector = vision.FaceDetector.create_from_options(options)

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

    def show_alert(self):
        messagebox.showwarning("Alert", "No person detected!")
        winsound.Beep(1000, 500)

    def run_detection(self):
        cap = cv2.VideoCapture(0)

        while self.running and cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            # Convert to MediaPipe format
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            # Detect faces
            detection_result = self.detector.detect(mp_image)

            if detection_result.detections:
                self.alert_shown = False

                for detection in detection_result.detections:
                    bbox = detection.bounding_box
                    x, y = bbox.origin_x, bbox.origin_y
                    w, h = bbox.width, bbox.height

                    # Draw rectangle
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Crop and zoom face
                    cropped_face = frame[y:y+h, x:x+w]
                    if cropped_face.size != 0:
                        resized_face = cv2.resize(cropped_face, (width, height))
                        cv2.imshow('Centre Face', resized_face)

            else:
                cv2.putText(frame, 'No person detected', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if not self.alert_shown:
                    self.alert_shown = True
                    self.show_alert()

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