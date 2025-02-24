import os
from flask import Flask, jsonify
from pymongo import MongoClient
import bcrypt
import re
from dotenv import load_dotenv
from authentification.notifications import create_notification

# Charger les variables d'environnement
load_dotenv()

# Initialiser Flask
app = Flask(__name__)

# Charger l'URI MongoDB depuis .env (sécurisé)
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://souidiimen16:84bgYx2Nb8pSbdQq@cluster0.khip5.mongodb.net/?retryWrites=true&w=majority&tls=true")
db_name = os.getenv("DB_NAME", "queney")
email_superadmin = os.getenv("EMAIL_SUPERADMIN", "admin@admin.com")

# Connexion à MongoDB
try:
    client = MongoClient(mongo_uri)
    db = client[db_name]
    users_collection = db["users"]
    notifications = db["notifications"]
    print("✅ Connexion réussie à MongoDB")
except Exception as e:
    print("❌ Erreur de connexion à MongoDB :", e)
    exit(1)


def hash_password(password):
    """ Hashage sécurisé du mot de passe """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def login(email, password):
    """ Connexion de l'utilisateur """
    user = users_collection.find_one({"email": email})

    if not user:
        raise ValueError("L'utilisateur n'existe pas")

    if "status" in user and user["status"] == "Desactivé":
        raise ValueError("Compte utilisateur désactivé")

    hashed_password = user["password"]
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        raise ValueError("Email ou mot de passe invalide")

    # Mettre à jour le champ "connect" de l'utilisateur
    users_collection.update_one({"_id": user["_id"]}, {"$set": {"connect": True}})
    updated_user = users_collection.find_one({"_id": user["_id"]})
    return True, updated_user


def logout(email):
    """ Déconnexion de l'utilisateur """
    user = users_collection.find_one({"email": email})
    if user:
        users_collection.update_one({"_id": user["_id"]}, {"$set": {"connect": False}})
        return "Déconnexion réussie"
    else:
        return "Utilisateur non trouvé"


def register(email, password, last_name, first_name, phone_number, role="user"):
    """ Créer un nouvel utilisateur avec un mot de passe haché """
    if users_collection.find_one({"email": email}):
        raise ValueError("L'email est déjà utilisé")

    # 🔥 Vérifier si le mot de passe est déjà haché
    if isinstance(password, str):  # Si c'est une chaîne, on le hache
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    else:
        hashed_password = password  # Si déjà en bytes, ne pas re-hacher

    new_user = {
        "email": email,
        "password": hashed_password,  # 🔥 Stocké en format bcrypt
        "last_name": last_name,
        "first_name": first_name,
        "phone_number": phone_number,
        "role": role,  # Ajoute le rôle par défaut "user"
        "status": "Désactivé"
    }

    users_collection.insert_one(new_user)
    print(f"✅ Utilisateur {email} créé avec un mot de passe sécurisé et le rôle {role}")

def is_email_valid(email):
    """ Vérifie si l'email est valide """
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(regex, email) is None:
        return False
    
    valid_extensions = ["naxxum.fr", "queney.com"]
    domain = email.split('@')[-1]
    return domain in valid_extensions


def is_password_strong(password):
    """ Vérifie si le mot de passe est sécurisé """
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )


def is_phone_number_valid(phone_number):
    """ Vérifie si le numéro de téléphone est valide """
    pattern = r"^\+[1-9]\d{1,14}$"
    return re.match(pattern, phone_number) is not None


def create_super_admin():
    """ Crée un super administrateur si inexistant """
    try:
        existing_superadmin = users_collection.find_one({'email': email_superadmin})
        
        if existing_superadmin:
            print("✅ Super admin existe déjà.")
            return  # Le superadmin existe déjà, pas besoin de recréer

        hashed_password = hash_password("azerty123")  # Hash du mot de passe

        super_admin = {
            'email': email_superadmin,
            'password': hashed_password,
            'first_name': "Super",
            'last_name': "Admin",
            'phone_number': "+33699999999",
            'role': 'superadmin',
            'status': None  # Le superadmin n'a pas de statut
        }

        users_collection.insert_one(super_admin)
        print("✅ Super admin créé avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de la création du super admin : {e}")


if __name__ == '__main__':
    app.run(debug=True)
