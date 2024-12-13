import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np

import os
import subprocess

def git_push(file_path, commit_message):
    try:
        # Vérifier l'état de Git
        status_result = subprocess.run(["git", "status", "--porcelain"], check=True, stdout=subprocess.PIPE, text=True)
        if file_path not in status_result.stdout:
            print(f"Aucun changement détecté pour {file_path}.")
            return
        
        # Ajouter le fichier au staging area
        subprocess.run(["git", "add", file_path], check=True)

        # Effectuer le commit
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push vers le dépôt
        subprocess.run(["git", "push"], check=True)

        print("Fichier poussé avec succès sur le dépôt Git.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution des commandes Git : {e}")



def preprocess_and_split(df):
    # 1. Sélectionner les colonnes pertinentes
    df = df[['MONTH', 'AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 
             'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'SCHEDULED_TIME', 'CANCELLATION_REASON',
             'DIVERTED', 'CANCELLED', 'SCHEDULED_ARRIVAL', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY',
             'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY', 'ARRIVAL_DELAY']]

    # 2. Remplacer les valeurs manquantes par 0 pour les colonnes de délai
    delay_columns = ['AIRLINE_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 
                     'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
    for col in delay_columns:
        df[col] = df[col].fillna(0)

    # 3. Supprimer les colonnes inutiles
    columns_to_drop = ['CANCELLATION_REASON', 'CANCELLED', 'DIVERTED']
    df = df.drop(columns=columns_to_drop)

    # 4. Remplacer les valeurs manquantes des colonnes spécifiques par le mode par AIRLINE
    columns = ['DEPARTURE_TIME', 'DEPARTURE_DELAY', 'SCHEDULED_TIME', 'ARRIVAL_DELAY']
    for col in columns:
        for airline, group in df.groupby('AIRLINE'):
            most_frequent_value = group[col].mode()[0]
            df.loc[df['AIRLINE'] == airline, col] = df.loc[df['AIRLINE'] == airline, col].fillna(most_frequent_value)

    # 5. Convertir la colonne DEPARTURE_TIME,SCHEDULED_ARRIVAL en format horaire
    def convert_to_datetime(time_float):
        if pd.isna(time_float):
            return time_float
        hours = int(time_float // 100)
        minutes = int(time_float % 100)
        if hours == 24:
            hours = 0
            minutes = 0
        return pd.to_datetime(f'{hours:02d}:{minutes:02d}', format='%H:%M')

    df['DEPARTURE_TIME'] = df['DEPARTURE_TIME'].apply(lambda x: convert_to_datetime(x))
    df['DEPARTURE_TIME_HOUR'] = df['DEPARTURE_TIME'].dt.hour
    df['DEPARTURE_TIME_MINUTE'] = df['DEPARTURE_TIME'].dt.minute

    # Supprimer la colonne DEPARTURE_TIME originale
    df = df.drop(columns=['DEPARTURE_TIME'])

    df['SCHEDULED_ARRIVAL'] = df['SCHEDULED_ARRIVAL'].apply(lambda x: convert_to_datetime(x))
    df['SCHEDULED_ARRIVAL_HOUR'] = df['SCHEDULED_ARRIVAL'].dt.hour
    df['SCHEDULED_ARRIVAL_MINUTE'] = df['SCHEDULED_ARRIVAL'].dt.minute

    # Supprimer la colonne SCHEDULED_ARRIVAL originale
    df = df.drop(columns=['SCHEDULED_ARRIVAL'])

    # Convertir les colonnes ORIGIN_AIRPORT et DESTINATION_AIRPORT en chaînes
    df['ORIGIN_AIRPORT'] = df['ORIGIN_AIRPORT'].astype(str)
    df['DESTINATION_AIRPORT'] = df['DESTINATION_AIRPORT'].astype(str)

    # Appliquer le one-hot encoding sur la colonne AIRLINE
    df_encoded = pd.get_dummies(df, columns=['AIRLINE'], dtype=float)

    # Combiner les deux colonnes pour créer un encodage unique
    airports = np.unique(df_encoded['ORIGIN_AIRPORT'].values.tolist() + df_encoded['DESTINATION_AIRPORT'].values.tolist())

    # Créer un LabelEncoder pour les aéroports
    airport_encoder = LabelEncoder()
    airport_encoder.fit(airports)

    # Encoder les colonnes
    df_encoded['ORIGIN_AIRPORT'] = airport_encoder.transform(df_encoded['ORIGIN_AIRPORT'])
    df_encoded['DESTINATION_AIRPORT'] = airport_encoder.transform(df_encoded['DESTINATION_AIRPORT'])

    # Sauvegarder l'encodeur pour un usage futur
    pickle.dump(airport_encoder, open('airport_encoder.pickle', "wb"))
    # un push automatique sur le git !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    git_push("airport_encoder.pickle", "Nouveau encodeur des aéroports")

    # Séparer les caractéristiques (X) et la variable cible (y)
    X = df_encoded.drop(columns=['ARRIVAL_DELAY'])  # Toutes les colonnes sauf ARRIVAL_DELAY
    y = df_encoded['ARRIVAL_DELAY']  # La variable cible

    # Diviser l'ensemble de données en un ensemble d'entraînement et de test (80% / 20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

