import math
import cv2
import numpy as np

def calculate_3d_angle(p1, p2, p3):
    """
    Calcule l'angle formé par trois points en 3D.
    
    :param p1: Tuple (x, y, z) du premier point
    :param p2: Tuple (x, y, z) du point central
    :param p3: Tuple (x, y, z) du troisième point
    :return: Angle en degrés entre les segments p1-p2 et p3-p2
    """
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]])  # Vecteur p2 -> p1
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]])  # Vecteur p2 -> p3

    # Produit scalaire des deux vecteurs
    dot_product = np.dot(v1, v2)
    
    # Normes des vecteurs
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    # Calcul de l'angle en radians puis conversion en degrés
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))  # Évite les erreurs numériques
    
    return np.degrees(angle)  # Conversion en degrés


def get_3d_coordinates(landmark):
    return (
      landmark.x*100,
      landmark.y*100,
      landmark.z*100,
    )

def get_angle(landmarks, mp_pose):
    genou_droit = calculate_3d_angle(
      get_3d_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_HIP]),
      get_3d_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]),
      get_3d_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]),
    )
    genou_gauche = calculate_3d_angle(
      get_3d_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_HIP]),
      get_3d_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_KNEE]),
      get_3d_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]),
    )   
    return(genou_droit, genou_gauche)

def display(genou_droit, genou_gauche, image):
    # Affiche les mesures d'angles
    cv2.putText(image, f'Genou droit: {int(genou_droit)}', (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(image, f'Genou gauche: {int(genou_gauche)}', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    