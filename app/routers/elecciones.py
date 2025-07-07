from fastapi import APIRouter, HTTPException
from typing import List
import pymysql
from ..db import get_connection
from ..models import EleccionCreate, ListaCreate

router = APIRouter(prefix="/elecciones", tags=["Elecciones"])

@router.post("/")
def create_eleccion(eleccion_data: EleccionCreate):
    """Crear nueva elección"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtener el siguiente ID de elección
        cursor.execute("SELECT MAX(ID) as max_id FROM eleccion")
        result = cursor.fetchone()
        next_id = 1 if result['max_id'] is None else result['max_id'] + 1
        
        # Insertar elección
        cursor.execute(
            "INSERT INTO eleccion (ID, fecha, tipo) VALUES (%s, %s, %s)",
            (next_id, eleccion_data.fecha, eleccion_data.tipo)
        )
        
        return {"message": "Elección creada exitosamente", "id": next_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id}")
def delete_eleccion(id: int):
    """Eliminar elección por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT ID FROM eleccion WHERE ID = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Elección no encontrada")
        
        # Eliminar elección
        cursor.execute("DELETE FROM eleccion WHERE ID = %s", (id,))
        
        return {"message": "Elección eliminada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/listas")
def create_lista(lista_data: ListaCreate):
    """Crear nueva lista electoral"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si la elección existe
        cursor.execute("SELECT ID FROM eleccion WHERE ID = %s", (lista_data.IDEleccion,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Elección no encontrada")
        
        # Verificar si el partido político existe
        cursor.execute("SELECT ID FROM partidoPolitico WHERE ID = %s", (lista_data.IDPartidoPolitico,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Partido político no encontrado")
        
        # Verificar si el candidato existe
        cursor.execute("SELECT CC FROM candidato WHERE CC = %s", (lista_data.CCCandidato,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Candidato no encontrado")
        
        # Obtener el siguiente número de lista
        cursor.execute("SELECT MAX(numero) as max_numero FROM lista WHERE IDEleccion = %s", (lista_data.IDEleccion,))
        result = cursor.fetchone()
        next_numero = 1 if result['max_numero'] is None else result['max_numero'] + 1
        
        # Insertar lista
        cursor.execute(
            "INSERT INTO lista (numero, IDEleccion, departamento, IDPartidoPolitico, CCCandidato) VALUES (%s, %s, %s, %s, %s)",
            (next_numero, lista_data.IDEleccion, lista_data.departamento, lista_data.IDPartidoPolitico, lista_data.CCCandidato)
        )
        
        return {"message": "Lista creada exitosamente", "numero": next_numero}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/listas")
def get_listas(eleccion_id: int = None):
    """Obtener listas electorales"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if eleccion_id:
            query = """
            SELECT l.numero, l.IDEleccion, l.departamento, pp.direccionSede as partido, 
                   v.nombre as candidato, l.CCCandidato
            FROM lista l
            INNER JOIN partidoPolitico pp ON l.IDPartidoPolitico = pp.ID
            INNER JOIN Votante v ON l.CCCandidato = v.CC
            WHERE l.IDEleccion = %s
            ORDER BY l.numero
            """
            cursor.execute(query, (eleccion_id,))
        else:
            query = """
            SELECT l.numero, l.IDEleccion, l.departamento, pp.direccionSede as partido, 
                   v.nombre as candidato, l.CCCandidato
            FROM lista l
            INNER JOIN partidoPolitico pp ON l.IDPartidoPolitico = pp.ID
            INNER JOIN Votante v ON l.CCCandidato = v.CC
            ORDER BY l.IDEleccion, l.numero
            """
            cursor.execute(query)
        
        listas = cursor.fetchall()
        return {"listas": listas}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/listas/{numero}")
def delete_lista(numero: int, eleccion_id: int):
    """Eliminar lista electoral"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT numero FROM lista WHERE numero = %s AND IDEleccion = %s", (numero, eleccion_id))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Lista no encontrada")
        
        # Eliminar lista
        cursor.execute("DELETE FROM lista WHERE numero = %s AND IDEleccion = %s", (numero, eleccion_id))
        
        return {"message": "Lista eliminada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 