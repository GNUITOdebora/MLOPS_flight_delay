import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np


training_cols=['MONTH', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'DEPARTURE_DELAY',
       'SCHEDULED_TIME', 'SCHEDULED_ARRIVAL', 'AIR_SYSTEM_DELAY',
       'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY',
       'WEATHER_DELAY', 'DEPARTURE_TIME_HOUR', 'DEPARTURE_TIME_MINUTE',
       'AIRLINE_AA', 'AIRLINE_AS', 'AIRLINE_B6', 'AIRLINE_DL', 'AIRLINE_EV',
       'AIRLINE_F9', 'AIRLINE_HA', 'AIRLINE_MQ', 'AIRLINE_NK', 'AIRLINE_OO',
       'AIRLINE_UA', 'AIRLINE_US', 'AIRLINE_VX', 'AIRLINE_WN']


def fix_missing_cols(training_cols, new_data):
    missing_cols = set(training_cols) - set(new_data.columns)
     # Add a missing column in test set with default value equal to 0
    for c in missing_cols:
        new_data[c] = 0
    # Ensure the order of column in the test set is in the same order than in train set
    new_data = new_data[training_cols]
    return new_data


def preprocess(df):
    
    
    # 5. Convertir la colonne DEPARTURE_TIME en format horaire
    
    df['DEPARTURE_TIME_HOUR'] = df['DEPARTURE_TIME'].dt.hour
    df['DEPARTURE_TIME_MINUTE'] = df['DEPARTURE_TIME'].dt.minute

    # 6. Supprimer la colonne DEPARTURE_TIME originale
    df = df.drop(columns=['DEPARTURE_TIME'])


    df['SCHEDULED_ARRIVAL_HOUR'] = df['SCHEDULED_ARRIVAL'].dt.hour
    df['SCHEDULED_ARRIVAL_MINUTE'] = df['SCHEDULED_ARRIVAL'].dt.minute

    # 6. Supprimer la colonne DEPARTURE_TIME originale
    df = df.drop(columns=['SCHEDULED_ARRIVAL'])


    # 7. Appliquer le one-hot encoding sur la colonne AIRLINE
    df_encoded = pd.get_dummies(df, columns=['AIRLINE'], dtype=float)

    

    # Charger l'encodeur sauvegardé
    airport_encoder=pickle.load(open("airport_encoder.pickle","rb"))
    # Encodage des nouvelles données
    try:
        df_encoded['ORIGIN_AIRPORT'] = airport_encoder.transform([df_encoded['ORIGIN_AIRPORT']])[0]
    except ValueError:
        df_encoded['ORIGIN_AIRPORT'] = -1  # Valeur inconnue

    try:
        df_encoded['DESTINATION_AIRPORT'] = airport_encoder.transform([df_encoded['DESTINATION_AIRPORT']])[0]
    except ValueError:
        df_encoded['DESTINATION_AIRPORT'] = -1  # Valeur inconnue

    dummy_cols = ['AIRLINE']
    df = pd.get_dummies(df, columns=dummy_cols, dtype= float)
    df = fix_missing_cols(training_cols,df)

    print("Données encodées :", df_encoded)


    return df_encoded
