from pathlib import Path
import pickle
import pandas as pd
import sys
from src.clean_data_json import clean_data_json
from src.data_preprocessing_training import preprocess_and_split
import mlflow
#from dotenv import load_dotenv
import os

from dotenv import load_dotenv
load_dotenv("../backend/src/secret.env")

DagsHub_username = os.getenv("DAGHUB_USERNAME")
DagsHub_token=os.getenv("DAGHUB_PASSWORD")
os.environ['MLFLOW_TRACKING_USERNAME']= DagsHub_username
os.environ['MLFLOW_TRACKING_PASSWORD'] = DagsHub_token




#setup mlflow
mlflow.set_tracking_uri('https://dagshub.com/deb.gnuito/MLOPS.mlflo') #your mlfow tracking uri


#tests if the model works as expected

def test_model_use():

    #let's call the model from the model registry ( in production stage)

    all_experiments = [exp.experiment_id for exp in mlflow.search_experiments()]
    df_mlflow = mlflow.search_runs(experiment_ids=all_experiments,filter_string="metrics.R2_Score <1")
    run_id = df_mlflow.loc[df_mlflow['metrics.R2_Score'].idxmax()]['run_id']


    logged_model = f'runs:/{run_id}/ML_models'

    # Load model as a PyFuncModel.
    model = mlflow.pyfunc.load_model(logged_model)


    
    d= {
                "MONTH": 11,
                "ORIGIN_AIRPORT": "JFK",
                "DESTINATION_AIRPORT": "LAX",
                "DEPARTURE_DELAY": 15.2,
                "SCHEDULED_TIME": 120.5,
                "AIR_SYSTEM_DELAY": 5.0,
                "SECURITY_DELAY": 2.0,
                "AIRLINE_DELAY": 10.0,
                "LATE_AIRCRAFT_DELAY": 8.0,
                "WEATHER_DELAY": 0.5,
                "DEPARTURE_TIME": "2024-05-14T08:30:00",
                "SCHEDULED_ARRIVAL": "2024-05-14T10:30:00",
                "AIRLINE": "AA"
            }

    


    df = pd.DataFrame(data=d,index=[0])
    dd = clean_data_json(df)
    predict_result = model.predict(dd)
    print(predict_result[0])
