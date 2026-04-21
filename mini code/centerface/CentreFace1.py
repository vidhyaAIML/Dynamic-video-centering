import cv2

import mediapipe as mp


# Initialize face detection and drawing modules

mp_face_detection = mp.face_detection
mp_drawing = mp.drawing_utils


# Capture video from the webcam
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
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
