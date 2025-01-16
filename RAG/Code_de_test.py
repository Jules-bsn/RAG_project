#pip install langchain openai PyPDF2 pdfplumber pandas
from dotenv import load_dotenv
import os
from pathlib import Path
import pdfplumber
import requests

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

def structure_text_with_gpt(input_text, base_url, token, model="gpt-4o-mini"):
    # Définir l'URL pour le endpoint completions
    completion_url = base_url + "/completions"
    
    # Construire le prompt
    prompt = (
        "Génère un fichier JSON contenant les informations suivantes : "
        f"{input_text}"
    )
    
    # Préparer les données pour la requête
    data = {
        'model': model,
        'prompt': prompt,
        'max_tokens': 10000,  # Augmenter si le texte est long
        'temperature': 0.2  # Garde une température basse pour des résultats cohérents
    }
    
    # Préparer les headers pour l'authentification
    headers = {"Authorization": token}
               

    # Envoyer la requête POST à l'API
    response = requests.post(completion_url, json=data, headers=headers)
    response_text = response.content.decode('utf-8')
    print(f"Reponse : {response_text}")
    

structure_text_with_gpt("Nom, prénom, age, profession", base_url, token, model="gpt-4o-mini")