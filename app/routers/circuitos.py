from fastapi import APIRouter, HTTPException
from typing import List
from ..db import get_connection
from ..models import CircuitoCreate

router = APIRouter(prefix="/circuitos", tags=["Circuitos"])

@router.post("/")
def create_circuito(circuito_data: CircuitoCreate):
    """Crear nuevo circuito"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si el establecimiento existe
        cursor.execute("SELECT ID FROM Establecimiento WHERE ID = %s", (circuito_data.IDEstablecimiento,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Establecimiento no encontrado")
        
        # Obtener el siguiente ID de circuito
        cursor.execute("SELECT MAX(ID) as max_id FROM circuito")
        result = cursor.fetchone()
        next_id = 1 if result['max_id'] is None else result['max_id'] + 1
        
        # Insertar circuito
        cursor.execute(
            "INSERT INTO circuito (ID, departamento, localidad, direccion, barrio, accesible, IDEstablecimiento) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (next_id, circuito_data.departamento, circuito_data.localidad, circuito_data.direccion, 
             circuito_data.barrio, circuito_data.accesible, circuito_data.IDEstablecimiento)
        )
        
        return {"message": "Circuito creado exitosamente", "id": next_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_circuitos():
    """Obtener todos los circuitos"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT c.ID, c.departamento, c.localidad, c.direccion, c.barrio, c.accesible, 
               e.nombre as establecimiento
        FROM circuito c
        INNER JOIN Establecimiento e ON c.IDEstablecimiento = e.ID
        ORDER BY c.ID
        """
        
        cursor.execute(query)
        circuitos = cursor.fetchall()
        
        return {"circuitos": circuitos}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{id}")
def get_circuito(id: int):
    """Obtener circuito por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT c.ID, c.departamento, c.localidad, c.direccion, c.barrio, c.accesible, 
               e.nombre as establecimiento
        FROM circuito c
        INNER JOIN Establecimiento e ON c.IDEstablecimiento = e.ID
        WHERE c.ID = %s
        """
        
        cursor.execute(query, (id,))
        circuito = cursor.fetchone()
        
        if not circuito:
            raise HTTPException(status_code=404, detail="Circuito no encontrado")
        
        return circuito
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id}")
def delete_circuito(id: int):
    """Eliminar circuito por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Circuito no encontrado")
        
        # Eliminar circuito
        cursor.execute("DELETE FROM circuito WHERE ID = %s", (id,))
        
        return {"message": "Circuito eliminado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 