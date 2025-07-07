from fastapi import APIRouter, HTTPException
from typing import List
from ..db import get_connection
from ..models import EstablecimientoCreate

router = APIRouter(prefix="/establecimientos", tags=["Establecimientos"])

@router.post("/")
def create_establecimiento(establecimiento_data: EstablecimientoCreate):
    """Crear nuevo establecimiento"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtener el siguiente ID de establecimiento
        cursor.execute("SELECT MAX(ID) as max_id FROM Establecimiento")
        result = cursor.fetchone()
        next_id = 1 if result['max_id'] is None else result['max_id'] + 1
        
        # Insertar establecimiento
        cursor.execute(
            "INSERT INTO Establecimiento (ID, nombre) VALUES (%s, %s)",
            (next_id, establecimiento_data.nombre)
        )
        
        return {"message": "Establecimiento creado exitosamente", "id": next_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_establecimientos():
    """Obtener todos los establecimientos"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID, nombre FROM Establecimiento ORDER BY ID")
        establecimientos = cursor.fetchall()
        
        return {"establecimientos": establecimientos}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{id}")
def get_establecimiento(id: int):
    """Obtener establecimiento por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID, nombre FROM Establecimiento WHERE ID = %s", (id,))
        establecimiento = cursor.fetchone()
        
        if not establecimiento:
            raise HTTPException(status_code=404, detail="Establecimiento no encontrado")
        
        return establecimiento
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id}")
def delete_establecimiento(id: int):
    """Eliminar establecimiento por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT ID FROM Establecimiento WHERE ID = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Establecimiento no encontrado")
        
        # Verificar si hay circuitos asociados
        cursor.execute("SELECT ID FROM circuito WHERE IDEstablecimiento = %s", (id,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="No se puede eliminar el establecimiento porque tiene circuitos asociados")
        
        # Eliminar establecimiento
        cursor.execute("DELETE FROM Establecimiento WHERE ID = %s", (id,))
        
        return {"message": "Establecimiento eliminado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 