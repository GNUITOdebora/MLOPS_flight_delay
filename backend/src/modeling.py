from dotenv import load_dotenv
import os
from data_preprocessing_training import transform_data
import pandas as pd
import mlflow
from treatement import DecisionTreeRegressor
from treatement import XGBRegressor
from treatement import LinearRegression
from treatement import LSTMModel

#Load environement variable (Dagshub credentials)
from dotenv import load_dotenv
load_dotenv("../backend/src/.env")

DagsHub_username = os.getenv("DAGHUB_USERNAME")
DagsHub_token=os.getenv("DAGHUB_PASSWORD")
os.environ['MLFLOW_TRACKING_USERNAME']= DagsHub_username
os.environ['MLFLOW_TRACKING_PASSWORD'] = DagsHub_token


#setup mlflow
mlflow.set_tracking_uri('https://dagshub.com/deb.gnuito/MLOPS.mlflow') #your mlfow tracking uri
mlflow.set_experiment("flight-delay-experiment")

#Data Url and version
version = "v2.0"
data_url = "../../dataGit/flight2.csv"

#read the data
df = pd.read_csv(data_url)

#cleaning and preprocessing
X_train,X_test,y_train,y_test = transform_data(df)

#Execute the models with new version of data:
LinearRegression(data_url,version,df,X_train,y_train,X_test,y_test)
XGBRegressor(data_url,version,df,X_train,y_train,X_test,y_test)
DecisionTreeRegressor(data_url,version,df,X_train,y_train,X_test,y_test)
LSTMModel(data_url,version,df,X_train,y_train,X_test,y_test)

