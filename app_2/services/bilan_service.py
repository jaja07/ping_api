from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
print("Current working directory:", os.getcwd())

# Configuration de pdfkit
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

def generate_pdf(data: dict, output_path: str = "bilan_kine.pdf"):
    base_dir = os.path.abspath("app_2/resources/templates")
    # Charger le template HTML
    env = Environment(loader=FileSystemLoader(base_dir))
    template = env.get_template('bdk.html')
    
    # Rendre le template avec les données
    html_content = template.render(data)
    
    # Générer le PDF
    pdfkit.from_string(html_content, output_path, configuration=config)
    
    return output_path