import pdfkit
import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from fastapi import Depends, HTTPException
from utils.dependencies import get_patient_id, get_consultation_id
from services.patient_service import PatientService
from services.consultation_service import ConsultationService
from services.kine_service import KineService

print("Current working directory:", os.getcwd())

# Configuration de pdfkit
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
patientService = PatientService()
consultationService = ConsultationService()
kineService = KineService()

async def generate_pdf(
    patient_id: str = Depends(get_patient_id),
    consultation_id: str = Depends(get_consultation_id),          
    output_path: str = "bilan_kine.pdf"
):
    base_dir = os.path.abspath("app/utils/")
    
    try:
        # Charger le template HTML
        env = Environment(loader=FileSystemLoader(base_dir))
        template = env.get_template('bdk.html')
    except TemplateNotFound:
        raise HTTPException(status_code=500, detail="Template HTML non trouvé")
    
    try:
        # Récupérer les données de la consultation
        consultation_data = await consultationService.read_one(consultation_id)
        output_path = "/code/app/bdk/" + consultation_data["bdk"]
        if not consultation_data:
            raise HTTPException(status_code=404, detail="Consultation non trouvée")
        
        # Récupérer les données du patient
        patient_data = await patientService.read_one(patient_id)
        if not patient_data:
            raise HTTPException(status_code=404, detail="Patient non trouvé")
        
        # Récupérer les données du kiné
        kine_data = await kineService.read_one(patient_data["kineid"])
        if not kine_data:
            raise HTTPException(status_code=404, detail="Kiné non trouvé")
        
        # Combiner et trier les données dans le dictionnaire data
        data = {
            "date_bilan": consultation_data["date_consultation"],
            "patient_nom": patient_data["nom"],
            "patient_dob": patient_data["date_naissance"],
            "kine_nom": kine_data["nom"] + " " + kine_data["prenom"],
            "kine_adresse": kine_data["adresse"]["rue"],
            "kine_ville": kine_data["adresse"]["ville"] + ", " + kine_data["adresse"]["code_postal"],
            "nb_seances": consultation_data["nb_seances"],
            "frequence_seances": consultation_data["frequence_seances"],
            "douleur_duree": consultation_data["douleur_duree"],
            "douleur_niveau": consultation_data["douleur_niveau"],
            "flexion": {"active": 0.0, "passive": consultation_data["flexion"]["passive"]},
            "extension": {"active": 0.0, "passive": consultation_data["extension"]["passive"]},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données: {str(e)}")
    
    try:
        # Rendre le template avec les données
        html_content = template.render(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du rendu du template: {str(e)}")
    
    try:
        # Générer le PDF
        pdfkit.from_string(html_content, output_path, configuration=config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du PDF: {str(e)}")
    
    return output_path