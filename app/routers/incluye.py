from fastapi import APIRouter, HTTPException
from typing import List
from ..db import get_connection
from ..models import IncluyeCreate

router = APIRouter(prefix="/incluye", tags=["Incluye"])

@router.post("/")
def create_incluye(incluye_data: IncluyeCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID FROM voto WHERE ID = %s", (incluye_data.IDVoto,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Voto no encontrado")
        
        cursor.execute("SELECT numero FROM lista WHERE numero = %s", (incluye_data.numeroLista,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Lista no encontrada")
        
        cursor.execute("SELECT IDVoto FROM incluye WHERE IDVoto = %s AND numeroLista = %s", (incluye_data.IDVoto, incluye_data.numeroLista))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe esta relación incluye")
        
        cursor.execute(
            "INSERT INTO incluye (IDVoto, numeroLista) VALUES (%s, %s)",
            (incluye_data.IDVoto, incluye_data.numeroLista)
        )
        
        return {"message": "Relación incluye creada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_incluye():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT i.IDVoto, i.numeroLista, v.fechaHora, v.IDCircuito, v.estado
        FROM incluye i
        INNER JOIN voto v ON i.IDVoto = v.ID
        ORDER BY v.fechaHora DESC
        """
        
        cursor.execute(query)
        incluye = cursor.fetchall()
        
        return {"incluye": incluye}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{id_voto}/{numero_lista}")
def get_incluye_by_voto_lista(id_voto: int, numero_lista: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT i.IDVoto, i.numeroLista, v.fechaHora, v.IDCircuito, v.estado
        FROM incluye i
        INNER JOIN voto v ON i.IDVoto = v.ID
        WHERE i.IDVoto = %s AND i.numeroLista = %s
        """
        
        cursor.execute(query, (id_voto, numero_lista))
        incluye = cursor.fetchone()
        
        if not incluye:
            raise HTTPException(status_code=404, detail="Relación incluye no encontrada")
        
        return incluye
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id_voto}/{numero_lista}")
def delete_incluye(id_voto: int, numero_lista: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT IDVoto FROM incluye WHERE IDVoto = %s AND numeroLista = %s", (id_voto, numero_lista))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Relación incluye no encontrada")
        
        cursor.execute("DELETE FROM incluye WHERE IDVoto = %s AND numeroLista = %s", (id_voto, numero_lista))
        
        return {"message": "Relación incluye eliminada exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 