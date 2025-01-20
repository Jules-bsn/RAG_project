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

if base_url == None : 
    print('Error : changer de kernel')



# Étape 2 : Fonction pour obtenir un token d'authentification
def authenticate(base_url, auth):
    login_url = base_url + "/login"  # Endpoint pour l'authentification
    response = requests.post(login_url, auth=auth)  # Envoie la requête POST avec les identifiants

    if response.status_code == 200:  # Vérifie si la requête a réussi
        token = response.json().get("token")  # Récupère le token depuis la réponse
        print("Authentification réussie. Token obtenu.")
        return token
    else:
        print(f"Erreur d'authentification : {response.status_code}, {response.text}")
        return None
    
# Étape 3 : Fonction pour extraire du texte d'un PDF
def extract_text_from_pdf(pdf_path):
    """
    Extrait le texte brut d'un fichier PDF.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:  # Parcourt chaque page du PDF
                text += page.extract_text()  # Ajoute le texte extrait
        print("Extraction du texte terminée.")
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du PDF : {e}")
        return None
    

# Fonction pour structurer automatiquement un texte avec GPT
def structure_text_with_gpt(input_text, base_url, token, model="gpt-4o-mini"):
    # Définir l'URL pour le endpoint completions
    completion_url = base_url + "/completions"
    
    # Construire le prompt
    prompt = (
        "Analyse le texte ci-dessous et structure-le en format JSON en détectant automatiquement sa structure logique "
        "(titres, sous-titres, paragraphes, listes, etc.). Voici le texte :\n\n"
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
    print(response)
    # Vérifier la réponse
    if response.status_code == 200:
        print("Texte structuré reçu depuis l'API.")
        structured_text = response.json()
        
        # Extraire la partie générée (texte structuré)
        structured_output = structured_text.get('choices', [{}])[0].get('text', '')
        
        return structured_output
    else:
        print(f"Erreur lors de l'appel à l'API : {response.status_code}, {response.text}")
        return None

def save_structured_data_to_file(structured_text, output_file):
    """
    Enregistre les données structurées dans un fichier JSON.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(structured_text)
        print(f"Données structurées enregistrées dans le fichier : {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des données : {e}")

def process_pdf_to_structured_data(pdf_path, output_file, base_url, auth):
    """
    Pipeline complet pour extraire, structurer et enregistrer le texte d'un PDF.
    """
    # Étape 1 : Authentification
    if not authenticate(base_url, auth):
        print("Fin du processus : échec d'authentification.")
        return
    else : 
        token = authenticate(base_url, auth)
        print("token =", token)
    # Étape 2 : Extraction du texte brut
    extracted_text = extract_text_from_pdf(pdf_path)

    if not extracted_text:
        print("Fin du processus : échec de l'extraction du texte.")
        return
    
    # Étape 3 : Structuration avec GPT
    structured_text = structure_text_with_gpt(extracted_text, base_url, token, model="gpt-4o-mini")
    if not structured_text:
        print("Fin du processus : échec de la structuration.")
        return
    
    # Étape 4 : Sauvegarde des données structurées
    save_structured_data_to_file(structured_text, output_file)
    print("Pipeline terminé avec succès.")

# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration
    pdf_path = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/FR_Loi_eckert.pdf" 
    output_file = "/Users/julesbesson/Documents/Projet_EY/Projet_EY/Data/structured_data_JSON/structured_Loi_eckert.json"  # Nom du fichier de sortie
    base_url = base_url
    # Lancer le pipeline
    process_pdf_to_structured_data(pdf_path, output_file, base_url, auth)