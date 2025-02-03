import os
import cv2
from ultralytics import YOLO
import numpy as np
from utils.yolo_utils import *

class YoloPose:
    def __init__(self, video_path: str, output_path: str):
        self.path = video_path
        self.output_path = output_path
        self.model = YOLO(os.path.join(os.path.dirname(__file__), "yolo11x-pose.pt"))

    def predict(self):
        flex_gauche = float('inf')
        flex_droit = float('inf')
        ext_gauche = float('-inf')
        ext_droit = float('-inf')
        cap = cv2.VideoCapture(self.path)
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            # Convertir le cadre au format RGB pour YOLO
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Effectuer la détection
            results = self.model(frame_rgb, conf=0.5)  # Ajuster le seuil de confiance si nécessaire
            result = results[0]
            keypoints = result.keypoints
            
            if keypoints is not None and keypoints.xy.shape[1] > 16:
                right_hip_coords = keypoints.xy[0, 12]  # Access coordinates for right hip (index 12)
                left_hip_coords = keypoints.xy[0, 11]  # Access coordinates for left hip (index 11)
                right_knee_coords = keypoints.xy[0, 14]  # Access coordinates for right knee (index 14)
                left_knee_coords = keypoints.xy[0, 13]  # Access coordinates for left knee (index 13)
                left_ankle_coords = keypoints.xy[0, 15]  # Access coordinates for left ankle (index 15)
                right_ankle_coords = keypoints.xy[0, 16]  # Access coordinates for right ankle (index 16)

                 # Calculer les angles de flexion des genoux
                genou_droit = get_angle(right_hip_coords, right_knee_coords, right_ankle_coords)
                genou_gauche = get_angle(left_hip_coords, left_knee_coords, left_ankle_coords)

                if genou_droit > ext_droit:
                    ext_droit = genou_droit
                if genou_gauche > ext_gauche:
                    ext_gauche = genou_gauche
                if genou_droit < flex_droit:
                    flex_droit = genou_droit
                if genou_gauche < flex_gauche:
                    flex_gauche = genou_gauche

        with open(self.output_path, 'w') as f:
            f.write(f"Flexion max droit: {flex_droit}\n")
            f.write(f"Flexion max gauche: {flex_gauche}\n")
            f.write(f"Extension max droit: {ext_droit}\n")
            f.write(f"Extension max gauche: {ext_gauche}\n")
        cap.release()