import requests
import streamlit as st 
import pandas as pd 
import datetime 
import json 
import io
st.set_page_config(layout="wide")

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

# Application Styling with a Professional Dashboard Layout

#Title of the application with a banner
st.markdown(""" <h1 style='color: #0086fc;'> ✈️ Flight Delay Predictor ✈️ </h1>  """, unsafe_allow_html=True)

# Sidebar layout with logo and navigation
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQ-_qwPouFTdBd2PRscHdtNoFv_5LEY7eZEA&s", width=400)
app_mode = st.sidebar.radio("Choose page", ["Data Visualization", "Flight Prediction Form", "Upload Historical Data","Team"])

# If user chooses the PDF viewer page (Page 1)
if app_mode == "Data Visualization":
#    st.subheader("View the Power BI PDF Report")

    # Embed the PDF located at 'images/powerBi.pdf'
    st.image("images/powerBi.png", caption="Power BI Report")
    #powerbi_embed_url = "https://app.powerbi.com/links/0SQIpJPIJ8?ctid=dbd6664d-4eb9-46eb-99d8-5c43ba153c61&pbi_source=linkShare"
    #st.button("Ouvrir le rapport Power BI", url="https://app.powerbi.com/links/0SQIpJPIJ8?ctid=dbd6664d-4eb9-46eb-99d8-5c43ba153c61&pbi_source=linkShare")
    if st.button("Ouvrir le rapport Power BI"):
    # Rediriger vers l'URL via st.markdown
        st.markdown(
            f'<a href="https://app.powerbi.com/links/0SQIpJPIJ8?ctid=dbd6664d-4eb9-46eb-99d8-5c43ba153c61&pbi_source=linkShare" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 10px 24px; border: none; cursor: pointer; border-radius: 5px;">Ouvrir le rapport Power BI</button></a>',
            unsafe_allow_html=True
        )
# Application Layout
   # st.title("Power BI Dashboard")
  #  st.markdown("## Embedded Power BI Dashboard")

# Embedding Power BI using iframe
 #   st.markdown(f"""<iframe width="100%" height="800" src="{powerbi_embed_url}" frameborder="0" allowFullScreen="true"></iframe> """, unsafe_allow_html=True)
# If user chooses the flight prediction form (Page 2)
elif app_mode == "Flight Prediction Form":
    st.subheader("Enter flight details below")

    # Form submission with fields for flight data
    with st.form("flight_form", clear_on_submit=False):
        origin_airport = st.text_input("Origin Airport Code", "JFK")
        destination_airport = st.text_input("Destination Airport Code", "LAX")
        airline_name = st.selectbox("Select Airline", list(airline_mapping.keys()))
        month = st.selectbox("Flight Month", [i for i in range(1, 13)])
        departure_delay = st.text_input("Departure Delay (min)", "0")
        scheduled_time = st.text_input("Scheduled Flight Duration (min)", "180")
        departure_time = st.time_input("Departure Time", datetime.time(12, 0))

        st.markdown("#### Delay Factors")  # Delay factors section
        weather_delay = st.text_input("Weather Delay (min)", "0")
        scheduled_arrival_time = st.time_input("Scheduled Arrival Time", datetime.time(15, 0))
        air_system_delay = st.text_input("Air System Delay (min)", "0")
        security_delay = st.text_input("Security Delay (min)", "0")
        airline_delay = st.text_input("Airline Delay (min)", "0")
        late_aircraft_delay = st.text_input("Late Aircraft Delay (min)", "0")

        # Convert times to datetime objects
        today = datetime.date.today()
        departure_datetime = datetime.datetime.combine(today, departure_time)
        scheduled_arrival_datetime = datetime.datetime.combine(today, scheduled_arrival_time)

        # Airline code (IATA)
        airline_code = airline_mapping[airline_name]

        # Data to be sent to the API
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
            "AIRLINE": airline_code
        }

        submit = st.form_submit_button("Submit")

        if submit:
            # Send data to the API
            res = requests.post("http://172.17.0.2:8080/predict", data=json.dumps(dd))

            if res.status_code == 200:
                predictions = res.json().get("predictions")

                if predictions:
                    time_msg = f"{predictions[0]} minutes"
                    if predictions[0] > 60:
                        hours, minutes = divmod(predictions[0], 60)
                        time_msg = f"{hours} hour(s) and {minutes} minute(s)"

                    # Show result based on delay prediction
                    if predictions[0] < 0:
                        st.success(f"Flight is expected to arrive early by {predictions[0]} min.")
                    elif 0 <= predictions[0] <= 5:
                        st.info("Flight is on time.")
                    elif 6 <= predictions[0] <= 20:
                        st.warning(f"Flight delay: {time_msg}.")
                    else:
                        st.error(f"Flight delay: {time_msg}.")

                    # Create a table with the entered values
                    flight_data = {
                        "Origin Airport": [origin_airport],
                        "Destination Airport": [destination_airport],
                        "Airline": [airline_name],
                        "Month": [month],
                        "Departure Delay": [departure_delay],
                        "Scheduled Flight Duration": [scheduled_time],
                        "Departure Time": [departure_time],
                        "Weather Delay": [weather_delay],
                        "Scheduled Arrival Time": [scheduled_arrival_time],
                        "Air System Delay": [air_system_delay],
                        "Security Delay": [security_delay],
                        "Airline Delay": [airline_delay],
                        "Late Aircraft Delay": [late_aircraft_delay],
                        "Prediction (min)": [predictions[0]],
                    }

                    df = pd.DataFrame(flight_data)

                    # Apply color styling to predictions
                    def highlight_prediction(val):
                        if val < 0:
                            return 'background-color: lightgreen'
                        elif 0 <= val <= 5:
                            return 'background-color: lightyellow'
                        elif 6 <= val <= 20:
                            return 'background-color: orange'
                        else:
                            return 'background-color: red'

                    styled_df = df.style.map(highlight_prediction, subset=["Prediction (min)"])

                    st.dataframe(styled_df)

                else:
                    st.error("No predictions received.")
            else:
                st.error("Error in prediction request.")

