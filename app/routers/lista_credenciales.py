from fastapi import APIRouter, HTTPException
from typing import List
from ..db import get_connection
from ..models import ListaCredencialesCreate

router = APIRouter(prefix="/lista-credenciales", tags=["Lista de Credenciales"])

@router.post("/")
def create_lista_credenciales(credencial_data: ListaCredencialesCreate):
    """Crear nueva entrada en lista de credenciales"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si el votante existe
        cursor.execute("SELECT CC FROM Votante WHERE CC = %s", (credencial_data.CC,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Votante no encontrado")
        
        # Verificar si el circuito existe
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (credencial_data.IDCircuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Circuito no encontrado")
        
        # Verificar si ya existe la relación
        cursor.execute("SELECT CC FROM listaCredenciales WHERE CC = %s AND IDCircuito = %s", (credencial_data.CC, credencial_data.IDCircuito))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe esta credencial para el votante en este circuito")
        
        # Insertar credencial
        cursor.execute(
            "INSERT INTO listaCredenciales (CC, IDCircuito) VALUES (%s, %s)",
            (credencial_data.CC, credencial_data.IDCircuito)
        )
        
        return {"message": "Credencial agregada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_lista_credenciales():
    """Obtener toda la lista de credenciales"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT lc.CC, lc.IDCircuito, v.nombre, v.CI, c.departamento, c.localidad
        FROM listaCredenciales lc
        INNER JOIN Votante v ON lc.CC = v.CC
        INNER JOIN circuito c ON lc.IDCircuito = c.ID
        ORDER BY c.ID, v.nombre
        """
        
        cursor.execute(query)
        credenciales = cursor.fetchall()
        
        return {"credenciales": credenciales}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{cc}/{id_circuito}")
def get_credencial(cc: str, id_circuito: int):
    """Obtener credencial específica por CC y ID de circuito"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT lc.CC, lc.IDCircuito, v.nombre, v.CI, c.departamento, c.localidad
        FROM listaCredenciales lc
        INNER JOIN Votante v ON lc.CC = v.CC
        INNER JOIN circuito c ON lc.IDCircuito = c.ID
        WHERE lc.CC = %s AND lc.IDCircuito = %s
        """
        
        cursor.execute(query, (cc, id_circuito))
        credencial = cursor.fetchone()
        
        if not credencial:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        
        return credencial
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{cc}/{id_circuito}")
def delete_credencial(cc: str, id_circuito: int):
    """Eliminar credencial por CC y ID de circuito"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT CC FROM listaCredenciales WHERE CC = %s AND IDCircuito = %s", (cc, id_circuito))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        
        # Eliminar credencial
        cursor.execute("DELETE FROM listaCredenciales WHERE CC = %s AND IDCircuito = %s", (cc, id_circuito))
        
        return {"message": "Credencial eliminada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 