from catboost import CatBoostRegressor
import pytest
import pandas as pd
from regression.core.config import settings

def test_model_accuracy():

    model = CatBoostRegressor()
    model.load_model(settings.model_path)

    input_data_test = pd.DataFrame([{
        'milage': 17000,
        'model_year': 2013,
        'model': '300 S',
        'brand': 'BMW',
        'engine': 'no_entry', 
        'engine_L': -1,
        'fuel_type': 'Gasoline',
        'accident': 'None reported',
        'clean_title': 1,
        'mileage': 17000 // 100,  
        'horsepower': -1
    }])

    for col in ['brand', 'model', 'fuel_type', 'accident']:
        input_data_test[col] = input_data_test[col].astype(str)

    # predicción
    try:
        predictions = model.predict(input_data_test)
    except Exception as e:
        pytest.fail(f"Model prediction failed: {e}")

    # Verificar el modelo no devuelve errores
    assert predictions is not None  
    # Asegurar la predicción tiene el tamaño correcto
    assert len(predictions) == len(input_data_test)  
    # Verificar la predicción sea un número
    assert isinstance(predictions[0], (int, float))  
    # Ajustar estos límites según tus expectativas
    assert 0 < predictions[0] < 150000  
