from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from regression.core.config import settings
import regression.core.lw_log as log
import regression.core.pkl_log as pkl_log

import pandas as pd
from typing import Optional, List

import json
from pydantic import BaseModel
from regression.predictor import predict_price, load_form_data


form_data = load_form_data()

#Crear la app
app = FastAPI(
    title=settings.proyect_name,
    description=settings.description,
    version=settings.version
    )

log.write_log("💹" + settings.proyect_name + " " + settings.version + " started")
pkl_log.write_log_pkl("💹" + settings.proyect_name + " " + settings.version + " started")

#Servir carpeta static
app.mount("/static", StaticFiles(directory="regression/static"), name="static")
#Configurar Jinja2 para las plantillas HTML
templates = Jinja2Templates(directory="regression/templates")
# Cargar modelo, scaler y columnas
# Modelo para la solicitud de predicción
class CarInput(BaseModel):
    brand: str
    model: str
    model_year: int
    milage: int
    fuel_type: str
    engine_L: Optional[float] = None
    horsepower: Optional[float] = None
    accident: str
    clean_title: int


# Ruta principal - Renderiza el formulario HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    lectura = log.leer_archivo()
    count_brands = len(form_data["categories"]["brand"])
    count_models = len(form_data["categories"]["models_by_brand"])
    return templates.TemplateResponse(request,
        "index.html", 
        {
            "request": request, 
            "lectura": lectura,
            "count_models": count_models,
            "count_brands": count_brands,
            "title": settings.proyect_name + ", " + settings.version,
            "description": settings.description,
            "form_data": json.dumps(form_data)
        }
    )

# Endpoint para obtener los modelos de una marca específica
@app.get(settings.api_prefix+"/models/{brand}")
async def get_models_by_brand(brand: str):
    if brand in form_data["categories"]["models_by_brand"]:
        return {"models": form_data["categories"]["models_by_brand"][brand]}
    return {"models": []}

# Endpoint para la predicción
@app.post(settings.api_prefix+"/predict")
async def predict(data: CarInput):
    try:

        input_data = pd.DataFrame({
            'milage': [data.milage],
            'model_year': [data.model_year],
            'model': [data.model],
            'brand': [data.brand],
            'engine': ['no_entry'],  # Valor por defecto, ya que usamos horsepower y engine_L
            'engine_L': [data.engine_L if data.engine_L is not None else -1],
            'fuel_type': [data.fuel_type],
            'accident': [data.accident],
            'clean_title': [data.clean_title],
            'mileage': [data.milage // 100],  # Calculado igual que en el preprocesamiento
            'horsepower': [data.horsepower if data.horsepower is not None else -1]
        })
        # Obtener la predicción
        price = predict_price(input_data)
        
        # Devolver el resultado
        return {
            "predicted_price": float(price),
            "formatted_price": f"${price:,.2f}"
        }
    except Exception as e:
        return {"error": str(e)}