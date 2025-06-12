from models import UsuariosSQL
from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.future import select
import unicodedata
from sqlalchemy import update, delete
from fastapi import HTTPException
from models import *
from datetime import datetime, timezone, date
from typing import Dict, Any, Optional, List
from sqlmodel import Session
from sqlalchemy import func, text, case
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
import os
from dotenv import load_dotenv
import httpx

def remove_tzinfo(dt: Optional[datetime | str]) -> Optional[datetime]:
    if isinstance(dt, str):
        if dt.endswith("Z"):
            dt = dt.replace("Z", "+00:00")
        dt = datetime.fromisoformat(dt)
    if isinstance(dt, datetime) and dt.tzinfo:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def restar_valor(valor_actual, valor_a_restar):
    return max(0, valor_actual - valor_a_restar)


async def create_mascota_sql(session: AsyncSession, mascota: MascotaSQL):
    # Normalizar el nombre del nuevo equipo

    # Verificar si ya existe un equipo activo con el mismo nombre normalizado
    existing_equipo = await session.execute(
        select(MascotaSQL).where(MascotaSQL.nombre == mascota.nombre, MascotaSQL.esta_activo == True)
        # <-- Filtra por activo
    )
    if existing_equipo.first():
        raise HTTPException(status_code=400, detail=f"El equipo '{mascota.nombre}' ya existe y está activo.")

    session.add(mascota)
    await session.commit()
    await session.refresh(mascota)
    print(f"DEBUG (operations): mascota '{mascota.nombre}' creada con ID {mascota.id}.")
    return mascota


load_dotenv()
API_TOKEN = os.getenv("SPORTMONKS_API_TOKEN")


def normalizar_nombre(nombre: str) -> str:
    nombre = nombre.lower()
    nombre = unicodedata.normalize('NFKD', nombre)
    nombre = ''.join(c for c in nombre if not unicodedata.combining(c))  # Elimina tildes
    return nombre


async def create_Usuarios_sql(session: AsyncSession, Usuario: UsuariosSQL):
    Usuario.nombre = normalizar_nombre(Usuario.nombre)

    existing_usuario = await session.execute(
        select(UsuariosSQL).where(UsuariosSQL.nombre == UsuariosSQL.nombre, UsuariosSQL.esta_activo == True)

    )
    if existing_usuario.first():
        raise HTTPException(status_code=400, detail=f"El usuario '{Usuario.nombre}' ya existe y está activo.")

    session.add(Usuario)
    await session.commit()
    await session.refresh(Usuario)
    print(f"DEBUG (operations): usuario '{Usuario.nombre}' creado con ID {Usuario.id}.")
    await (session, Usuario.pais)
    return Usuario

