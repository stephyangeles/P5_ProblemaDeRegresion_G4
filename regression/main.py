from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from regression.core.config import settings
import regression.core.lw_log as log
from catboost import CatBoostClassifier, CatBoostRegressor
import pandas as pd
from regression.predictor import predict_price, load_form_data


form_data = load_form_data()

#Crear la app
app = FastAPI(
    title=settings.proyect_name,
    description=settings.description,
    version=settings.version)

log.write_log("💹" + settings.proyect_name + " " + settings.version + " started")

#Servir carpeta static
app.mount("/static", StaticFiles(directory="regression/static"), name="static")
#Configurar Jinja2 para las plantillas HTML
templates = Jinja2Templates(directory="regression/templates")
# Cargar modelo, scaler y columnas



@app.get("/", response_class=HTMLResponse)
def read_root( request: Request):
    try:
        lectura_log = log.leer_archivo() 
        log.write_log(f"✅ Datos recuperados correctamente")
    except Exception as e:
        log.write_log(f"❌ Error al recuperar datos {e}")
        print(f"❌ Error al recuperar algo {e}")
    return templates.TemplateResponse(request,
        "index.html",
          {
            "lectura": lectura_log,
            "request": request
        }
    )

@app.post("/predict")
async def predict(data):
    try:
        # Crear un DataFrame con los datos de entrada
        input_data = pd.DataFrame({
            'brand': [data.brand],
            'model': [data.model],
            'model_year': [data.model_year],
            'milage': [data.milage],
            'mileage': [data.milage // 100],  # Calculado igual que en el preprocesamiento
            'fuel_type': [data.fuel_type],
            'engine_L': [data.engine_L if data.engine_L is not None else -1],
            'horsepower': [data.horsepower if data.horsepower is not None else -1],
            'accident': [data.accident],
            'clean_title': [data.clean_title],
            'engine': ['no_entry']  # Valor por defecto, ya que usamos horsepower y engine_L
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

@app.get("/models/{brand}")
async def get_models_by_brand(brand: str):
    if brand in form_data["categories"]["models_by_brand"]:
        return {"models": form_data["categories"]["models_by_brand"][brand]}
    return {"models": []}