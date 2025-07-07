from fastapi import APIRouter, HTTPException
from typing import List
import pymysql
from ..db import get_connection
from ..models import IntegraCreate

router = APIRouter(prefix="/integra", tags=["Integra"])

@router.post("/")
def create_integra(integra_data: IntegraCreate):
    """Crear nueva relación integra"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si el integrante existe
        cursor.execute("SELECT CC FROM integranteLista WHERE CC = %s", (integra_data.CC,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Integrante de lista no encontrado")
        
        # Verificar si la lista existe
        cursor.execute("SELECT numero FROM lista WHERE numero = %s", (integra_data.numeroLista,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Lista no encontrada")
        
        # Verificar si ya existe la relación
        cursor.execute("SELECT CC FROM integra WHERE CC = %s AND numeroLista = %s", (integra_data.CC, integra_data.numeroLista))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe esta relación integra")
        
        # Insertar relación integra
        cursor.execute(
            "INSERT INTO integra (CC, numeroLista, ordenIntegrantes, organo) VALUES (%s, %s, %s, %s)",
            (integra_data.CC, integra_data.numeroLista, integra_data.ordenIntegrantes, integra_data.organo)
        )
        
        return {"message": "Relación integra creada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_integra():
    """Obtener todas las relaciones integra"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT i.CC, i.numeroLista, i.ordenIntegrantes, i.organo,
               v.nombre as integrante_nombre
        FROM integra i
        INNER JOIN Votante v ON i.CC = v.CC
        ORDER BY i.numeroLista, i.ordenIntegrantes
        """
        
        cursor.execute(query)
        integra = cursor.fetchall()
        
        return {"integra": integra}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{cc}/{numero_lista}")
def get_integra_by_cc_lista(cc: str, numero_lista: int):
    """Obtener relación integra por CC y número de lista"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT i.CC, i.numeroLista, i.ordenIntegrantes, i.organo,
               v.nombre as integrante_nombre
        FROM integra i
        INNER JOIN Votante v ON i.CC = v.CC
        WHERE i.CC = %s AND i.numeroLista = %s
        """
        
        cursor.execute(query, (cc, numero_lista))
        integra = cursor.fetchone()
        
        if not integra:
            raise HTTPException(status_code=404, detail="Relación integra no encontrada")
        
        return integra
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{cc}/{numero_lista}")
def delete_integra(cc: str, numero_lista: int):
    """Eliminar relación integra por CC y número de lista"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT CC FROM integra WHERE CC = %s AND numeroLista = %s", (cc, numero_lista))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Relación integra no encontrada")
        
        # Eliminar relación
        cursor.execute("DELETE FROM integra WHERE CC = %s AND numeroLista = %s", (cc, numero_lista))
        
        return {"message": "Relación integra eliminada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 