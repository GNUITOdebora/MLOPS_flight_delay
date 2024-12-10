import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np


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

def preprocess(df):
    # Convertir DEPARTURE_TIME en datetime si nécessaire
    if not pd.api.types.is_datetime64_any_dtype(df['DEPARTURE_TIME']):
        df['DEPARTURE_TIME'] = pd.to_datetime(df['DEPARTURE_TIME'], errors='coerce')

    df['DEPARTURE_TIME_HOUR'] = df['DEPARTURE_TIME'].dt.hour
    df['DEPARTURE_TIME_MINUTE'] = df['DEPARTURE_TIME'].dt.minute
    df = df.drop(columns=['DEPARTURE_TIME'])

    # Convertir SCHEDULED_ARRIVAL en datetime si nécessaire
    if not pd.api.types.is_datetime64_any_dtype(df['SCHEDULED_ARRIVAL']):
        df['SCHEDULED_ARRIVAL'] = pd.to_datetime(df['SCHEDULED_ARRIVAL'], errors='coerce')

    df['SCHEDULED_ARRIVAL_HOUR'] = df['SCHEDULED_ARRIVAL'].dt.hour
    df['SCHEDULED_ARRIVAL_MINUTE'] = df['SCHEDULED_ARRIVAL'].dt.minute
    df = df.drop(columns=['SCHEDULED_ARRIVAL'])

    # Appliquer le one-hot encoding sur AIRLINE si elle existe
    if 'AIRLINE' in df.columns:
        df = pd.get_dummies(df, columns=['AIRLINE'], dtype=float)

    # Charger l'encodeur sauvegardé
    airport_encoder = pickle.load(open("airport_encoder.pickle", "rb"))

    # Encodage des colonnes ORIGIN_AIRPORT et DESTINATION_AIRPORT
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
