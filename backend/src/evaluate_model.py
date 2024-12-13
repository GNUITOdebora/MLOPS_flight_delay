from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def evaluate_regression_model(actual, pred):
    # Calculer les métriques
    mae = mean_absolute_error(actual, pred)  # Erreur absolue moyenne
    mse = mean_squared_error(actual, pred)   # Erreur quadratique moyenne
    rmse = np.sqrt(mse)                      # Racine carrée de MSE
    r2 = r2_score(actual, pred)              # Coefficient de détermination (R²)
    
    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R²": r2
    }
