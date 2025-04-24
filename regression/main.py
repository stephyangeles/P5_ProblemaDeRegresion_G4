from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from regression.core.config import settings
import regression.core.lw_log as log
from catboost import CatBoostClassifier, CatBoostRegressor
import pandas as pd
import pickle



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

with open(settings.model_path, "rb") as f:
    model_cat = pickle.load(f)



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