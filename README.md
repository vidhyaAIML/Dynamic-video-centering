# Dynamic Video Centering App

This project is a real-time face detection application that uses a webcam to detect faces and dynamically center them on the screen. It also provides alerts when no person is detected.

The system is built using Python with a GUI interface and supports live video processing.

---

## 🚀 Features

* 🎥 Real-time face detection using webcam
* 🎯 Dynamic face centering (zoomed face view)
* 🖥️ GUI with Start/Stop controls
* ⚠️ Alert (popup + sound) when no face is detected
* 📦 Bounding box visualization
* ⚡ Multithreading for smooth performance

---

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* Tkinter (GUI)
* NumPy

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the application

```bash
python my_face_app.py
```

---

## ⚙️ How It Works

1. Webcam captures live video frames
2. Each frame is converted from BGR to RGB
3. MediaPipe processes the frame for face detection
4. If a face is detected:

   * Bounding box is calculated
   * Face region is cropped
   * Face is resized and displayed in **Centre Face window**
5. If no face is detected:

   * Warning message is displayed
   * Sound alert is triggered
6. Original video is shown in **Normal View window**

---



---

## ⚠️ Requirements

* Python 3.9 (recommended for MediaPipe compatibility)
* Webcam access

---

## ⚠️ Notes

* Close other apps using the camera (Zoom, Teams, etc.)
* Press **ESC** to exit camera windows
* Works best under good lighting conditions

---

## 🎯 Use Cases

* Smart video conferencing
* Automatic camera framing
* Surveillance systems
* Human-computer interaction
