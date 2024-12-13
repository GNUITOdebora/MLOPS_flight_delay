


import pandas as pd
import pickle
import numpy as np
import requests



training_cols=['MONTH', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'DEPARTURE_DELAY',
       'SCHEDULED_TIME', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
       'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY', 'DEPARTURE_TIME_HOUR',
       'DEPARTURE_TIME_MINUTE', 'SCHEDULED_ARRIVAL_HOUR',
       'SCHEDULED_ARRIVAL_MINUTE', 'AIRLINE_AA', 'AIRLINE_AS', 'AIRLINE_B6',
       'AIRLINE_DL', 'AIRLINE_EV', 'AIRLINE_F9', 'AIRLINE_HA', 'AIRLINE_MQ',
       'AIRLINE_NK', 'AIRLINE_OO', 'AIRLINE_UA', 'AIRLINE_US', 'AIRLINE_VX',
       'AIRLINE_WN']


def fix_missing_cols(training_cols, new_data):
    missing_cols = set(training_cols) - set(new_data.columns)
     # Add a missing column in test set with default value equal to 0
    for c in missing_cols:
        new_data[c] = 0
    # Ensure the order of column in the test set is in the same order than in train set
    new_data = new_data[training_cols]
    return new_data

def load_airport_encoder_from_git(url):
    """
    Charge l'encodeur des aéroports directement depuis l'URL donnée.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return pickle.loads(response.content)
    else:
        raise ValueError(f"Unable to fetch file. HTTP Status Code: {response.status_code}")



def clean_data_csv(df):


     # 1. Sélectionner les colonnes pertinentes
    df = df[['MONTH', 'AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 
             'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'SCHEDULED_TIME', 
             'SCHEDULED_ARRIVAL', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY',
             'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']]

    # 2. Remplacer les valeurs manquantes par 0 pour les colonnes de délai
    delay_columns = ['AIRLINE_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 
                     'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
    for col in delay_columns:
        df[col] = df[col].fillna(0)
     
   # 3. Remplacer les valeurs manquantes des colonnes spécifiques par le mode par AIRLINE
    columns = ['DEPARTURE_TIME', 'DEPARTURE_DELAY', 'SCHEDULED_TIME']
    for col in columns:
        for airline, group in df.groupby('AIRLINE'):
            most_frequent_value = group[col].mode()[0]
            df.loc[df['AIRLINE'] == airline, col] = df.loc[df['AIRLINE'] == airline, col].fillna(most_frequent_value)

    # 4. Convertir la colonne DEPARTURE_TIME,SCHEDULED_ARRIVAL en format horaire
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

    #5 Appliquer le one-hot encoding sur AIRLINE si elle existe
    if 'AIRLINE' in df.columns:
        df = pd.get_dummies(df, columns=['AIRLINE'], dtype=float)

     
    # Charger l'encodeur sauvegardé depuis le git 
    airport_encoder_url = "https://dagshub.com/deb.gnuito/MLOPS/raw/main/notebooks/airport_encoder.pickle"

    try:
        airport_encoder = load_airport_encoder_from_git(airport_encoder_url)
        print("Airport encoder loaded successfully from DAGsHub.")
        print(airport_encoder)
    except ValueError as e:
        print(f"Error loading airport encoder: {e}")

    #6 Encodage des colonnes ORIGIN_AIRPORT et DESTINATION_AIRPORT
    try:
        df['ORIGIN_AIRPORT'] = airport_encoder.transform(df['ORIGIN_AIRPORT'])
    except ValueError:
        df['ORIGIN_AIRPORT'] = -1  # Valeur inconnue

    try:
        df['DESTINATION_AIRPORT'] = airport_encoder.transform(df['DESTINATION_AIRPORT'])
    except ValueError:
        df['DESTINATION_AIRPORT'] = -1  # Valeur inconnue

    # Vérifier les colonnes manquantes et les ajouter
    df = fix_missing_cols(training_cols, df)

    print("Données encodées :", df)

    return df
