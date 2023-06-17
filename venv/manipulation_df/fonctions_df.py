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




# !/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


def supprimer_lignes_utilisateur_repete(dataframe):
    # Supprimer les lignes répétées en conservant uniquement la première occurrence de chaque identifiant d'utilisateur
    dataframe_unique = dataframe.drop_duplicates(subset='User id', keep='first')
    # Retourner le DataFrame sans les lignes répétées
    return dataframe_unique

def supprimer_lignes_utilisateur_repete(dataframe):
    if 'User id' in dataframe.columns:
        # Remove duplicate rows based on 'User id' column
        dataframe_unique = dataframe.drop_duplicates(subset=['User id'], keep='first')
    else:
        # 'User id' column doesn't exist, return the original DataFrame
        dataframe_unique = dataframe
    return dataframe_unique




# In[3]:



def lecture_fichier(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("current_dir: " + current_dir)
    path = os.path.join(current_dir, filename)
    if filename.lower().endswith('.csv'):
        dataframe = pd.read_csv(path, delimiter=',')  
        dataframe = dataframe.drop(['S.No', 'Created at', 'Updated at'], axis=1)
        dataframe = supprimer_lignes_utilisateur_repete(dataframe)
    return dataframe



# In[4]:


def jointure():
    
    servir = lecture_fichier(r'C:\Users\user\Downloads\Backend-main\Backend-main\venv\data\servir.csv')
    profil = lecture_fichier(r'C:\Users\user\Downloads\Backend-main\Backend-main\venv\data\profil.csv')
    queney = lecture_fichier(r'C:\Users\user\Downloads\Backend-main\Backend-main\venv\data\queney.csv')

    try:
        df = pd.merge(servir, queney, on='User id', suffixes=('', ' '))
        df = pd.merge(df, profil, on='User id', suffixes=('', '  '))
        df.insert(0, 'User id', df.pop('User id'))
        print ("jointure df => "+df)
        return df
    except KeyError as e:
        print("KeyError: " + str(e))
        return None



# In[5]:



def lecture_dictionnaire(filename):
    venv_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(venv_dir, 'data')
    path = os.path.join(data_dir, filename)
    dictionnaire = {}
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        dictionnaire = ast.literal_eval(content)
    return dictionnaire








# In[6]:


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


# In[7]:


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


# In[8]:


def compatible_columns_lignes(df):
    for i in range(df.shape[0]):
        dictionnaire = lecture_dictionnaire('dic.txt')
        result = compatible_columns(df.iloc[i], dictionnaire)
        if result is not None and result[0] == True:
            return result[0], result[1]
    # Gérer le cas où aucune valeur compatible n'est trouvée
    return False, None



# In[9]:


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


# In[10]:


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


# In[11]:


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


# In[12]:


def rechercher_sous_ensemble(dictionnaire_synonymes, reponse):
    for critere, valeurs in dictionnaire_synonymes.items():
        synonymes = valeurs.get('synonymes', {})
        for sous_ensemble, liste_synonymes in synonymes.items():
            if reponse in liste_synonymes:
                return sous_ensemble
    return None


# In[13]:


def verifier_coherence(reponses, question_colonne, dictionnaire_synonymes):
    for i in range(1, len(reponses)):
        current_reponse = reponses[i]
        previous_reponse = reponses[i - 1]

        ensemble_synonymes_current = rechercher_sous_ensemble(dictionnaire_synonymes, current_reponse)
        ensemble_synonymes_previous = rechercher_sous_ensemble(dictionnaire_synonymes, previous_reponse)

        if ensemble_synonymes_current is None or ensemble_synonymes_previous is None or ensemble_synonymes_current != ensemble_synonymes_previous:
            return False

    return True


# In[14]:





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


# In[15]:


def remplir(df, dictionnaire_synonymes):
    for index, row in df.iterrows():
        reponses = creer_liste_reponses_ligne(row, dictionnaire_synonymes.keys())
        nbre_col = 0
        for reponse in reponses:
            for colonne in df.columns[nbre_col + 1:]:
                nbre_col += 1
                if colonne.endswith('Qualification'):
                    qualification_colonne = colonne
                    question_colonne = colonne[:-14]
                    if question_colonne == 'Sport':
                        if len(mots_repetes(reponse)) != 0:
                            df.at[index, qualification_colonne] = 'Cohérent'
                            df.at[index, question_colonne] = ", ".join(mots_repetes(reponse))
                        else:
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        break
                    elif question_colonne in ['Permis de conduire', 'Motorisé']:
                        is_coherent = verifier_coherence(reponse, question_colonne, dictionnaire_synonymes)
                        if (is_coherent or all(element == reponse[0] for element in reponse)) and (
                                row['Age'] == 'moins 18 an'):
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        elif is_coherent or all(element == reponse[0] for element in reponse):
                            df.at[index, qualification_colonne] = 'Cohérent'
                            df.at[index, question_colonne] = reponse[0]
                        else:
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        break
                    else:
                        is_coherent = verifier_coherence(reponse, question_colonne, dictionnaire_synonymes)
                        if is_coherent or all(element == reponse[0] for element in reponse):
                            df.at[index, qualification_colonne] = 'Cohérent'
                            df.at[index, question_colonne] = reponse[0]
                        else:
                            df.at[index, qualification_colonne] = 'Incohérent'
                            df.at[index, question_colonne] = None
                        break
            continue

    return df


# In[16]:
def transformer_donnees(df, liste1, liste2):
    dff = df[['User id']].copy()
    
    for key, values in liste1.items():
        if key not in dff.columns:
            for value in values:
                dff.loc[:, value] = df[value]
            dff.loc[:, key + ' Qualification'] = 'Qualification'
            dff.loc[:, key] = key
    
    for key, values in liste2.items():
        if key in liste1.keys():
            for value in values:
                if value not in dff.columns:
                    dff.loc[:, value] = df[value]
        else:
            for value in values:
                if value not in dff.columns:
                    dff.loc[:, value] = df[value]
            dff.loc[:, key + ' Qualification'] = 'Qualification'
            dff.loc[:, key] = key
    
    return dff


def fusionner_donnees(dataframe, dff, liste1, liste2):
    for key in liste1.keys():
        dataframe = pd.merge(dataframe, dff[['User id', key]], on='User id')
    
    for key in liste2.keys():
        if key not in dataframe.columns:
            dataframe = pd.merge(dataframe, dff[['User id', key]], on='User id')
    return dataframe

def obtenir_df_final(dataframe, df, liste1, liste2):
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
    
    df_final = pd.merge(dataframe, df, on='User id')
    
    return df_final

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


# In[17]:


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


