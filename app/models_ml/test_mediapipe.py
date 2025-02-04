import cv2
import mediapipe as mp
import numpy as np
from utils.mp_utils import *

# Initialisation de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class MpPose:
    def __init__(self, video_path: str, output_path: str):
        self.path = video_path
        self.output_path = output_path

    def predict(self, genou: int):
        # Initialisation des variables
        flex_gauche = float('inf')
        flex_droit = float('inf')
        ext_gauche = float('-inf')
        ext_droit = float('-inf')

        # Ouvrir la vidéo
        cap = cv2.VideoCapture(self.path)
        if not cap.isOpened():
            print(f"Erreur : Impossible d'ouvrir la vidéo à l'emplacement {self.path}")
            return None

        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=2
        ) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Fin de la vidéo ou erreur de lecture.")
                    break

                # Traitement de l'image
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Détection des landmarks de pose
                results = pose.process(image)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    genou_droit, genou_gauche = get_angle(landmarks, mp_pose)

                    # Mettre à jour les valeurs pour le genou droit
                    if genou == 1 and genou_droit is not None:
                        if genou_droit > ext_droit:
                            ext_droit = genou_droit
                        if genou_droit < flex_droit:
                            flex_droit = genou_droit

                    # Mettre à jour les valeurs pour le genou gauche
                    if genou == 0 and genou_gauche is not None:
                        if genou_gauche > ext_gauche:
                            ext_gauche = genou_gauche
                        if genou_gauche < flex_gauche:
                            flex_gauche = genou_gauche

        # Libérer les ressources
        cap.release()

        # Retourner les résultats
        if genou == 1:
            return {'Flexion': flex_droit, 'Extension': ext_droit}
        elif genou == 0:
            return {'Flexion': flex_gauche, 'Extension': ext_gauche}
        else:
            return None