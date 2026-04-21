import cv2
import threading
from tkinter import Tk, Button, Label, messagebox
import winsound

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

        # Load OpenCV face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

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
        messagebox.showwarning("Alert", "No face detected!")
        winsound.Beep(1000, 500)

    def run_detection(self):
        cap = cv2.VideoCapture(0)

        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                self.alert_shown = False

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Zoomed face view
                    face_crop = frame[y:y+h, x:x+w]
                    if face_crop.size != 0:
                        zoomed = cv2.resize(face_crop, (frame.shape[1], frame.shape[0]))
                        cv2.imshow("Centre Face", zoomed)

            else:
                cv2.putText(frame, "No face detected", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if not self.alert_shown:
                    self.alert_shown = True
                    self.show_alert()

            cv2.imshow("Normal View", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.running = False


if __name__ == "__main__":
    root = Tk()
    app = FaceDetectionApp(root)
    root.mainloop()