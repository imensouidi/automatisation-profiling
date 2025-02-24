from flask import Flask, jsonify
from pymongo import MongoClient

# Create Flask application
app = Flask(__name__)


email_superadmin = "admin@admin.com"


def create_notification(email, last_name, first_name):
    # Create a new notification document
    message = f"Nouvelle inscription en attente de validation : {last_name} {first_name} ({email})"
    new_notification = {
        "email": email_superadmin,
        "message": message,
        "status": "Desactivaté"
    }
    # Insert the new notification into the collection
    return new_notification



