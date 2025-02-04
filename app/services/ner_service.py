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
    for d in liste_dicts_uniques:
        # Si la clé existe déjà, on ajoute la valeur à une liste
        for key, value in d.items():
            if key in dictionnaire_final:
                if isinstance(dictionnaire_final[key], list):
                    dictionnaire_final[key].append(value)
                else:
                    dictionnaire_final[key] = [dictionnaire_final[key], value]
            else:
                dictionnaire_final[key] = value
    return dictionnaire_final