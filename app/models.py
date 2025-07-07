from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

# Modelos base para las tablas

class Votante(BaseModel):
    CC: str
    CI: str
    nombre: str
    direccion: str
    fechaNacimiento: date

class Establecimiento(BaseModel):
    ID: int
    nombre: str

class Circuito(BaseModel):
    ID: int
    departamento: str
    localidad: str
    direccion: str
    barrio: str
    accesible: bool
    IDEstablecimiento: int

class MiembroMesa(BaseModel):
    CC: str
    organismoEstado: str
    IDCircuito: int
    password: str
    rol: str

class AgentePolicia(BaseModel):
    CC: str
    IDEstablecimiento: int
    Comisaria: str

class IntegranteLista(BaseModel):
    CC: str

class PartidoPolitico(BaseModel):
    ID: int
    direccionSede: str
    autoridades: str

class Candidato(BaseModel):
    CC: str
    IDPartidoPolitico: int

class Eleccion(BaseModel):
    ID: int
    fecha: date
    tipo: str

class Lista(BaseModel):
    numero: int
    IDEleccion: int
    departamento: str
    IDPartidoPolitico: int
    CCCandidato: str

class Integra(BaseModel):
    CC: str
    numeroLista: int
    ordenIntegrantes: int
    organo: str

class Voto(BaseModel):
    ID: int
    fechaHora: datetime
    IDCircuito: int
    estado: str
    observado: str

class Incluye(BaseModel):
    IDVoto: int
    numeroLista: int

class ListaCredenciales(BaseModel):
    CC: str
    IDCircuito: int

class RegistroDeEmision(BaseModel):
    CC: str
    IDEleccion: int
    fechaHora: datetime
    IDCircuito: int

# Schemas para requests y responses

class VotanteCreate(BaseModel):
    CI: str
    nombre: str
    direccion: str
    fechaNacimiento: date

class VotanteResponse(BaseModel):
    CC: str
    CI: str
    nombre: str
    direccion: str
    fechaNacimiento: date

class OperadorLogin(BaseModel):
    CC: str
    password: str

class OperadorResponse(BaseModel):
    CC: str
    organismoEstado: str
    IDCircuito: int
    rol: str

class OperadorCreate(BaseModel):
    CC: str
    organismoEstado: str
    IDCircuito: int
    password: str
    rol: str

class VotoCreate(BaseModel):
    IDCircuito: int
    numeroLista: Optional[int] = None
    estado: str = "VALIDO"

class VotoResponse(BaseModel):
    ID: int
    fechaHora: datetime
    IDCircuito: int
    estado: str
    observado: str

class EleccionCreate(BaseModel):
    fecha: date
    tipo: str

class ListaCreate(BaseModel):
    IDEleccion: int
    departamento: str
    IDPartidoPolitico: int
    CCCandidato: str

class CircuitoCreate(BaseModel):
    departamento: str
    localidad: str
    direccion: str
    barrio: str
    accesible: bool
    IDEstablecimiento: int

class EstablecimientoCreate(BaseModel):
    nombre: str

class IntegranteListaCreate(BaseModel):
    CC: str

class IntegraCreate(BaseModel):
    CC: str
    numeroLista: int
    ordenIntegrantes: int
    organo: str

class IncluyeCreate(BaseModel):
    IDVoto: int
    numeroLista: int

class ListaCredencialesCreate(BaseModel):
    CC: str
    IDCircuito: int

class RegistroDeEmisionCreate(BaseModel):
    CC: str
    IDEleccion: int
    IDCircuito: int

class VotoObservadoResponse(BaseModel):
    es_observado: bool
    motivo: str

class ResultadoCircuito(BaseModel):
    lista: str
    partido: str
    cant_votos: int
    porcentaje: float

class ResultadoPartido(BaseModel):
    partido: str
    votos: int
    porcentaje: float

class ResultadoCandidato(BaseModel):
    partido: str
    candidato: str
    cant_votos: int
    porcentaje: float

class GanadorDepartamento(BaseModel):
    departamento: str
    candidato: str
    partido: str
    votos: int 