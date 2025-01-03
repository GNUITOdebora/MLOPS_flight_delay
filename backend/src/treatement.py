import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import xgboost as xgb
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
warnings.filterwarnings("ignore")

def LinearRegression(data_url,version,df,X_train,y_train,X_test,y_test):
    # disable autologging
    mlflow.sklearn.autolog(disable=True)
    with mlflow.start_run(run_name='LinearRegression'):
        mlflow.log_param("data_url",data_url)
        mlflow.log_param("data_version",version)
        mlflow.log_param("input_rows",df.shape[0])
        mlflow.log_param("input_cols",df.shape[1])
        #model fitting and training
        lr=LinearRegression()
        mlflow.set_tag(key= "model",value="LinearRegression")
        params = lr.get_params()
        mlflow.log_params(params)
        lr.fit(X_train,y_train)
        train_features_name = f'{X_train=}'.split('=')[0]
        train_label_name = f'{y_train=}'.split('=')[0]
        mlflow.set_tag(key="train_features_name",value= train_features_name)
        mlflow.set_tag(key= "train_label_name",value=train_label_name)
        predicted=lr.predict(X_test)

            # Calcul des métriques
        mse = mean_squared_error(y_test, predicted)
        mae = mean_absolute_error(y_test, predicted)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predicted)

        # Enregistrement des métriques
        mlflow.log_metric("MSE", mse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE",  rmse)
        mlflow.log_metric("R2_Score", r2)

        # Enregistrer le modèle
        mlflow.sklearn.log_model(lr, artifact_path="ML_models")

def XGBRegressor(data_url,version,df,X_train,y_train,X_test,y_test):
    # disable autologging
    mlflow.sklearn.autolog(disable=True)
    with mlflow.start_run(run_name='XGBRegressor'):
        mlflow.log_param("data_url",data_url)
        mlflow.log_param("data_version",version)
        mlflow.log_param("input_rows",df.shape[0])
        mlflow.log_param("input_cols",df.shape[1])
        #model fitting and training
        best_param= {'subsample': 0.6, 'n_estimators': 200, 
                     'max_depth': 7, 'learning_rate': 0.1,
                    'gamma': 0.2, 'colsample_bytree': 0.8}
        
        xgb = xgb.XGBRegressor(**best_param, random_state=42)
        mlflow.set_tag(key= "model",value="XGBRegressor")
        params = xgb.get_params()
        mlflow.log_params(params)
        xgb.fit(X_train,y_train)
        train_features_name = f'{X_train=}'.split('=')[0]
        train_label_name = f'{y_train=}'.split('=')[0]
        mlflow.set_tag(key="train_features_name",value= train_features_name)
        mlflow.set_tag(key= "train_label_name",value=train_label_name)
        predicted=xgb.predict(X_test)

            # Calcul des métriques
        mse = mean_squared_error(y_test, predicted)
        mae = mean_absolute_error(y_test, predicted)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predicted)

        # Enregistrement des métriques
        mlflow.log_metric("MSE", mse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE",  rmse)
        mlflow.log_metric("R2_Score", r2)

        # Enregistrer le modèle
        mlflow.sklearn.log_model(xgb, artifact_path="ML_models")

def DecisionTreeRegressor(data_url,version,df,X_train,y_train,X_test,y_test):
    # disable autologging
    mlflow.sklearn.autolog(disable=True)
    with mlflow.start_run(run_name='DecisionTreeRegressor'):
        mlflow.log_param("data_url",data_url)
        mlflow.log_param("data_version",version)
        mlflow.log_param("input_rows",df.shape[0])
        mlflow.log_param("input_cols",df.shape[1])
        #model fitting and training
        Decision_Tree = DecisionTreeRegressor(random_state=42)
        mlflow.set_tag(key= "model",value="Decision_Tree")
        params = Decision_Tree.get_params()
        mlflow.log_params(params)
        Decision_Tree.fit(X_train,y_train)
        train_features_name = f'{X_train=}'.split('=')[0]
        train_label_name = f'{y_train=}'.split('=')[0]
        mlflow.set_tag(key="train_features_name",value= train_features_name)
        mlflow.set_tag(key= "train_label_name",value=train_label_name)
        predicted=Decision_Tree.predict(X_test)

            # Calcul des métriques
        mse = mean_squared_error(y_test, predicted)
        mae = mean_absolute_error(y_test, predicted)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predicted)

        # Enregistrement des métriques
        mlflow.log_metric("MSE", mse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE",  rmse)
        mlflow.log_metric("R2_Score", r2)

        # Enregistrer le modèle
        mlflow.sklearn.log_model(Decision_Tree, artifact_path="ML_models")

def LSTMModel(data_url, version, df, X_train, y_train, X_test, y_test):
    # Désactiver l'autologging de MLflow pour éviter les conflits
    mlflow.keras.autolog(disable=True)

    with mlflow.start_run(run_name='LSTM_Model'):
        # Enregistrer les paramètres
        mlflow.log_param("data_url", data_url)
        mlflow.log_param("data_version", version)
        mlflow.log_param("input_rows", df.shape[0])
        mlflow.log_param("input_cols", df.shape[1])

        # Créer et entraîner le modèle LSTM
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=False, input_shape=(X_train.shape[1], 1)))  # LSTM
        model.add(Dense(units=1))  # Couche de sortie

        model.compile(optimizer='adam', loss='mean_squared_error')

        # Enregistrer les hyperparamètres
        mlflow.set_tag(key="model", value="LSTM")
        params = {"units": 50, "optimizer": "adam", "loss": "mean_squared_error"}
        mlflow.log_params(params)

        # Entraîner le modèle
        model.fit(X_train, y_train, epochs=4, batch_size=128, verbose=1)

        # Enregistrer les noms des caractéristiques d'entrée et de sortie
        train_features_name = f'{X_train=}'.split('=')[0]
        train_label_name = f'{y_train=}'.split('=')[0]
        mlflow.set_tag(key="train_features_name", value=train_features_name)
        mlflow.set_tag(key="train_label_name", value=train_label_name)

        # Prédictions sur le jeu de test
        predictions = model.predict(X_test)

        # Calcul des métriques
        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)

        # Enregistrer les métriques dans MLflow
        mlflow.log_metric("MSE", mse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("R2_Score", r2)

        # Enregistrer le modèle LSTM dans MLflow
        mlflow.keras.log_model(model, artifact_path="ML_models")

