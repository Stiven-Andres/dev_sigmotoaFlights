from sqlmodel import SQLModel, Field
from typing import Optional
from sqlmodel import Relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

from pydantic import ConfigDict


class Mascota(str, Enum):
    gato="Gato"
    perro="Perro"
    loro="Loro"
    hamster="Hamster"



class MascotaCreate(BaseModel):
    id: Optional[int] = None
    nombre: str
    edad: int
    email: str
    mascota: Mascota



# --------- Modelo Equipo ---------
class UsuariosSQL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=3, max_length=50)
    edad: int= Field(default=0)
    email: str = Field(min_length=15, max_length=50)
    Mascotas: int = Field(default=0)

class MascotaSQL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=3, max_length=50)
    raza: str = Field(min_length=3, max_length=50)
    sexo: str = Field(min_length=1, max_length=1)
    tipo: Mascota = Field(default=Mascota.perro)
    logo_url: Optional[str] = Field(default="img/shield.png")
    esta_activo: bool = Field(default=True)


class VueloSQL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    origen: str = Field(min_length=3, max_length=50)
    destino: str = Field(min_length=3, max_length=50)
    fecha_partida: datetime = Field(default_factory=datetime.utcnow)
    reservado: bool = Field(default=True)
    disponibilidad: bool = Field(default=True)
    precio: float = Field(default=0.0)
    mascotas: int = Field(default=0)


