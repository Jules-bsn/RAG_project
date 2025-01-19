#pip install langchain openai PyPDF2 pdfplumber pandas
from dotenv import load_dotenv
import os
from pathlib import Path
import pdfplumber
import requests
import json

print(json.dumps({"test": "success"}))

# Charge les variables d'environnement depuis le fichier .env
env_path = Path('/Users/julesbesson/Documents/Projet_EY/Projet_EY/RAG/.env')  # Fichier .env est dans le dossier parent
load_dotenv(dotenv_path=env_path)

# Accéder à la variable d'environnement
base_url = os.getenv("BASE_URL")
auth_user = os.getenv("AUTH_USER")
auth_password = os.getenv("AUTH_PASSWORD")
auth = (auth_user, auth_password)

login_url = base_url + "/login"

response = requests.post(login_url, auth = auth)
print(f"Reponse : {response.content}")

token= response.json().get('token')
print(token)

headers = {'Authorization': token}
print(headers)

def extract_text_from_pdf(pdf_path):
    """
    Extrait le texte brut d'un fichier PDF.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:  # Parcourt chaque page du PDF
                text += page.extract_text()
        print("Extraction du texte terminée.")
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du PDF : {e}")
        return None
    
def structure_text_with_gpt(input_text, base_url, token, model="gpt-4o-mini"):
    # Définir l'URL pour le endpoint completions
    completion_url = base_url + "/completions"
    
    # Construire le prompt
    prompt = (
       # "Génère seulement et uniquement un JSON sans texte qui donne la hiéarchie du document ainsi que son contenu en entier : (Reste sur un petit niveau de granularité) "
       "Est ce que tu peux générer seulement et uniquement un JSON sans texte qui me donne uniquement la hiéarchie du texte (je ne veux pas que le content soit rempli, seulement la hiéarchie) extrait dun document de loi le but étant ensuite de donné la structure à un code pour extraire le contenu :"
        f"{input_text}"
    )
    
    # Préparer les données pour la requête
    data = {
        'model': model,
        'prompt': prompt,
        'max_tokens': 15000,  # Augmenter si le texte est long
        'temperature': 0.2  # Garde une température basse pour des résultats cohérents
    }
    
    # Préparer les headers pour l'authentification
    headers = {"Authorization": token}
               

    # Envoyer la requête POST à l'API
    response = requests.post(completion_url, json=data, headers=headers)
    response_text = response.content.decode('utf-8')
    #print(f"Reponse : {response_text}")
    return response_text


def save_json_to_file(json_content, output_path):
    """
    Sauvegarde le contenu JSON dans un fichier.
    :param json_content: Le contenu JSON à sauvegarder (sous forme de dict ou string JSON).
    :param output_path: Le chemin où enregistrer le fichier JSON.
    """
    try:
        # Si le JSON est sous forme de string, le convertir en dict
        if isinstance(json_content, str):
            json_content = json.loads(json_content)
            print("Json is instance")

        # Écrire dans un fichier
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_content, json_file, indent=4, ensure_ascii=False)
        print(f"Le fichier JSON a été sauvegardé avec succès dans : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du JSON : {e}")

def save_json_to_file_V2(json_content, output_path):
    """
    Sauvegarde le contenu JSON dans un fichier.
    :param json_content: Le contenu JSON à sauvegarder (sous forme de dict ou string JSON).
    :param output_path: Le chemin où enregistrer le fichier JSON.
    """
    try:
        # Si le JSON est sous forme de string, le convertir en dict
        if isinstance(json_content, str):
            json_content = json.loads(json_content)
            print("Json is instance")

        # Écrire dans un fichier
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_content, json_file, indent=4, ensure_ascii=False)
        print(f"Le fichier JSON a été sauvegardé avec succès dans : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du JSON : {e}")

def save_json_into_file (response_text, output_json_path):
    try:
        save_json_to_file_V2(response_text, output_json_path)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la réponse JSON : {e}")

pdf_path = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/FR_Loi_eckert.pdf" 
output_path ="/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/structured_data/structured_Loi_eckert.json"
input_text = extract_text_from_pdf(pdf_path)


response_text =structure_text_with_gpt(input_text, base_url, token, model="gpt-4o-mini")

print(f"Contenu brut de la réponse : {response_text}")
save_json_into_file(response_text, output_path)

