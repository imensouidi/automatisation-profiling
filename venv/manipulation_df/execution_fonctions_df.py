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

def fonctions():
    df = normaliser(jointure())
    n, liste1 = compatible_columns_lignes(df)
    liste2 = compatible_columns_colonnes(df, lecture_dictionnaire('dic.txt'))
    dff = transformer_donnees(df, liste1, liste2)
    dff = remplir(dff, lecture_dictionnaire('dic.txt'))
    return liste1, liste2, df, dff

def create_dataframe_criteres():
    liste1, liste2, df, dff = fonctions()
    dataframe = df[['User id']]
    clubs = extraire_colonnes_club(df)
    clubs.insert(0, 'User id', df['User id'])
    clubs = remplir_common_columns(clubs)
    dataframe = pd.merge(dataframe, clubs[['User id', clubs.columns[3]]], on='User id').rename(columns={clubs.columns[3]: 'Club'})
    dataframe = fusionner_donnees(dataframe, dff, liste1, liste2)
    return dataframe

def tables():
    liste1, liste2, df, dff = fonctions()
    dataframe = create_dataframe_criteres()
    df_final = obtenir_df_final(dataframe, df, liste1, liste2)
    return df_final







# def colonnes_choisie():
#     dataframe = create_dataframe_criteres()
#     label_encoder = LabelEncoder()
#     colonnes_choisies = pd.DataFrame(dataframe.iloc[:, 0])

#     data = request.get_json()
#     t = data['t']
#     n = 0

#     while t in range(dataframe.shape[1]):
#         n += 1
#         column = dataframe.columns[t]
#         found_in_keywords = False

#         for key in lecture_dictionnaire('dic.txt').keys():
#             if column == key:
#                 found_in_keywords = True
#                 break

#         if not found_in_keywords:
#             nom = input('Donner un nom à cette colonne : ')
#         else:
#             nom = column

#         colonnes_choisies.insert(n, nom, label_encoder.fit_transform(dataframe.iloc[:, t]))
#         t = data['t']

#     return colonnes_choisies
    
# def cluster_data():
#     est_bandwidth = 10

#     # Obtenez les données à partir de create_dataframe_criteres()
#     dataframe = create_dataframe_criteres()
#     X = colonnes_choisie()

#     # Créer l'instance du modèle Mean Shift
#     ms = MeanShift(bandwidth=est_bandwidth, bin_seeding=True).fit(X.iloc[:, 1:])

#     labels_unique = np.unique(ms.labels_)
#     n_clusters_ = len(labels_unique)

#     # Ajuster le modèle Mean Shift sur les données
#     ms = MeanShift()
#     ms.fit(X.drop('User id', axis=1))
#     labels = ms.labels_

#     n_clusters = len(set(labels))

#     dataframe['cluster'] = ms.labels_

#     result = pd.DataFrame(columns=dataframe.drop('User id', axis=1).columns)

#     for name, group in dataframe.groupby(['cluster']):
#         cluster_info = {}
#         for col in dataframe.drop(['User id'], axis=1).columns:
#             mode_values = group[col].mode()
#             if not mode_values.empty:
#                 common = mode_values.iloc[0]
#                 cluster_info[col] = common
#         cluster_info['Number of Users'] = len(group)  # Ajouter le nombre d'identifiants d'utilisateurs
#         result = result.append(cluster_info, ignore_index=True)

#     result.insert(0, 'cluster', result.pop('cluster'))

#     # Convertir la colonne 'Number of Users' en entier
#     result['Number of Users'] = result['Number of Users'].astype(int)

#     return result


if __name__ == '__main__':
    app.run()
