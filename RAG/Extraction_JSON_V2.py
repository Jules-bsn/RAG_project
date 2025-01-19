import pdfplumber
import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
env_path = Path('/Users/julesbesson/Documents/Projet_EY/Projet_EY/RAG/.env')
load_dotenv(dotenv_path=env_path)

# Étape 1 : Authentification pour obtenir le token
base_url = os.getenv("BASE_URL")
auth_user = os.getenv("AUTH_USER")
auth_password = os.getenv("AUTH_PASSWORD")
auth = (auth_user, auth_password)

login_url = base_url + "/login"
response = requests.post(login_url, auth=auth)

if response.status_code != 200:
    print(f"Erreur d'authentification : {response.content}")
    exit()

token = response.json().get('token')
headers = {'Authorization': token}
print(f"Token obtenu : {token}")

# Étape 2 : Extraire le texte brut du PDF
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Étape 3 : Analyser la structure avec l'API ChatGPT
def structure_law_with_custom_api(text):
    # Découper le texte en parties gérables (pour éviter la limite de tokens)
    chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
    structured_data = []

    for chunk in chunks:
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Vous êtes un assistant spécialisé en structuration de textes législatifs."
                },
                {
                    "role": "user",
                    "content": f"Voici un texte législatif :\n\n{chunk}\n\n"
                               "Analysez ce texte et structurez-le en JSON avec cette hiérarchie :\n"
                               "1. Chapitres (title).\n"
                               "2. Sections (sous les chapitres).\n"
                               "3. Articles (dans chaque section).\n"
                               "4. Contenu complet de chaque article."
                }
            ]
        }

        # Requête à l'API avec le token
        api_url = base_url + "/completions"
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Erreur lors de la requête API : {response.content}")
            continue

        try:
            response_data = response.json()
            structured_data.append(json.loads(response_data["choices"][0]["message"]["content"]))
        except (KeyError, json.JSONDecodeError):
            print(f"Erreur de parsing JSON : {response.content}")

    return structured_data

# Étape 4 : Sauvegarder le JSON final
def save_to_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Chemin du fichier PDF
file_path = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/FR_Loi_eckert.pdf" 
output_file ="/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/structured_data/structured_Loi_eckert.json"
text = extract_text_from_pdf(file_path)
structured_data = structure_law_with_custom_api(text)
save_to_json(structured_data, output_file)

print(f"Données structurées sauvegardées dans {output_file}")
