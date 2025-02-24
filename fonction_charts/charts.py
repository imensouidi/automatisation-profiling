from manipulation_df.fonctions_df import supprimer_lignes_utilisateur_repete, lecture_fichier, jointure, lecture_dictionnaire, obtenir_df_final, normaliser, compatible_columns, compatible_columns_lignes, transformer_donnees, extraire_colonnes_club, compatible_columns_colonnes, creer_liste_reponses_ligne, rechercher_sous_ensemble, verifier_coherence, mots_repetes, remplir, get_common_columns, remplir_common_columns
from manipulation_df.fonctions_df import fusionner_donnees
import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
import ast
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from sklearn.cluster import MeanShift
import re

app=Flask(__name__)
CORS(app)



#Detecter l'occurence des réponses de toutes les colonnes
def count_occurrences(df):
    counts = {}
    for col in df.columns[1:]:
        counts[col] = df[col].value_counts().to_dict()
    return counts

#Trouver la réponse la plus courrante
def trouver_reponse_plus_repondu(df, colonne):
    occurrences = occurence_colonne(df, colonne)
    sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    max_occurrence = max(occurrences.values())  # Occurrence maximale
    max_revenu = [revenu for revenu, occurrence in sorted_occurrences if occurrence == max_occurrence]
    if max_revenu:
        return max_revenu[0]  # Retourne le premier revenu ayant l'occurrence maximale
    else:
        return None
    
#Retourner l'occurence maximale
def occurence_colonne_max(df, colonne):
    occurrences = {}
    for valeur in df[colonne]:
        if valeur in occurrences:
            occurrences[valeur] += 1
        else:
            occurrences[valeur] = 1
    max_occurrence = max(occurrences.values())
    return max_occurrence


#Detecter l'occurence des réponses des colonnes Genre, Permis de conduire et Motorisé
def count_occurrences_colonnes(df):
    selected_columns = ["Genre", "Permis de conduire", "Motorisé"]
    counts = {}
   
    for col in selected_columns:
        counts[col] = df[col].value_counts().to_dict()

    return counts

#Detecter la valeur maximale
def find_max_revenue(df):
    max_revenue = df["Revenu"].max()
    return max_revenue

#Détecter l'occurence des réponses d'une seule colonne
def occurence_colonne(df, colonne):
    
    count = df[colonne].value_counts().to_dict()
    return count

            
            
            
# Fonction qui retourne les 3 noms de clubs les plus fréquents
def find_top_3_occurrences(df, colonne):
    occurrences = occurence_colonne(df, colonne)
    sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    top_3 = []
    count = 0
    for club, occurrence in sorted_occurrences:
        if count >= 3:
            break
        if club.lower() != 'none' and club.lower() != 'aucun':
            top_3.append(club)
            count += 1
    return top_3

#Fonction pour les sports les plus choisis
def detect_most_common_sports(df, colonne, top_n=3):
    all_options = [option for option in df[colonne] if option is not None and option.lower() != "aucun"]
    all_options = ', '.join(all_options).split(', ')
    word_counts = Counter(all_options)
    top_sports = word_counts.most_common(top_n)

    other_sports_count = sum(word_counts.values()) - sum(count for word, count in top_sports)
    other_sports = {"Sport": "Autres", "Occurrence": other_sports_count}

    top_sports_with_occurrence = [{"Sport": sport, "Occurrence": count} for sport, count in top_sports]
    top_sports_with_occurrence.append(other_sports)

    return top_sports_with_occurrence



def calculer_revenu_moyen(df):
    salaire_moyen = {}
    for occupation in df['Occupation'].unique():
        salaires = []
        for revenu in df[df['Occupation'] == occupation]['Revenu']:
            if revenu:
                # Vérifier les différents formats de valeurs de revenu
                if 'entre' in revenu:
                    valeurs = [int(v) for v in re.findall(r'\d+', revenu)]
                    salaires.extend(range(valeurs[0], valeurs[1]+1))
                elif 'supérieur' in revenu:
                    salaires.append(int(re.findall(r'\d+', revenu)[0]))
                else:
                    salaires.append(int(re.findall(r'\d+', revenu)[0]))
        
        if salaires:
            salaire_moyen[occupation] = sum(salaires) / len(salaires)
    
    return salaire_moyen

def trouver_revenu(df, colonne):
    occurrences = occurence_colonne(df, colonne)
    reponse_plus_repondu = max(occurrences, key=occurrences.get)
    return reponse_plus_repondu



if __name__ == '__main__':
    app.run() 

