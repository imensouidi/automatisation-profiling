import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import MeanShift
from manipulation_df.fonctions_df import lecture_dictionnaire
from manipulation_df.execution_fonctions_df import create_dataframe_criteres
from flask import Flask, request
import json

app=Flask(__name__)

def cluster_data(tableau):
    # Copier le tableau d'origine
    tableau_copie = tableau.copy()
    
    # Supprimer la colonne "User id"
    tableau_copie = tableau_copie.drop("User id", axis=1)
    # Prétraitement des colonnes catégorielles
    colonnes_categorielles = tableau_copie.select_dtypes(include=["object"]).columns
    for colonne in colonnes_categorielles:
        # Encoder les valeurs catégorielles en numériques
        label_encoder = LabelEncoder()
        tableau_copie[colonne] = label_encoder.fit_transform(tableau_copie[colonne])
        
    est_bandwidth = 10
    ms = MeanShift(bandwidth=est_bandwidth, bin_seeding=True).fit(tableau_copie)

    labels_unique=np.unique(ms.labels_)
    n_clusters_=len(labels_unique)

    # Récupérer les étiquettes de cluster
    etiquettes_cluster = ms.labels_
    
    # Récupérer les centres de cluster
    centres_cluster = ms.cluster_centers_
    
    # Compter le nombre d'utilisateurs dans chaque cluster
    comptage_cluster = {}
    for label in etiquettes_cluster:
        if label in comptage_cluster:
            comptage_cluster[label] += 1
        else:
            comptage_cluster[label] = 1
    
    # Créer le tableau "result" avec les informations requises
    result = []
    for i in range(len(centres_cluster)):
        critere = centres_cluster[i]
        numero_cluster = i
        nombre_utilisateurs = comptage_cluster[i]
        
        result.append({
            "numero_cluster": numero_cluster,
            "critere": critere,
            "nombre_utilisateurs": nombre_utilisateurs
        })
    

# Créer un dictionnaire contenant la liste convertie


    return result

def regrouper_clusters(tableau):
    # Copier le tableau d'origine
    tableau_copie = tableau.copy()
    
    # Supprimer la colonne "User id"
    tableau_copie = tableau_copie.drop("User id", axis=1)
    
    # Prétraitement des colonnes catégorielles
    colonnes_categorielles = tableau_copie.select_dtypes(include=["object"]).columns
    for colonne in colonnes_categorielles:
        # Encoder les valeurs catégorielles en numériques
        label_encoder = LabelEncoder()
        tableau_copie[colonne] = label_encoder.fit_transform(tableau_copie[colonne])
        
    est_bandwidth = 10
    ms = MeanShift(bandwidth=est_bandwidth, bin_seeding=True).fit(tableau_copie)

    labels_unique = np.unique(ms.labels_)
    n_clusters_ = len(labels_unique)
    
    tableau['cluster'] = ms.labels_
    tableau['Number of Users'] = np.nan
    
    for name, group in tableau.groupby(['cluster']):
        cluster_info = {}
        for col in tableau.drop(['User id', 'cluster', 'Number of Users'], axis=1).columns:
            mode_values = group[col].mode()
            if not mode_values.empty:
                common = mode_values.iloc[0]
                cluster_info[col] = common
        cluster_info['Number of Users'] = len(group)  # Ajouter le nombre d'identifiants d'utilisateurs
    
        tableau.loc[tableau['cluster'] == name, 'Number of Users'] = len(group)
    
    tableau = tableau.groupby('cluster').first().reset_index()
    tableau['Number of Users'] = tableau['Number of Users'].astype(int)
    
    tableau = tableau.drop('User id', axis=1)
   
    return tableau



if __name__ == '__main__':
    app.run()
