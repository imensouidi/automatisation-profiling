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

app=Flask(__name__)
CORS(app)





#supprimer les lignes des utilisateurs qui se repetent
def supprimer_lignes_utilisateur_repete(dataframe):
    if 'User id' in dataframe.columns:
        # Remove duplicate rows based on 'User id' column
        dataframe_unique = dataframe.drop_duplicates(subset=['User id'], keep='first')
    else:
        # 'User id' column doesn't exist, return the original DataFrame
        dataframe_unique = dataframe
    return dataframe_unique




#lire un fichier
def lecture_fichier(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("current_dir: " + current_dir)
    path = os.path.join(current_dir, filename)
    if filename.lower().endswith('.csv'):
        dataframe = pd.read_csv(path, delimiter=',')  
        dataframe = dataframe.drop(['S.No', 'Created at', 'Updated at'], axis=1)
        dataframe = supprimer_lignes_utilisateur_repete(dataframe)
    return dataframe


# Fonction pour obtenir le chemin correct vers `data/`
def get_data_path(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Récupère `Backend-main/`
    return os.path.join(base_dir, "data", filename)

def jointure():
    servir = pd.read_csv(get_data_path("servir.csv"), delimiter=',')
    profil = pd.read_csv(get_data_path("profil.csv"), delimiter=',')
    queney = pd.read_csv(get_data_path("queney.csv"), delimiter=',')

    try:
        df = pd.merge(servir, queney, on='User id', suffixes=('', ' '))
        df = pd.merge(df, profil, on='User id', suffixes=('', '  '))
        df.insert(0, 'User id', df.pop('User id'))
        print("jointure df => \n", df)
        return df
    except KeyError as e:
        print("KeyError:", e)
        return None

#lecture du dictionnaire créé
def lecture_dictionnaire(filename):
    venv_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(venv_dir, 'data')
    path = os.path.join(data_dir, filename)
    dictionnaire = {}
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        dictionnaire = ast.literal_eval(content)
    return dictionnaire








#normaliser la dataframe
def normaliser(df):
    # Télécharger les ensembles de données nécessaires
    nltk.download('stopwords')
    nltk.download('wordnet')

    # Normaliser les noms de colonnes en minuscules et enlever la ponctuation
    print("normaliser df => " , df)
    df = df.applymap(lambda x: x.lower().translate(str.maketrans('', '', string.punctuation)) if type(x) == str else x)
    # Définir les stopwords et initialiser le lemmatizer
    stop_words = set(stopwords.words('french'))
    lemmatizer = WordNetLemmatizer()

    # Fonction pour lemmatiser les mots et enlever les stopwords
    def preprocess(text):
        if isinstance(text, str):
            words = text.split()
            words = [lemmatizer.lemmatize(word, pos='n') for word in words if word not in stop_words]
            return ' '.join(words)
        else:
            return text

    # Appliquer la fonction de prétraitement sur les noms de colonnes
    df = df.applymap(preprocess)
    return df

#supprimer la normalisation effectuée
def supprimer_normalisation(df_original, df_normalise):
    # Restaurer les noms de colonnes d'origine
    df_normalise.columns = df_original.columns

    # Supprimer les modifications de normalisation
    df_normalise = df_normalise.applymap(lambda x: x.upper() if type(x) == str else x)

    return df_normalise

#rechercher les colonnes qui contiennent des questions qui demandent des informations sur le même critere
def compatible_columns(row, synonym_dict):
    compatible_columns = {}
    for col in row.index:
        value = row[col]
        if isinstance(value, str):  # Vérifier si la valeur est une chaîne de caractères
            words = value.split()
            for critere, details in synonym_dict.items():
                similarite = details.get('similarite', [])
                synonymes = details.get('synonymes', {})
                if any(synonyme in words for synonyme in similarite):
                    if critere not in compatible_columns:
                        compatible_columns[critere] = [col]
                    else:
                        compatible_columns[critere].append(col)
                else:
                    for synonyme, synonyme_values in synonymes.items():
                        if any(syn in words for syn in synonyme_values):
                            if critere not in compatible_columns:
                                compatible_columns[critere] = [col]
                            else:
                                compatible_columns[critere].append(col)

    if compatible_columns:
        return True, compatible_columns

    return False, None

#utiliser la fonction précedente pour l'appliquer à chaque ligne 
def compatible_columns_lignes(df):
    for i in range(df.shape[0]):
        dictionnaire = lecture_dictionnaire('dic.txt')
        result = compatible_columns(df.iloc[i], dictionnaire)
        if result is not None and result[0] == True:
            return result[0], result[1]
    # Gérer le cas où aucune valeur compatible n'est trouvée
    return False, None



#extraction des colonnes qui demande le club préféré
def extraire_colonnes_club(df):
    colonnes_club = []

    # Recherche des colonnes contenant 'club' dans leur nom
    for colonne in df.columns:
        if 'club' in colonne.lower():
            colonnes_club.append(colonne)

    # Recherche des colonnes contenant 'club' dans certaines lignes
    for colonne in df.columns:
        for valeur in df[colonne]:
            if isinstance(valeur, str) and 'club' in valeur.lower() and colonne not in colonnes_club:
                colonnes_club.append(colonne)
                break

    # Création d'un nouveau DataFrame avec les colonnes extraites
    df_club = df[colonnes_club]

    return df_club


#Fonction qui permet l'affichage pour chaque critere les questions correspondantes
def compatible_columns_colonnes(df, synonym_dict):
    compatible_columns = {}
    for col in df.columns:
        value = str(col)
        words = value.split()
        for critere, details in synonym_dict.items():
            similarite = details["similarite"]
            synonymes = details["synonymes"]
            if any(synonyme in words for synonyme in similarite):
                if critere not in compatible_columns:
                    compatible_columns[critere] = [col]
                else:
                    compatible_columns[critere].append(col)
            for syn, syn_values in synonymes.items():
                if any(syn_value in words for syn_value in syn_values):
                    if critere not in compatible_columns:
                        compatible_columns[critere] = [col]
                    else:
                        compatible_columns[critere].append(col)

    if compatible_columns:
        return compatible_columns

    return None


#Renvoyer la liste des réponses d'une ligne avant la colonne critère_Qualification
def creer_liste_reponses_ligne(row, criteres):
    reponses = []
    liste_reponses = []

    for colonne in row.index:
        if colonne.endswith('Qualification'):
            liste_reponses.append(reponses)
            reponses = []
            continue

        if colonne != 'User id' and colonne not in criteres:
            reponses.append(row[colonne])

    liste_reponses.append(reponses)

    return liste_reponses


#rechercher une réponse donnée dans un dictionnaire de synonymes et renvoie le sous-ensemble auquel la réponse appartient
def rechercher_sous_ensemble(dictionnaire_synonymes, reponse):
    for critere, valeurs in dictionnaire_synonymes.items():
        synonymes = valeurs.get('synonymes', {})
        for sous_ensemble, liste_synonymes in synonymes.items():
            if reponse in liste_synonymes:
                return sous_ensemble
    return None


#comparer chaque réponse avec sa précédente et vérifie si elles appartiennent au même sous-ensemble défini dans le dictionnaire
def verifier_coherence(reponses, question_colonne, dictionnaire_synonymes):
    for i in range(1, len(reponses)):
        current_reponse = reponses[i]
        previous_reponse = reponses[i - 1]

        ensemble_synonymes_current = rechercher_sous_ensemble(dictionnaire_synonymes, current_reponse)
        ensemble_synonymes_previous = rechercher_sous_ensemble(dictionnaire_synonymes, previous_reponse)

        if ensemble_synonymes_current is None or ensemble_synonymes_previous is None or ensemble_synonymes_current != ensemble_synonymes_previous:
            return False

    return True


#Compter le nombre d'occurrences de chaque mot, et renvoie une liste des mots qui apparaissent plus d'une fois dans la liste d'origine
def mots_repetes(liste):
    mots_repetes = []
    mots_comptes = Counter()

    for element in liste:
        mots = element.split()
        mots_comptes.update(mots)

    for mot, count in mots_comptes.items():
        if count > 1:
            mots_repetes.append(mot)

    return mots_repetes


#remlir la colonne de qualification par Cohérent ou Incohérent
def remplir(df, dictionnaire_synonymes):
    # Parcourt chaque ligne du DataFrame
    for index, row in df.iterrows():
        # Crée une liste des réponses pour chaque ligne en utilisant les critères du dictionnaire des synonymes
        reponses = creer_liste_reponses_ligne(row, dictionnaire_synonymes.keys())
        nbre_col = 0
        # Parcourt chaque réponse dans la liste des réponses
        for reponse in reponses:
            # Parcourt chaque colonne à partir de la colonne suivante
            for colonne in df.columns[nbre_col + 1:]:
                nbre_col += 1
                # Vérifie si la colonne se termine par 'Qualification'
                if colonne.endswith('Qualification'):
                    qualification_colonne = colonne
                    question_colonne = colonne[:-14]
                    
                    # Cas spécifique pour la question 'Sport'
                    if question_colonne == 'Sport':
                        # Vérifie si des mots sont répétés dans la réponse
                        if len(mots_repetes(reponse)) != 0:
                            # Attribue la qualification 'Cohérent' et les mots répétés à la colonne de qualification et à la colonne de question
                            df.at[index, qualification_colonne] = 'Cohérent'
                            df.at[index, question_colonne] = ", ".join(mots_repetes(reponse))
                        else:
                            # Attribue la qualification 'Incohérent' et aucune valeur à la colonne de qualification et à la colonne de question
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        break
                    
                    # Cas spécifique pour les questions 'Permis de conduire' et 'Motorisé'
                    elif question_colonne in ['Permis de conduire', 'Motorisé']:
                        # Vérifie la cohérence des réponses et des critères spécifiques
                        is_coherent = verifier_coherence(reponse, question_colonne, dictionnaire_synonymes)
                        
                        # Vérifie les conditions pour attribuer les valeurs appropriées aux colonnes de qualification et de question
                        if (is_coherent or all(element == reponse[0] for element in reponse)) and (row['Age'] == 'moins 18 an'):
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        elif is_coherent or all(element == reponse[0] for element in reponse):
                            df.at[index, qualification_colonne] = 'Cohérent'
                            df.at[index, question_colonne] = reponse[0]
                        else:
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        break
                    
                    # Cas général pour les autres questions
                    else:
                        # Vérifie la cohérence des réponses par rapport au critère spécifique
                        is_coherent = verifier_coherence(reponse, question_colonne, dictionnaire_synonymes)
                        
                        # Vérifie les conditions pour attribuer les valeurs appropriées aux colonnes de qualification et de question
                        if is_coherent or all(element == reponse[0] for element in reponse):
                            df.at[index, qualification_colonne] = 'Cohérent'
                            df.at[index, question_colonne] = reponse[0]
                        else:
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        break
            continue

    return df



#Ajout de la colonne Qualification et  Key qui va stocker sa valeur
def transformer_donnees(df, liste1, liste2):
    # Crée une nouvelle DataFrame avec la colonne 'User id' à partir du DataFrame d'origine
    dff = df[['User id']].copy()
    
    # Parcourt les éléments de liste1 
    for key, values in liste1.items():
        # Vérifie si la clé n'est pas déjà présente dans les colonnes de la nouvelle DataFrame
        if key not in dff.columns:
            # Parcourt les valeurs associées à la clé
            for value in values:
                # Copie les colonnes correspondantes depuis le DataFrame d'origine vers la nouvelle DataFrame
                dff.loc[:, value] = df[value]
            
            # Ajoute une colonne de qualification pour la clé et définit sa valeur
            dff.loc[:, key + ' Qualification'] = 'Qualification'
            
            # Définit la valeur de la colonne de la clé dans la nouvelle DataFrame
            dff.loc[:, key] = key
    
    # Parcourt les éléments de liste2 
    for key, values in liste2.items():
        # Vérifie si la clé est déjà présente dans les clés de liste1
        if key in liste1.keys():
            # Parcourt les valeurs associées à la clé
            for value in values:
                # Vérifie si la valeur n'est pas déjà présente dans les colonnes de la nouvelle DataFrame
                if value not in dff.columns:
                    # Copie les colonnes correspondantes depuis le DataFrame d'origine vers la nouvelle DataFrame
                    dff.loc[:, value] = df[value]
        else:
            # Parcourt les valeurs associées à la clé
            for value in values:
                # Vérifie si la valeur n'est pas déjà présente dans les colonnes de la nouvelle DataFrame
                if value not in dff.columns:
                    # Copie les colonnes correspondantes depuis le DataFrame d'origine vers la nouvelle DataFrame
                    dff.loc[:, value] = df[value]
            
            # Ajoute une colonne de qualification pour la clé et définit sa valeur
            dff.loc[:, key + ' Qualification'] = 'Qualification'
            
            # Définit la valeur de la colonne de la clé dans la nouvelle DataFrame
            dff.loc[:, key] = key
    
    # Renvoie la nouvelle DataFrame
    return dff


#Fusionner dataframe et dff en se basant les clés de liste1 et liste2
def fusionner_donnees(dataframe, dff, liste1, liste2):
    for key in liste1.keys():
        dataframe = pd.merge(dataframe, dff[['User id', key]], on='User id')
    
    for key in liste2.keys():
        if key not in dataframe.columns:
            dataframe = pd.merge(dataframe, dff[['User id', key]], on='User id')
    return dataframe

def obtenir_df_final(df, liste1, liste2):
    for cols in liste1.values():
        for col in cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
    
    for cols in liste2.values():
        for col in cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
    data, df = get_common_columns(df)
    while data.shape[1] > 1:
        rt = remplir_common_columns(data)
        df[rt.columns[1]] = rt[rt.columns[-1]]
        data, df = get_common_columns(df)
    
    return df

def get_common_columns(df):
    d = df
    data = d[['User id']]
    for j in range(1, d.shape[1]):
        c = d.columns[j]
        for i in range(j + 1, d.shape[1]):
            if c.rstrip() == d.columns[i].rstrip():
                data[c] = d[c]
                data[d.columns[i]] = d[d.columns[i]]
        if c in data.columns:
            break  # Arrêter la boucle externe si une colonne commune est trouvée
    d = d.drop(data.drop('User id', axis=1).columns, axis=1)
    return data, d



def remplir_common_columns(df):
    columns = df.columns[1:]
    similar_counts = df[columns].eq(df[columns].shift(axis=1)).sum(axis=1)
    df['Valeur'] = np.nan

    for i in range(len(df)):
        if df.iloc[i, 1] == df.iloc[i, 2]:
            df.at[i, 'Valeur'] = df.iloc[i, 1]
        else:
            df.at[i, 'Valeur'] = "None"
          
    
    return df

    




if __name__ == '__main__':
    app.run()


