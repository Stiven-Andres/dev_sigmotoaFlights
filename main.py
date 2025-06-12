from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from shutil import copyfileobj
from sqlalchemy.orm import selectinload
from operations import *
from models import *
from sqlmodel.ext.asyncio.session import AsyncSession

from models import *
import uuid
import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from utils.connection_db import *
from contextlib import asynccontextmanager
from operations import *


# Configuración de plantilla Jinja2
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


templates = Jinja2Templates(directory="templates")
app = FastAPI(lifespan=lifespan)
UPLOAD_DIR = "static/logos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Archivos estáticos (CSS, imágenes, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/inicio", response_class=HTMLResponse)
async def mostrar_inicio(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})

@app.get("/formulario_mascota", response_class=HTMLResponse)
async def mostrar_formulario_mascota(request: Request):
    return templates.TemplateResponse("formulario_mascota.html", {"request": request})

@app.get("/mascota-agregada", name="mostrar_mascota_agregada", response_class=HTMLResponse)
async def mostrar_mascota_agregada(request: Request, nombre: str, raza: str, sexo: str, logo_url: str):
    return templates.TemplateResponse("mascota_agregada.html", {
        "request": request,
        "nombre": nombre,
        "raza": raza,
        "sexo": sexo,
        "logo_url": logo_url,
    })


# ----------- mascotas --------------
@app.post("/equipos/", response_class=HTMLResponse)
async def crear_mascota(
    request: Request,
    nombre: str = Form(...),
    raza: str = Form(...),
    sexo: str = Form(...),
    tipo: str = Form(...),
    logo: UploadFile = File(...),
    esta_activo: bool = Form(True),
    session: AsyncSession = Depends(get_session)
):
    # Verificar tipo de archivo
    if logo.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no válido (solo .png o .jpg)")

    # Crear nombre único para el archivo
    extension = os.path.splitext(logo.filename)[1]
    nombre_archivo = f"{uuid.uuid4().hex}{extension}"
    ruta_archivo = os.path.join("static", "img", nombre_archivo)

    # Guardar imagen
    os.makedirs("static/img", exist_ok=True)
    with open(ruta_archivo, "wb") as buffer:
        copyfileobj(logo.file, buffer)

    # Crear instancia del modelo
    mascota_db = MascotaSQL(
        nombre=nombre,
        raza=raza,
        sexo=sexo,
        tipo=Mascota,
        logo_url=f"img/{nombre_archivo}",
        esta_activo = esta_activo
    )

    # Guardar en base de datos
    await create_mascota_sql(session, mascota_db)

    # Redireccionar al HTML con modal
    url = str(request.url_for("mostrar_mascota_agregada")) + \
          f"?nombre={nombre}&raza={raza}&tipo={Mascota}&logo_url={mascota_db.logo_url}"

    return RedirectResponse(url=url, status_code=303)


@app.get("/mascotas/", response_model=List[MascotaSQL])
async def listar_mascotas(session: AsyncSession = Depends(get_session)):
    return await obtener_todas_las_mascotas(session)

