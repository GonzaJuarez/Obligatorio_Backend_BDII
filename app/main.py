from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import operadores, votantes, votos, elecciones, circuitos, establecimientos
from .routers import integrantes_listas, integra, incluye, lista_credenciales, registro_emision, estadisticas
from .db import get_connection

app = FastAPI(
    title="API Sistema de Votación Electrónico",
    description="API para gestión de elecciones, votantes, votos y operadores/admins.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(operadores.router)
app.include_router(votantes.router)
app.include_router(votos.router)
app.include_router(elecciones.router)
app.include_router(circuitos.router)
app.include_router(establecimientos.router)
app.include_router(integrantes_listas.router)
app.include_router(integra.router)
app.include_router(incluye.router)
app.include_router(lista_credenciales.router)
app.include_router(registro_emision.router)
app.include_router(estadisticas.router)

@app.get("/")
def read_root():
    return {"message": "Obligatorio BD II - 2025"}

@app.get("/test-db")
def test_database_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "message": "Conexión a la base de datos exitosa",
            "test_result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": "Error al conectar con la base de datos",
            "error": str(e)
        }