# If user selects the CSV file upload page (Page 3)
elif app_mode == "Upload Historical Data":
    st.subheader("Upload your historical transactions CSV file")

    # Display file uploader widget
    data = st.file_uploader("Choose a CSV file", type="csv")
    if data is None:
        st.warning("No file uploaded. Using default file for prediction.")
        
        # Charger un fichier CSV par défaut
        default_file_path = "test_file_upload/test_flight_data.csv"  # Vous pouvez spécifier le chemin de votre fichier par défaut
        with open(default_file_path, "rb") as f:
            data = io.BytesIO(f.read())
    if data is not None:
        df = pd.read_csv(data)
        st.write("Preview of the uploaded data:")
        st.dataframe(df.head())  # Preview of the uploaded CSV data

        # Send CSV file for prediction
        file = {"file": data.getvalue()}
        res = requests.post("http://172.17.0.2:8080/predict/csv", files=file)

        if res.status_code == 200:
            predictions = res.json().get("predictions")
            
            # Add the prediction column to the DataFrame
            if predictions:
                df['Prediction'] = predictions  # Add the prediction column to the DataFrame

                # Apply color styling to the prediction column (green background for predictions)
                def highlight_prediction(val):
                    return 'background-color: lightred' if val >= 0 else 'background-color: lightgreen'  # Green for non-negative predictions

                # Apply the style to the prediction column
                styled_df = df.style.map(highlight_prediction, subset=["Prediction"])

                st.write("Data with predictions:")
                st.dataframe(styled_df)  # Display the DataFrame with highlighted predictions
            else:
                st.error("No predictions received.")
        else:
            st.error("Failed to get predictions for the CSV data.")
# If user selects the Team page (Page 4)
elif app_mode == "Team":
    st.subheader("Team Members Information")


    # URLs des photos des membres
    photo1_url = "https://media.licdn.com/dms/image/v2/D4D03AQHzhvWZztFG9g/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1718304956444?e=1739404800&v=beta&t=ski81m2dkmGQM45-5GEKyy1sx00X5CnXg--G26VK0bU"
    photo2_url = "https://media.licdn.com/dms/image/v2/D5603AQGUFtCpihVUbw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1709069836403?e=1739404800&v=beta&t=HZWt4rcBFsc5ZAnQPOdeRkzHFBkrao86W2nNC58yAhY"


    # Affichage des photos côte à côte avec leurs noms en dessous
    col1,col2,col3,col4= st.columns(4)  # Créez deux colonnes pour afficher les photos côte à côte
    with col2:
        st.subheader(" ")
        st.image(photo1_url, width=350)
        st.markdown("Moheddine BEN ABDALLAH -I3-FSS")

    with col3:
        st.subheader(" ")
        st.image(photo2_url, width=350)
        st.markdown("Débora GNUITO -I3-FSS")
