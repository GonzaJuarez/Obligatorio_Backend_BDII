from fastapi import APIRouter, HTTPException
from typing import List
import pymysql
from ..db import get_connection
from ..models import IntegranteListaCreate

router = APIRouter(prefix="/integrantes-listas", tags=["Integrantes de Listas"])

@router.post("/")
def create_integrante_lista(integrante_data: IntegranteListaCreate):
    """Crear nuevo integrante de lista"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si el votante existe
        cursor.execute("SELECT CC FROM Votante WHERE CC = %s", (integrante_data.CC,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Votante no encontrado")
        
        # Verificar si ya existe como integrante
        cursor.execute("SELECT CC FROM integranteLista WHERE CC = %s", (integrante_data.CC,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe un integrante con ese CC")
        
        # Insertar integrante
        cursor.execute("INSERT INTO integranteLista (CC) VALUES (%s)", (integrante_data.CC,))
        
        return {"message": "Integrante de lista creado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_integrantes_listas():
    """Obtener todos los integrantes de listas"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT il.CC, v.nombre, v.CI
        FROM integranteLista il
        INNER JOIN Votante v ON il.CC = v.CC
        ORDER BY v.nombre
        """
        
        cursor.execute(query)
        integrantes = cursor.fetchall()
        
        return {"integrantes": integrantes}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{cc}")
def get_integrante_lista(cc: str):
    """Obtener integrante de lista por CC"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT il.CC, v.nombre, v.CI
        FROM integranteLista il
        INNER JOIN Votante v ON il.CC = v.CC
        WHERE il.CC = %s
        """
        
        cursor.execute(query, (cc,))
        integrante = cursor.fetchone()
        
        if not integrante:
            raise HTTPException(status_code=404, detail="Integrante de lista no encontrado")
        
        return integrante
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{cc}")
def delete_integrante_lista(cc: str):
    """Eliminar integrante de lista por CC"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT CC FROM integranteLista WHERE CC = %s", (cc,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Integrante de lista no encontrado")
        
        # Eliminar integrante
        cursor.execute("DELETE FROM integranteLista WHERE CC = %s", (cc,))
        
        return {"message": "Integrante de lista eliminado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 