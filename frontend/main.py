import requests
import streamlit as st
import pandas as pd
import datetime
import json

# Dictionnaire de correspondance des compagnies aériennes
airline_mapping = {
    'United Air Lines Inc.': 'UA',
    'American Airlines Inc.': 'AA',
    'US Airways Inc.': 'US',
    'Frontier Airlines Inc.': 'F9',
    'JetBlue Airways': 'B6',
    'Skywest Airlines Inc.': 'OO',
    'Alaska Airlines Inc.': 'AS',
    'Spirit Air Lines': 'NK',
    'Southwest Airlines Co.': 'WN',
    'Delta Air Lines Inc.': 'DL',
    'Atlantic Southeast Airlines': 'EV',
    'Hawaiian Airlines Inc.': 'HA',
    'American Eagle Airlines Inc.': 'MQ',
    'Virgin America': 'VX'
}

# Titre de l'application
st.title("Flight Delay Predictor Web App")
st.subheader("Enter flight details below")


# Création du formulaire avec trois colonnes
col1, col2, col3 = st.columns([3, 1, 3])  # La colonne centrale est plus petite, les autres plus larges

# Définir le formulaire
with st.form("flight_form", clear_on_submit=False):
    with col1:
        origin_airport = st.text_input("Enter Origin Airport Code", "JFK")
        destination_airport = st.text_input("Enter Destination Airport Code", "LAX")
        airline_name = st.selectbox("Select Airline", list(airline_mapping.keys()))
        month = st.selectbox("Select Month of Flight", [i for i in range(1, 13)])
        departure_delay = st.text_input("Departure Delay (in minutes)", "0")
        scheduled_time = st.text_input("Scheduled Flight Duration (in minutes)", "180")
        departure_time = st.time_input("Departure Time", datetime.time(12, 0))

    with col3:
        st.markdown("#### Delay Case")  # Title for the delay case section
        weather_delay = st.text_input("Weather Delay (in minutes)", "0")
        scheduled_arrival_time = st.time_input("Scheduled Arrival Time", datetime.time(15, 0))
        air_system_delay = st.text_input("Air System Delay (in minutes)", "0")
        security_delay = st.text_input("Security Delay (in minutes)", "0")
        airline_delay = st.text_input("Airline Delay (in minutes)", "0")
        late_aircraft_delay = st.text_input("Late Aircraft Delay (in minutes)", "0")

    # Conversion des champs horaires en datetime
    today = datetime.date.today()
    departure_datetime = datetime.datetime.combine(today, departure_time)
    scheduled_arrival_datetime = datetime.datetime.combine(today, scheduled_arrival_time)

    # Obtenir le code IATA de la compagnie aérienne
    airline_code = airline_mapping[airline_name]

    # Préparation des données pour l'API
    dd = {
        "MONTH": month,
        "ORIGIN_AIRPORT": origin_airport,
        "DESTINATION_AIRPORT": destination_airport,
        "DEPARTURE_DELAY": float(departure_delay),
        "SCHEDULED_TIME": float(scheduled_time),
        "AIR_SYSTEM_DELAY": float(air_system_delay),
        "SECURITY_DELAY": float(security_delay),
        "AIRLINE_DELAY": float(airline_delay),
        "LATE_AIRCRAFT_DELAY": float(late_aircraft_delay),
        "WEATHER_DELAY": float(weather_delay),
        "DEPARTURE_TIME": departure_datetime.isoformat(),
        "SCHEDULED_ARRIVAL": scheduled_arrival_datetime.isoformat(),
        "AIRLINE": airline_code  # Envoi du code IATA à l'API
    }

    submit = st.form_submit_button("Submit this form")

    if submit:
        # Envoi des données à l'API pour prédiction en JSON
        res = requests.post("http://172.17.0.2:8080/predict", data=json.dumps(dd))

        if res.status_code == 200:
            predictions = res.json().get("predictions")

            # Calcul du temps de retard/avance
            if predictions is not None:
                if predictions[0] > 60:
                    hours, minutes = divmod(predictions[0], 60)
                    if hours >= 24:
                        days, hours = divmod(hours, 24)
                        time_msg = f"{days} day(s), {hours} hour(s), and {minutes} minute(s)"
                    else:
                        time_msg = f"{hours} hour(s) and {minutes} minute(s)"
                else:
                    time_msg = f"{predictions[0]} minute(s)"

                # Affichage des résultats
                if predictions[0] < 0:
                    st.text(f"The flight is expected to arrive early by {abs(predictions[0])} minute(s). 😃")
                elif 0 <= predictions[0] <= 5:
                    st.text("The flight is expected to be on time. 🕒")
                elif 6 <= predictions[0] <= 20:
                    st.text(f"The flight is expected to have a slight delay of {time_msg}. 🌤")
                elif 21 <= predictions[0] <= 60:
                    st.text(f"The flight is expected to have a significant delay of {time_msg}. 🚨")
                elif predictions[0] > 60:
                    st.text(f"The flight is expected to have a very long delay of {time_msg}. We apologize for the inconvenience. 😔")
            else:
                st.error("No prediction data received.")
        else:
            st.error("Failed to get prediction from the API.")
