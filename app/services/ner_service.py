# services.py
from gliner import GLiNER

model_name = "almanach/camembert-bio-gliner-v0.1"
model = GLiNER.from_pretrained(model_name)

def extraction(text_kine: str) -> str:
    labels = ["personne", "Date de naissance", "Numéro de téléphone", "Email", "Adresse", "Code postal", "Ville", "Pays", "Numéro de sécurité social", "Taille", "Poids", "Latéralité", "Maladie","Symptômes", "Profession", "Lieu de travail", "Sport et loisirs"]
    entities = model.predict_entities(text_kine, labels, threshold=0.5, flat_ner=True)
    # Liste pour stocker toutes les entités
    entities_json = []

    # Parcourir chaque entité
    for entity in entities:
        # Ajouter chaque entité sous forme de dictionnaire à la liste
        entities_json.append({
            entity["label"]: entity["text"]
        })
    # Étape 1 : Éliminer les dictionnaires en double
    # Convertir chaque dictionnaire en tuple pour le rendre hachable
    liste_dicts_uniques = [dict(t) for t in {tuple(d.items()) for d in entities_json}]
    # Étape 2 : Fusionner les dictionnaires uniques en un seul
    dictionnaire_final = {}
    cles_a_concatener = ["personne", "Sport et loisirs"]
    cles_a_garder_en_liste = []  # On enlève "Sport et loisirs" d'ici

    for d in liste_dicts_uniques:
        for key, value in d.items():
            if key in dictionnaire_final:
                if isinstance(dictionnaire_final[key], list):
                    if key in cles_a_concatener:
                        # Si c'est une liste, on concatène les éléments et la nouvelle valeur
                        dictionnaire_final[key] = " ".join(dictionnaire_final[key] + ([value] if isinstance(value, str) else value))
                else:
                    if key in cles_a_concatener:
                        # Fusionner l'ancienne valeur (texte) avec la nouvelle
                        dictionnaire_final[key] = f"{dictionnaire_final[key]} {value}" if isinstance(value, str) else f"{dictionnaire_final[key]} {' '.join(value)}"
            else:
                if key in cles_a_concatener:
                    # Si c'est une liste, on la transforme directement en chaîne
                    dictionnaire_final[key] = " ".join(value) if isinstance(value, list) else value
                else:
                    dictionnaire_final[key] = value
    return dictionnaire_final