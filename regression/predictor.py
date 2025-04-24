import pickle
import os
import pandas as pd
import numpy as np
from regression.core.config import settings
# Rutas a los archivos
MODEL_PATH = settings.model_path
FORM_DATA_PATH = settings.data_path

def load_model():
    """Carga el modelo desde el archivo pickle"""
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

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
    categorical_columns = ["brand", "model", "fuel_type", "accident"]
    for col in categorical_columns:
        input_data[col] = input_data[col].astype(str)
    # Realizar la predicción
    prediction = model.predict(input_data)
    
    # Asegurarse de que la predicción es un valor único
    if isinstance(prediction, (list, np.ndarray)):
        prediction = prediction[0]
    
    # Limitar a un rango razonable (como en el notebook)
    prediction = np.clip(prediction, 2000, 2954083)
    
    return prediction