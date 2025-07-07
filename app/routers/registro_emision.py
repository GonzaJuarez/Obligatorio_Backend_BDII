from fastapi import APIRouter, HTTPException
from typing import List
import pymysql
from datetime import datetime
from ..db import get_connection
from ..models import RegistroDeEmisionCreate

router = APIRouter(prefix="/registro-emision", tags=["Registro de Emisión"])

@router.post("/")
def create_registro_emision(registro_data: RegistroDeEmisionCreate):
    """Crear nuevo registro de emisión"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si el votante existe
        cursor.execute("SELECT CC FROM Votante WHERE CC = %s", (registro_data.CC,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Votante no encontrado")
        
        # Verificar si la elección existe
        cursor.execute("SELECT ID FROM eleccion WHERE ID = %s", (registro_data.IDEleccion,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Elección no encontrada")
        
        # Verificar si el circuito existe
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (registro_data.IDCircuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Circuito no encontrado")
        
        # Verificar si ya existe el registro
        cursor.execute("SELECT CC FROM registroDeEmision WHERE CC = %s AND IDEleccion = %s", (registro_data.CC, registro_data.IDEleccion))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe un registro de emisión para este votante en esta elección")
        
        # Insertar registro
        fecha_hora = datetime.now()
        cursor.execute(
            "INSERT INTO registroDeEmision (CC, IDEleccion, fechaHora, IDCircuito) VALUES (%s, %s, %s, %s)",
            (registro_data.CC, registro_data.IDEleccion, fecha_hora, registro_data.IDCircuito)
        )
        
        return {"message": "Registro de emisión creado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_registros_emision():
    """Obtener todos los registros de emisión"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT re.CC, re.IDEleccion, re.fechaHora, re.IDCircuito,
               v.nombre as votante_nombre, e.tipo as eleccion_tipo,
               c.departamento, c.localidad
        FROM registroDeEmision re
        INNER JOIN Votante v ON re.CC = v.CC
        INNER JOIN eleccion e ON re.IDEleccion = e.ID
        INNER JOIN circuito c ON re.IDCircuito = c.ID
        ORDER BY re.fechaHora DESC
        """
        
        cursor.execute(query)
        registros = cursor.fetchall()
        
        return {"registros": registros}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{cc}/{id_eleccion}")
def get_registro_emision(cc: str, id_eleccion: int):
    """Obtener registro de emisión específico por CC y ID de elección"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT re.CC, re.IDEleccion, re.fechaHora, re.IDCircuito,
               v.nombre as votante_nombre, e.tipo as eleccion_tipo,
               c.departamento, c.localidad
        FROM registroDeEmision re
        INNER JOIN Votante v ON re.CC = v.CC
        INNER JOIN eleccion e ON re.IDEleccion = e.ID
        INNER JOIN circuito c ON re.IDCircuito = c.ID
        WHERE re.CC = %s AND re.IDEleccion = %s
        """
        
        cursor.execute(query, (cc, id_eleccion))
        registro = cursor.fetchone()
        
        if not registro:
            raise HTTPException(status_code=404, detail="Registro de emisión no encontrado")
        
        return registro
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{cc}/{id_eleccion}")
def delete_registro_emision(cc: str, id_eleccion: int):
    """Eliminar registro de emisión por CC y ID de elección"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT CC FROM registroDeEmision WHERE CC = %s AND IDEleccion = %s", (cc, id_eleccion))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Registro de emisión no encontrado")
        
        # Eliminar registro
        cursor.execute("DELETE FROM registroDeEmision WHERE CC = %s AND IDEleccion = %s", (cc, id_eleccion))
        
        return {"message": "Registro de emisión eliminado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 