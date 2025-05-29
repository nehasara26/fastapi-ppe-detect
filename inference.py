import cv2
from ultralytics import YOLO
import time

model = YOLO("C:/NEHA/INTERNSHIP PROJECT/ppe-detection/best.pt")

def run_inference(video_path, output_path="static/output.mp4"):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)
        annotated_frame = results[0].plot()

        if out is None:
            h, w, _ = annotated_frame.shape
            out = cv2.VideoWriter(output_path, fourcc, 20.0, (w, h))

        out.write(annotated_frame)

    cap.release()
    if out:
        out.release()