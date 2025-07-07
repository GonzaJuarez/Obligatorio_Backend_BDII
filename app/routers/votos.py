from fastapi import APIRouter, HTTPException
from typing import List
import pymysql
from datetime import datetime
from ..db import get_connection
from ..models import VotoCreate, VotoResponse, VotoObservadoResponse

router = APIRouter(prefix="/votos", tags=["Votos"])

@router.post("/", response_model=VotoResponse)
def create_voto(voto_data: VotoCreate):
    """Crear nuevo voto"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtener el siguiente ID de voto
        cursor.execute("SELECT MAX(ID) as max_id FROM voto")
        result = cursor.fetchone()
        next_id = 1 if result['max_id'] is None else result['max_id'] + 1
        
        # Verificar si el circuito existe
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (voto_data.IDCircuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Circuito no encontrado")
        
        # Verificar si la lista existe (si se proporciona)
        if voto_data.numeroLista:
            cursor.execute("SELECT numero FROM lista WHERE numero = %s", (voto_data.numeroLista,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Lista no encontrada")
        
        # Insertar voto
        fecha_hora = datetime.now()
        cursor.execute(
            "INSERT INTO voto (ID, fechaHora, IDCircuito, estado, observado) VALUES (%s, %s, %s, %s, %s)",
            (next_id, fecha_hora, voto_data.IDCircuito, voto_data.estado, "FALSE")
        )
        
        # Si se proporciona una lista, crear la relación incluye
        if voto_data.numeroLista:
            cursor.execute(
                "INSERT INTO incluye (IDVoto, numeroLista) VALUES (%s, %s)",
                (next_id, voto_data.numeroLista)
            )
        
        return VotoResponse(
            ID=next_id,
            fechaHora=fecha_hora,
            IDCircuito=voto_data.IDCircuito,
            estado=voto_data.estado,
            observado="FALSE"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/resultados")
def get_resultados():
    """Obtener resultados de votación"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Consulta para obtener resultados por lista
        query = """
        SELECT 
            l.numero as lista,
            pp.direccionSede as partido,
            COUNT(i.IDVoto) as cant_votos,
            ROUND((COUNT(i.IDVoto) * 100.0 / (SELECT COUNT(*) FROM voto WHERE estado = 'VALIDO')), 2) as porcentaje
        FROM lista l
        LEFT JOIN partidoPolitico pp ON l.IDPartidoPolitico = pp.ID
        LEFT JOIN incluye i ON l.numero = i.numeroLista
        LEFT JOIN voto v ON i.IDVoto = v.ID AND v.estado = 'VALIDO'
        GROUP BY l.numero, pp.direccionSede
        ORDER BY l.numero
        """
        
        cursor.execute(query)
        resultados_lista = cursor.fetchall()
        
        # Consulta para votos en blanco y anulados
        query_especiales = """
        SELECT 
            estado,
            COUNT(*) as cant_votos,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM voto)), 2) as porcentaje
        FROM voto 
        WHERE estado IN ('EN_BLANCO', 'ANULADO')
        GROUP BY estado
        """
        
        cursor.execute(query_especiales)
        votos_especiales = cursor.fetchall()
        
        return {
            "resultados_por_lista": resultados_lista,
            "votos_especiales": votos_especiales
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/verificar-observado", response_model=VotoObservadoResponse)
def verificar_voto_observado(cc: str, id_circuito: int):
    """Verificar si un voto es observado (votante no está en el circuito correcto)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si el votante está en la lista de credenciales del circuito
        cursor.execute(
            "SELECT CC FROM listaCredenciales WHERE CC = %s AND IDCircuito = %s",
            (cc, id_circuito)
        )
        
        es_observado = not cursor.fetchone()
        motivo = "Votante no está habilitado para votar en este circuito" if es_observado else "Voto válido"
        
        return VotoObservadoResponse(
            es_observado=es_observado,
            motivo=motivo
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 