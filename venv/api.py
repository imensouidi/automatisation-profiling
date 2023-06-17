from flask import Flask, jsonify, request
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json
from manipulation_df.execution_fonctions_df import tables, create_dataframe_criteres
from manipulation_df.regroupement import cluster_data, regrouper_clusters
from fonction_charts.charts import count_occurrences, count_occurrences_colonnes, find_max_revenue, occurence_colonne, find_top_3_occurrences, detect_most_common_sports, calculer_revenu_moyen
import logging
from authentification.authQueney import login, register, create_super_admin
from middlewares.authMiddleware import admin_required, eu_required,superadmin_required
from bson import ObjectId

app = Flask(__name__)


# Route pour l'inscription d'un nouvel utilisateur
@app.route('/api/signup', methods=['POST'])
def signup_route():
    # Récupérer les données de la requête POST
    email = request.json.get('email')
    password = request.json.get('password')
    last_name = request.json.get('last_name')
    first_name = request.json.get('first_name') 
    phone_number = request.json.get('phone_number')   
    # Appeler la fonction pour l'inscription d'un nouvel utilisateur
    try:
        register(email, password,last_name,first_name,phone_number)
        return jsonify({'message': 'Registration successful'})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

# Route pour la connexion de l'utilisateur
@app.route('/api/login', methods=['POST'])
def login_route():
    # Récupérer les données de la requête POST
    email = request.json.get('email')
    password = request.json.get('password')

    # Appeler la fonction de connexion de l'utilisateur
    try:
        success, user = login(email, password)

        response = {'message': 'Login successful', 'user': user} if success else {'message': 'Invalid username or password'}
        return jsonify(response)
    except ValueError as e:
        return jsonify({'message': str(e)}), 401

#Api qui affiche les occurences des reponses de chaque colonne parcourant tout le tableau
@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    dataframe=create_dataframe_criteres()
    occurence=count_occurrences(dataframe)
    response_data = {
        "countByField" : occurence
    }
    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}

#Api pour l'interface qui affiche un dataframe
@app.route('/api/tables', methods=['GET'])
def api_tables():
    tableau=tables()
    occurence=count_occurrences(tableau)
    response_data = {
        "Questions et critères": tableau.to_dict(orient='records'),
        "countByField" : occurence 
    }
    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}

#Cet Api pour les criteres Age, Permis, Motorise et Most payed
@app.route('/api/dashboard_4col', methods=['GET'])
def api_dashboard_col():
    dataframe = create_dataframe_criteres()
    occurence = count_occurrences_colonnes(dataframe)
    max_revenue = find_max_revenue(dataframe)

    response_data = {
        "countByField": occurence,
        "maxRevenue": {
            "value": max_revenue
        }
    }

    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}

#Api concernant l'age
@app.route('/api/chartage', methods=['GET'])
def api_chart_age():
    dataframe = create_dataframe_criteres()
    selected_column = "Age"
    occ = occurence_colonne(dataframe, selected_column)

    data = list(occ.values())
    labels = list(occ.keys())  # Utiliser directement les clés comme liste de labels

    response_data = {
        "data": data,
        "labels": labels
    }

    response = json.dumps(response_data)  # Convertir le dictionnaire en chaîne JSON
    return response, 200, {'Content-Type': 'application/json'}

#Api des films
@app.route('/api/chartfilm', methods=['GET'])
def api_chart_film():
    dataframe = create_dataframe_criteres()
    selected_column = "Film"
    occ = occurence_colonne(dataframe, selected_column)

    data = list(occ.values())
    labels = list(occ.keys())  # Utiliser directement les clés comme liste de labels

    response_data = {
        "data": data,
        "labels": labels
    }

    response = json.dumps(response_data)  # Convertir le dictionnaire en chaîne JSON
    return response, 200, {'Content-Type': 'application/json'}

#Api des clubs
@app.route('/api/chartclub', methods=['GET'])
def api_top_3_clubs():
    dataframe = create_dataframe_criteres() 
    colonne = "Club"
    top_3_responses = find_top_3_occurrences(dataframe, colonne)

    counts = occurence_colonne(dataframe, colonne)
    data = [counts[response] for response in top_3_responses]

    response_data = {
        "data": data,
        "labels": top_3_responses
    }

    response = json.dumps(response_data)  # Convertir le dictionnaire en chaîne JSON
    return response, 200, {'Content-Type': 'application/json'}

#Api concernant sports
@app.route('/api/chartsports', methods=['GET'])
def api_top_sports():
    dataframe = create_dataframe_criteres()
    colonne = "Sport"
    top_sports = detect_most_common_sports(dataframe, colonne, top_n=3)

    labels = [sport["Sport"] for sport in top_sports]
    data = [sport["Occurrence"] for sport in top_sports]

    response_data = {
        "data": data,
        "labels": labels
    }
    
    response = json.dumps(response_data)  # Convertir le dictionnaire en chaîne JSON
    return response, 200, {'Content-Type': 'application/json'}


@app.route('/api/clustering', methods=['GET'])
def api_meanshift():
    dataframe=create_dataframe_criteres()
    result=regrouper_clusters(dataframe)
    response_data = {
        "result": result.to_dict(orient='records'),
    }
    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO)
    create_super_admin()
    app.run(debug=True)

