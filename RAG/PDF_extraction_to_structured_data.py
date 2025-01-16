from dotenv import load_dotenv
import os
from pathlib import Path

# Charge les variables d'environnement depuis le fichier .env
env_path = Path('/Users/julesbesson/Documents/Projet_EY/Projet_EY/RAG/.gitignore/.env')  # Fichier .env est dans le dossier parent
load_dotenv(dotenv_path=env_path)

# Accéder à la variable d'environnement
base_url = os.getenv("BASE_URL")
auth_user = os.getenv("AUTH_USER")
auth_password = os.getenv("AUTH_PASSWORD")

