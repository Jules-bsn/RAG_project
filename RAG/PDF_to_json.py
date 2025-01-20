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
'''
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

def split_text_into_chunks(text, chunk_size=4000):
    """
    Divise un texte en morceaux de taille spécifiée.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def clean_and_convert_to_json(raw_text):
    """
    Nettoie une chaîne brute et tente de la convertir en JSON valide.
    
    Args:
        raw_text (str): Texte brut reçu au format JSON-like.
    
    Returns:
        dict: Un objet JSON Python (ou None si la conversion échoue).
    """
    try:
        # Étape 1 : Supprimer les parties parasites (si nécessaire, adapter les règles)
        cleaned_text = raw_text.strip()  # Suppression des espaces et lignes vides au début/fin
        
        # Si des caractères ou des sections parasites sont attendus, ajouter un nettoyage ici.
        # Par exemple, pour enlever des "```json" ou des commentaires parasites :
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.replace("```json", "").replace("```", "")
        
        # Étape 2 : Convertir le texte nettoyé en JSON
        json_data = json.loads(cleaned_text)
        return json_data
    
    except json.JSONDecodeError as e:
        print("Erreur lors de la conversion en JSON :", e)
        print("Texte problématique :", raw_text)
        return None

def process_chunk(chunk, base_url, token, model="gpt-4o-mini"):
    """
    Traite un morceau de texte via l'API GPT pour générer un JSON structuré.
    """
    completion_url = base_url + "/completions"
    prompt = (
        "Génère seulement et uniquement un JSON sans texte qui donne la hiérarchie du document ainsi que son contenu en entier : "
        f"{chunk}"
    )
    
    data = {
        'model': model,
        'prompt': prompt,
        'max_tokens': 15000,
        'temperature': 0.2
    }
    headers = {"Authorization": token}

    try:
        response = requests.post(completion_url, json=data, headers=headers)
        response.raise_for_status()  # Vérifie si la requête est réussie
        #print(f"Réponse brute pour le chunk : {response.content}")

        response_text = response.content.decode('utf-8')
        cleaned_json = clean_and_convert_to_json(response_text)
        print(cleaned_json)
        return cleaned_json  # Convertit en objet JSON
    except Exception as e:
        print(f"Erreur lors du traitement du chunk : {e}")
        return None

def merge_json_responses(json_responses):
    """
    Combine plusieurs réponses JSON en un seul JSON structuré.
    """
    combined_data = {"sections": []}  # Exemple de structure, à adapter selon vos besoins
    for response in json_responses:
        if response:  # Si la réponse n'est pas None
            combined_data["sections"].append(response)
    return combined_data

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

# Fonction principale
def process_large_text(text, base_url, token, output_path, chunk_size=4000, model="gpt-4o-mini"):
    """
    Divise un texte en morceaux, les traite via l'API, puis combine les réponses dans un fichier JSON.
    """
    chunks = split_text_into_chunks(text, chunk_size)
    print(f"Nombre de chunks créés : {len(chunks)}")

    json_responses = []
    for i, chunk in enumerate(chunks):
        print(f"Traitement du chunk {i + 1}/{len(chunks)}")
        response = process_chunk(chunk, base_url, token, model)
        json_responses.append(response)

    combined_json = merge_json_responses(json_responses)
    save_json_to_file(combined_json, output_path)
    print(f"Le JSON combiné a été sauvegardé avec succès dans : {output_path}")

# Exemple d'utilisation
pdf_path = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/FR_Loi_eckert.pdf"
output_path = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/structured_data_JSON/structured_Loi_eckert.json"

# Extraction du texte brut du PDF
input_text = extract_text_from_pdf(pdf_path)

# Traitement du texte en chunks
process_large_text(input_text, base_url, token, output_path, chunk_size=4000)
'''

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

def split_text_into_chunks(text, chunk_size=4000):
    """
    Divise un texte en morceaux de taille spécifiée.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def clean_and_convert_to_json(raw_text):
    """
    Nettoie une chaîne brute et tente de la convertir en JSON valide.
    
    Args:
        raw_text (str): Texte brut reçu au format JSON-like.
    
    Returns:
        dict: Un objet JSON Python (ou None si la conversion échoue).
    """
    try:
        # Étape 1 : Supprimer les parties parasites (si nécessaire, adapter les règles)
        cleaned_text = raw_text.strip()  # Suppression des espaces et lignes vides au début/fin
        
        # Si des caractères ou des sections parasites sont attendus, ajouter un nettoyage ici.
        # Par exemple, pour enlever des "```json" ou des commentaires parasites :
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.replace("```json", "").replace("```", "")
        
        # Étape 2 : Convertir le texte nettoyé en JSON
        json_data = json.loads(cleaned_text)
        return json_data
    
    except json.JSONDecodeError as e:
        print("Erreur lors de la conversion en JSON :", e)
        print("Texte problématique :", raw_text)
        return None

def process_chunk(chunk, base_url, token, model="gpt-4o-mini"):
    """
    Traite un morceau de texte via l'API GPT pour générer un JSON structuré.
    """
    completion_url = base_url + "/completions"
    prompt = (
        "Voici un extrait de texte législatif. Structure-le en un JSON hiérarchique qui respecte la structure des chapitres, articles et sections, "
        "en préservant le contenu intégral (le niveau de granularité doit être faible). Utilise des clés claires pour représenter les titres et le contenu. Ne génère que du JSON :\n"
        f"{chunk}"
    )
    
    data = {
        'model': model,
        'prompt': prompt,
        'max_tokens': 15000,
        'temperature': 0.2
    }
    headers = {"Authorization": token}

    try:
        response = requests.post(completion_url, json=data, headers=headers)
        response.raise_for_status()  # Vérifie si la requête est réussie
        #print(f"Réponse brute pour le chunk : {response.content}")

        response_text = response.content.decode('utf-8')
        cleaned_json = clean_and_convert_to_json(response_text)
        #print(cleaned_json)
        return cleaned_json  # Convertit en objet JSON
    except Exception as e:
        print(f"Erreur lors du traitement du chunk : {e}")
        return None

def merge_json_responses(json_responses):
    """
    Combine plusieurs réponses JSON en un seul JSON structuré.
    """
    combined_data = {"sections": []}  # Exemple de structure, à adapter selon vos besoins
    for response in json_responses:
        if response:  # Si la réponse n'est pas None
            combined_data["sections"].append(response)
    return combined_data

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

# Fonction principale
def process_large_text(text, base_url, token, output_path, chunk_size=4000, model="gpt-4o-mini"):
    """
    Divise un texte en morceaux, les traite via l'API, puis combine les réponses dans un fichier JSON.
    """
    chunks = split_text_into_chunks(text, chunk_size)
    print(f"Nombre de chunks créés : {len(chunks)}")

    json_responses = []
    for i, chunk in enumerate(chunks):
        print(f"Traitement du chunk {i + 1}/{len(chunks)}")
        response = process_chunk(chunk, base_url, token, model)
        json_responses.append(response)

    combined_json = merge_json_responses(json_responses)
    save_json_to_file(combined_json, output_path)
    print(f"Le JSON combiné a été sauvegardé avec succès dans : {output_path}")

# Exemple d'utilisation
pdf_path = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/FR_Loi_eckert.pdf"
output_path = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/structured_data_JSON/structured_Loi_eckert.json"

# Extraction du texte brut du PDF
input_text = extract_text_from_pdf(pdf_path)

# Traitement du texte en chunks
process_large_text(input_text, base_url, token, output_path, chunk_size=4000)
