import logging
from flask import Flask, jsonify, request
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json
from manipulation_df.execution_fonctions_df import tables, create_dataframe_criteres, questions_sans_criteres
from manipulation_df.regroupement import cluster_data, regrouper_clusters
from fonction_charts.charts import count_occurrences, count_occurrences_colonnes, find_max_revenue, occurence_colonne, find_top_3_occurrences, detect_most_common_sports, calculer_revenu_moyen, trouver_reponse_plus_repondu, occurence_colonne_max
from authentification.authQueney import login, register, create_super_admin, logout, users_collection
from middlewares.authMiddleware import admin_required, eu_required, superadmin_required
from bson import ObjectId
from authentification.gerer_compte.fonctions_superadmin import afficher_utilisateurs, changer_statut_utilisateur
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permet toutes les origines sur les routes /api/*





@app.route('/api/signup', methods=['POST'])
def signup_route():
    print("Received data:", request.json)  # Debugging print

    email = request.json.get('email')
    password = request.json.get('password')
    last_name = request.json.get('last_name')
    first_name = request.json.get('first_name')
    phone_number = request.json.get('phone_number')
    
    # 🔥 Ajouter un rôle par défaut si non fourni
    role = request.json.get('role', 'user')  # Default role is "user"

    try:
        register(email, password, last_name, first_name, phone_number, role)  # Pass role to register function
        return jsonify({'message': 'Registration successful'})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        print("Unexpected error:", str(e))  # Debugging print
        return jsonify({'message': 'Internal Server Error'}), 500


    
@app.route('/api/login', methods=['POST'])
def login_route():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        success, user = login(email, password)
        
        if success:
            # 🔥 Vérification du statut
            if user.get("status") != "Activé":
                return jsonify({'message': 'Votre compte est désactivé. Veuillez contacter un administrateur.'}), 403

            response = {
                'message': 'Connexion réussie',
                'user': {
                    'email': user['email'],
                    'role': user['role'],
                    'first_name': user.get('first_name', ''),
                    'last_name': user.get('last_name', ''),
                    'status': user.get('status', 'Inconnu')
                }
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': 'Email ou mot de passe incorrect'}), 401

    except ValueError as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        print(f"🚨 Erreur serveur: {e}")
        return jsonify({'message': 'Erreur serveur interne'}), 500



@app.route('/api/logout', methods=['POST'])
def logout_api():
    # Récupérer les informations de l'utilisateur depuis la requête
    email = request.json.get('email')
    
    try:
        message = logout(email)
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'message': str(e)}), 500




#Route qui affiche les occurences des reponses de chaque colonne parcourant tout le tableau
@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    dataframe=create_dataframe_criteres()
    occurence=count_occurrences(dataframe)
    response_data = {
        "critères": dataframe.to_dict(orient='records'), 
        "countByField" : occurence
    }
    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}

#Route pour l'interface qui affiche un dataframe des criteres et d'autres questions
@app.route('/api/tables', methods=['GET'])
def api_tables():
    try:
        tableau = tables()
        occurence = count_occurrences(tableau)

        # Vérifier les valeurs problématiques
        print("Tableau avant conversion JSON:", tableau.head())

        tableau = tableau.fillna("").astype(str)

        response_data = {
            "Questions et critères": tableau.to_dict(orient='records'),
            "countByField": occurence
        }

        print("Réponse JSON prête à être envoyée")
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Erreur dans /api/tables: {e}")
        return jsonify({"message": "Erreur interne", "error": str(e)}), 500


@app.route('/api/questionssanscriteres', methods=['GET'])
def api_questions():
    questions = questions_sans_criteres()
    occurence=count_occurrences(questions)
    response_data = {
        "Questions sans critères": questions.to_dict(orient='records'),
        "countByField" : occurence 
    }
    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}
    
#Route pour les criteres Age, Permis, Motorise et Most payed
@app.route('/api/dashboard_4col', methods=['GET'])
def api_dashboard_col():
    dataframe = create_dataframe_criteres()
    occurence = count_occurrences_colonnes(dataframe)
    colonne = 'Revenu'
    occ_max = occurence_colonne_max(dataframe, colonne)
    revenu = trouver_reponse_plus_repondu(dataframe, colonne)
    response_data = {
        
        "countByField": occurence,
        revenu : occ_max
    }

    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}

#Route pour afficher le revenu le plus choisi
@app.route('/api/revenu', methods=['GET'])
def get_revenu():
    dataframe=create_dataframe_criteres()
    colonne = 'Revenu'
    occurence = occurence_colonne_max(dataframe, colonne)
    revenu = trouver_reponse_plus_repondu(dataframe, colonne)
    
    response_data = {
        revenu : occurence
    }
    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}


#Route concernant l'age
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

#Route des films
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

#Route des clubs
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

#Route concernant sports
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

#occupation : revenu 
@app.route('/api/chartrevenu', methods=['GET'])
def api_salaire_moyen_par_occupation():
    dataframe = create_dataframe_criteres()
    result = calculer_revenu_moyen(dataframe)

    labels = []
    data = []

    for occupation, revenu in result.items():
        labels.append(occupation)
        data.append(revenu)

    response_data = {
        "occupation_revenu": dict(zip(labels, data))
    }

    response = jsonify(response_data)
    return response, 200


   


#Route pour le regroupement
@app.route('/api/clustering', methods=['GET'])
def api_meanshift():
    dataframe=create_dataframe_criteres()
    result=regrouper_clusters(dataframe)
    response_data = {
        "result": result.to_dict(orient='records'),
    }
    response = json.dumps(response_data)  # Convert dictionary to JSON string
    return response, 200, {'Content-Type': 'application/json'}

#Route pour afficher la liste des utilisateurs
@app.route('/api/get_users', methods=['GET'])
def get_users():
    result = afficher_utilisateurs()
    return jsonify(result)

@app.route('/api/changer_statut_utilisateur', methods=['POST'])
def api_changer_statut_utilisateur():
    email = request.json.get('email')
    status = request.json.get('status')

    if not email or not status:
        return jsonify({'success': False, 'message': 'Paramètres manquants.'}), 400

    statuts_valides = ["Activé", "Désactivé"]
    if status not in statuts_valides:
        return jsonify({'success': False, 'message': 'Statut non valide.'}), 400

    success = changer_statut_utilisateur(email, status)

    if success:
        return jsonify({'success': True, 'message': f'Statut utilisateur mis à jour en {status}.'})
    else:
        return jsonify({'success': False, 'message': 'Utilisateur non trouvé.'}), 404


if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO)
    create_super_admin()
    app.run(debug=True)

