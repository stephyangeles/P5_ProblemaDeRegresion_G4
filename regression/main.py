from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates


#Crear la app
app = FastAPI(title="API Precio de Coches")
#Servir carpeta static
#app.mount("/static", StaticFiles(directory="static"), name="static")
#Configurar Jinja2 para las plantillas HTML
templates = Jinja2Templates(directory="regression/templates")


@app.get("/", response_class=HTMLResponse)
def read_root( request: Request):
    return templates.TemplateResponse(request,
        "index.html",
          {
            "request": request,
            #"brands": brands
        }
    )