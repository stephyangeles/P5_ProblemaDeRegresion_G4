import pickle
import os
import pandas as pd
import numpy as np
from regression.core.config import settings
import regression.core.lw_log as logg
from catboost import CatBoostRegressor
# Rutas a los archivos
MODEL_PATH = settings.model_path
FORM_DATA_PATH = settings.data_path

def load_model():
    model = CatBoostRegressor()
    return model.load_model(MODEL_PATH)

def load_form_data():
    """Carga los datos para el formulario"""
    with open(FORM_DATA_PATH, 'rb') as f:
        return pickle.load(f)

def predict_price(input_data):

    """
    Realiza la predicción del precio del coche
    
    Args:
        input_data: DataFrame con los datos de entrada
        
    Returns:
        float: Precio predicho
    """
    model = load_model()
    input_df = pd.DataFrame(input_data)
    logg.write_log("🔍 Columnas del input_df: " + ", ".join(input_df.columns.tolist()))
    logg.write_log("📦 Columnas que espera el modelo: " + ", ".join(model.feature_names_))
    logg.write_log("📊 Valores del input_df:\n" + str(input_df))
    logg.write_log("Parámetros del modelo: " + str(model.get_params()))


    for col in ['brand', 'model', 'fuel_type', 'accident']:
        input_df[col] = input_df[col].astype(str)

    # Realizar la predicción
    prediction = model.predict(input_df)[0]
    # Asegurarse de que la predicción es un valor único
    if isinstance(prediction, (list, np.ndarray)):
        prediction = prediction[0]
    
    # Limitar a un rango razonable (como en el notebook)
    prediction = np.clip(prediction, 2000, 2954083)
    
    return prediction


