import pandas as pd
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import mlflow
from src.clean_data_csv import clean_data_csv
from src.clean_data_json import clean_data_json
from example_json.flight_info import FlightDataModel
import os
import mlflow.pyfunc

os.environ['MLFLOW_TRACKING_USERNAME']= "deb.gnuito"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "#Dagshub2001"


"""
from dotenv import load_dotenv
import os
load_dotenv("../backend/src/secret.env")

DagsHub_username = os.getenv("DAGHUB_USERNAME")
DagsHub_token=os.getenv("DAGHUB_PASSWORD")
os.environ['MLFLOW_TRACKING_USERNAME']= DagsHub_username
os.environ["MLFLOW_TRACKING_PASSWORD"] = DagsHub_token
"""

#setup mlflow
mlflow.set_tracking_uri('https://dagshub.com/deb.gnuito/MLOPS.mlflow') #your mlfow tracking uri


app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#let's call the model from the model registry ( in production stage)

df_mlflow=mlflow.search_runs(filter_string="metrics.R2_Score < 1")
run_id = df_mlflow.loc[df_mlflow['metrics.R2_Score'].idxmax()]['run_id']



logged_model = f'runs:/{run_id}/ML_models'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

@app.get("/")
def read_root():
    return {"Hello": "to flight delay prediction app version 2"}

# this endpoint receives data in the form of csv file (histotical transactions data)
@app.post("/predict/csv")
def return_predictions(file: UploadFile = File(...)):
    data = pd.read_csv(file.file)
    preprocessed_data = clean_data_csv(data)
    predictions = model.predict(preprocessed_data)
    return {"predictions": predictions.tolist()}


# this endpoint receives data in the form of json (informations about one transaction)
@app.post("/predict")
def predict(data : FlightDataModel):
    received = data.dict()
    df =  pd.DataFrame(received,index=[0])
    preprocessed_data = clean_data_json(df)
    print(preprocessed_data)
    predictions = model.predict(preprocessed_data)
    return {"predictions": predictions.tolist()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

