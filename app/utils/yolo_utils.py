import numpy as np

def calculate_angle(p1, p2, p3):
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])  # Vecteur p2 -> p1
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])  # Vecteur p2 -> p3

    # Produit scalaire des deux vecteurs
    dot_product = np.dot(v1, v2)
    
    # Normes des vecteurs
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    # Calcul de l'angle en radians puis conversion en degrés
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))  # Évite les erreurs numériques
    
    return np.degrees(angle)  # Conversion en degrés


def get_coordinates(landmark):
    return (
      landmark[0],
      landmark[1]
    )

def get_angle(hip, knee, ankle):
    angle = calculate_angle(
      get_coordinates(hip),
      get_coordinates(knee),
      get_coordinates(ankle)
    ) 
    return(angle)



    