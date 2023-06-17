import os
from flask import Flask, jsonify
from pymongo import MongoClient
import bcrypt
import re
from authentification.notifications import create_notification

# Create Flask application
app = Flask(__name__)


# Connect to MongoDB
mongo_uri = "mongodb+srv://mariembnacef:azerty123@cluster0.0e48dj1.mongodb.net/?retryWrites=true&w=majority"
db_name ="queney"
email_superadmin = "admin@admin.com"

client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db["users"]
notifications = db['notifications']

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def login(email, password):
    # Check if the user exists in the database
    user = users_collection.find_one({"email": email})

    if not user:
        raise ValueError("user does not exist")

    if "status" in user and user["status"] == "Desactivé":
        raise ValueError("Compte utilisateur désactivé")

    
    hashed_password = user["password"]
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        raise ValueError("Invalid email or password")
    
    # Convert the bytes to string
    user["_id"] = str(user["_id"])
    user["password"] = str(user["password"])

    return True, user


def register(email, password, last_name, first_name, phone_number):
    # Vérifier si le nom d'utilisateur existe déjà dans la base de données
    existing_user = users_collection.find_one({"email": email})

    if existing_user:
        raise ValueError("L'email existe déjà.")
    if not is_email_valid(email):
        raise ValueError("L'email n'est pas valide.")
    if not is_password_strong(password):
        raise ValueError("Le mot de passe doit être fort.")
    if not last_name or not first_name:
        raise ValueError("Veuillez entrer votre nom et prénom.")
    if not is_phone_number_valid(phone_number):
        raise ValueError("Veuillez saisir votre numéro de téléphone correctement")
    
    # Hasher le mot de passe
    hashed_password = hash_password(password)

    # Créer un nouveau document utilisateur
    new_user = {
        "email": email,
        "last_name": last_name,
        "first_name": first_name,
        "phone_number": phone_number,
        "role": "admin",
        "status": "Desactivé",
        "password": hashed_password
    }
    # Insérer le nouvel utilisateur dans la base de données
    users_collection.insert_one(new_user)
    # Créer une notification pour le super administrateur
    notifications.insert_one(create_notification(email, last_name, first_name))

    return True

def is_email_valid(email):
    # Vérifier si l'email a un format valide
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

def is_password_strong(password):
    # Vérifier la longueur du mot de passe
    if len(password) < 8:
        return False
    
    # Vérifier s'il contient une lettre en majuscule
    if not re.search(r'[A-Z]', password):
        return False
    
    # Vérifier s'il contient un caractère spécial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

def is_phone_number_valid(phone_number):
    pattern = r"^\+[1-9]\d{1,14}$"
    return re.match(pattern, phone_number) is not None

def create_super_admin():
    # Check if the super admin user already exists
    if users_collection.find_one({'email': 'admin@admin.com'}):
        return
    
    # Hash the password
    hashed_password = hash_password("azerty123")

    # Create the super admin user
    super_admin = {
        'email': email_superadmin,
        'password': hashed_password,
        'name': 'Super Admin',
        'role': 'superadmin',
        'enabled':True
    }
    users_collection.insert_one(super_admin)
    
if __name__ == '__main__':
    app.run()