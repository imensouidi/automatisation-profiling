import os
from flask import Flask, jsonify
from pymongo import MongoClient
import re

# Create Flask application
app = Flask(__name__)

from pymongo import MongoClient

# Se connecter à la base de données MongoDB
client = MongoClient('mongodb+srv://souidiimen16:84bgYx2Nb8pSbdQq@cluster0.khip5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.queney  # Se connecter à la base de données "queney"
collection = db.users  # Accéder à la collection "users"
collection_notifications = db.notifications

#Fonction qui permet l'affichage des liste des utilisateurs
def afficher_utilisateurs():
    utilisateurs = collection.find()

    # Créer une liste d'utilisateurs avec les informations spécifiques
    result = []
    for utilisateur in utilisateurs:
        email = utilisateur.get('email')
        last_name = utilisateur.get('last_name')
        first_name = utilisateur.get('first_name')
        phone_number = utilisateur.get('phone_number')
        status = utilisateur.get('status')

        #les informations à afficher
        user_info = {
            'email': email,
            'last_name': last_name,
            'first_name': first_name,
            'phone_number': phone_number,
            'status': status
        }
        result.append(user_info)

    return result

# Fonction pour activer ou désactiver un compte
def changer_statut_utilisateur(email, nouveau_statut):
    """ Met à jour le statut d'un utilisateur et vérifie si l'opération a réussi """
    result = collection.update_one({'email': email}, {'$set': {'status': nouveau_statut}})

    if result.modified_count > 0:
        print(f"✅ Statut de {email} mis à jour en {nouveau_statut}.")
        return True
    else:
        print(f"⚠️ Aucune mise à jour effectuée pour {email} (peut-être introuvable ou statut inchangé).")
        return False






if __name__ == '__main__':
    app.run()