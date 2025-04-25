# from fastapi import FastAPI, Request

# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
# from fastapi.templating import Jinja2Templates
# from regression.core.config import settings
# import regression.core.lw_log as log



# #Crear la app
# app = FastAPI(
#     title=settings.proyect_name,
#     description=settings.description,
#     version=settings.version)

# log.write_log("💹" + settings.proyect_name + " " + settings.version + " started")

# #Servir carpeta static
# app.mount("/static", StaticFiles(directory="regression/static"), name="static")
# #Configurar Jinja2 para las plantillas HTML
# templates = Jinja2Templates(directory="regression/templates")


# @app.get("/", response_class=HTMLResponse)
# def read_root( request: Request):
#     try:
#         lectura_log = log.leer_archivo() 
#         log.write_log(f"✅ Datos recuperados correctamente")
#     except Exception as e:
#         log.write_log(f"❌ Error al recuperar datos {e}")
#         print(f"❌ Error al recuperar algo {e}")
#     return templates.TemplateResponse(request,
#         "index.html",
#           {
#             "lectura": lectura_log,
#             "request": request,
#             #"brands": brands
#         }
#     )

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import pandas as pd
import joblib
from catboost import CatBoostRegressor

# Cargar el modelo
model = CatBoostRegressor()

model.load_model("models/CatBoostModel.cbm")

FEATURES = ['milage', 'model_year', 'model', 'brand',
            'engine', 'engine_L', 'fuel_type',
            'accident', 'clean_title', 'mileage',
            'horsepower']

CAT_FEATURES = ['brand', 'model', 'fuel_type', 'engine',
                'accident', 'model_year', 'clean_title']

# Crear app
app = FastAPI(title="Car Price Prediction API")

# Pydantic input con validaciones
class CarFeatures(BaseModel):
    milage: float = Field(..., gt=0)
    model_year: int = Field(..., ge=1980, le=2025)
    model: str
    brand: str
    engine: str
    engine_L: float = Field(..., gt=0)
    fuel_type: str
    accident: str
    clean_title: str
    mileage: float = Field(..., gt=0)
    horsepower: float = Field(..., gt=0)

    @validator('accident', 'clean_title')
    def check_binary_string(cls, v):
        if v.lower() not in ['yes', 'no']:
            raise ValueError("Debe ser 'Yes' o 'No'")
        return v.title()

@app.get("/")
def root():
    return {"message": "Car Price Prediction API. Use POST /predict to get a price estimate."}

@app.post("/predict")
def predict_price(car: CarFeatures):
    try:
        df = pd.DataFrame([car.dict()])[FEATURES]
        prediction = model.predict(df)
        return {"predicted_price": round(float(prediction[0]), 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))