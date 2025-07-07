from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import pymysql
from ..db import get_connection
from ..models import VotanteCreate, VotanteResponse
from ..utils import generate_cc

router = APIRouter(prefix="/votantes", tags=["Votantes"])

@router.get("/{cc}", response_model=VotanteResponse)
def get_votante(cc: str):
    """Obtener votante por CC"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT CC, CI, nombre, direccion, fechaNacimiento FROM Votante WHERE CC = %s",
            (cc,)
        )
        votante = cursor.fetchone()
        
        if not votante:
            raise HTTPException(status_code=404, detail="Votante no encontrado")
        
        return VotanteResponse(**votante)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/", response_model=List[VotanteResponse])
def get_votantes(
    cc: Optional[str] = Query(None, description="Filtrar por CC"),
    circuito: Optional[int] = Query(None, description="Filtrar por ID de circuito")
):
    """Obtener votantes con filtros opcionales"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT v.CC, v.CI, v.nombre, v.direccion, v.fechaNacimiento FROM Votante v"
        params = []
        
        if cc:
            query += " WHERE v.CC = %s"
            params.append(cc)
        elif circuito:
            query += " INNER JOIN listaCredenciales lc ON v.CC = lc.CC WHERE lc.IDCircuito = %s"
            params.append(circuito)
        
        cursor.execute(query, params)
        votantes = cursor.fetchall()
        
        return [VotanteResponse(**votante) for votante in votantes]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=VotanteResponse)
def create_votante(votante_data: VotanteCreate):
    """Crear nuevo votante"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cc = generate_cc()
        
        while True:
            cursor.execute("SELECT CC FROM Votante WHERE CC = %s", (cc,))
            if not cursor.fetchone():
                break
            cc = generate_cc()
        
        cursor.execute(
            "INSERT INTO Votante (CC, CI, nombre, direccion, fechaNacimiento) VALUES (%s, %s, %s, %s, %s)",
            (cc, votante_data.CI, votante_data.nombre, votante_data.direccion, votante_data.fechaNacimiento)
        )
        
        return VotanteResponse(
            CC=cc,
            CI=votante_data.CI,
            nombre=votante_data.nombre,
            direccion=votante_data.direccion,
            fechaNacimiento=votante_data.fechaNacimiento
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{cc}")
def delete_votante(cc: str):
    """Eliminar votante por CC"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT CC FROM Votante WHERE CC = %s", (cc,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Votante no encontrado")
        
        cursor.execute("DELETE FROM Votante WHERE CC = %s", (cc,))
        
        return {"message": "Votante eliminado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 