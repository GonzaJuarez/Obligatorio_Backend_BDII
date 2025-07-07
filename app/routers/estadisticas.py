from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import pymysql
from ..db import get_connection

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas y Reportes"])

@router.get("/resultados-circuito/{id_circuito}")
def get_resultados_circuito(id_circuito: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (id_circuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Circuito no encontrado")
        
        query_listas = """
        SELECT 
            CONCAT('Lista ', l.numero) as lista,
            pp.direccionSede as partido,
            COUNT(i.IDVoto) as cant_votos,
            ROUND((COUNT(i.IDVoto) * 100.0 / (SELECT COUNT(*) FROM voto WHERE IDCircuito = %s AND estado = 'VALIDO')), 2) as porcentaje
        FROM lista l
        LEFT JOIN partidoPolitico pp ON l.IDPartidoPolitico = pp.ID
        LEFT JOIN incluye i ON l.numero = i.numeroLista
        LEFT JOIN voto v ON i.IDVoto = v.ID AND v.IDCircuito = %s AND v.estado = 'VALIDO'
        GROUP BY l.numero, pp.direccionSede
        ORDER BY l.numero
        """
        
        cursor.execute(query_listas, (id_circuito, id_circuito))
        resultados_listas = cursor.fetchall()
        
        query_especiales = """
        SELECT 
            CASE 
                WHEN estado = 'EN_BLANCO' THEN 'En Blanco'
                WHEN estado = 'ANULADO' THEN 'Anulado'
                ELSE estado
            END as lista,
            CASE 
                WHEN estado = 'EN_BLANCO' THEN 'En Blanco'
                WHEN estado = 'ANULADO' THEN 'Anulado'
                ELSE estado
            END as partido,
            COUNT(*) as cant_votos,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM voto WHERE IDCircuito = %s)), 2) as porcentaje
        FROM voto 
        WHERE IDCircuito = %s AND estado IN ('EN_BLANCO', 'ANULADO')
        GROUP BY estado
        """
        
        cursor.execute(query_especiales, (id_circuito, id_circuito))
        votos_especiales = cursor.fetchall()
        
        return {
            "circuito_id": id_circuito,
            "resultados": resultados_listas + votos_especiales
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/resultados-partido-circuito/{id_circuito}")
def get_resultados_partido_circuito(id_circuito: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (id_circuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Circuito no encontrado")
        
        query_partidos = """
        SELECT 
            pp.direccionSede as partido,
            COUNT(i.IDVoto) as votos,
            ROUND((COUNT(i.IDVoto) * 100.0 / (SELECT COUNT(*) FROM voto WHERE IDCircuito = %s AND estado = 'VALIDO')), 2) as porcentaje
        FROM partidoPolitico pp
        LEFT JOIN lista l ON pp.ID = l.IDPartidoPolitico
        LEFT JOIN incluye i ON l.numero = i.numeroLista
        LEFT JOIN voto v ON i.IDVoto = v.ID AND v.IDCircuito = %s AND v.estado = 'VALIDO'
        GROUP BY pp.ID, pp.direccionSede
        HAVING COUNT(i.IDVoto) > 0
        ORDER BY votos DESC
        """
        
        cursor.execute(query_partidos, (id_circuito, id_circuito))
        resultados_partidos = cursor.fetchall()
        
        query_especiales = """
        SELECT 
            CASE 
                WHEN estado = 'EN_BLANCO' THEN 'En Blanco'
                WHEN estado = 'ANULADO' THEN 'Anulado'
                ELSE estado
            END as partido,
            COUNT(*) as votos,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM voto WHERE IDCircuito = %s)), 2) as porcentaje
        FROM voto 
        WHERE IDCircuito = %s AND estado IN ('EN_BLANCO', 'ANULADO')
        GROUP BY estado
        """
        
        cursor.execute(query_especiales, (id_circuito, id_circuito))
        votos_especiales = cursor.fetchall()
        
        return {
            "circuito_id": id_circuito,
            "resultados": resultados_partidos + votos_especiales
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/resultados-candidato-circuito/{id_circuito}")
def get_resultados_candidato_circuito(id_circuito: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (id_circuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Circuito no encontrado")
        
        query_candidatos = """
        SELECT 
            pp.direccionSede as partido,
            v.nombre as candidato,
            COUNT(i.IDVoto) as cant_votos,
            ROUND((COUNT(i.IDVoto) * 100.0 / (SELECT COUNT(*) FROM voto WHERE IDCircuito = %s AND estado = 'VALIDO')), 2) as porcentaje
        FROM candidato c
        INNER JOIN Votante v ON c.CC = v.CC
        INNER JOIN partidoPolitico pp ON c.IDPartidoPolitico = pp.ID
        INNER JOIN lista l ON c.CC = l.CCCandidato
        LEFT JOIN incluye i ON l.numero = i.numeroLista
        LEFT JOIN voto vt ON i.IDVoto = vt.ID AND vt.IDCircuito = %s AND vt.estado = 'VALIDO'
        GROUP BY c.CC, v.nombre, pp.direccionSede
        ORDER BY cant_votos DESC
        """
        
        cursor.execute(query_candidatos, (id_circuito, id_circuito))
        resultados_candidatos = cursor.fetchall()
        
        query_especiales = """
        SELECT 
            CASE 
                WHEN estado = 'EN_BLANCO' THEN 'En Blanco'
                WHEN estado = 'ANULADO' THEN 'Anulado'
                ELSE estado
            END as partido,
            CASE 
                WHEN estado = 'EN_BLANCO' THEN 'En blanco'
                WHEN estado = 'ANULADO' THEN 'Anulado'
                ELSE estado
            END as candidato,
            COUNT(*) as cant_votos,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM voto WHERE IDCircuito = %s)), 2) as porcentaje
        FROM voto 
        WHERE IDCircuito = %s AND estado IN ('EN_BLANCO', 'ANULADO')
        GROUP BY estado
        """
        
        cursor.execute(query_especiales, (id_circuito, id_circuito))
        votos_especiales = cursor.fetchall()
        
        return {
            "circuito_id": id_circuito,
            "resultados": resultados_candidatos + votos_especiales
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/resultados-departamento/{departamento}")
def get_resultados_departamento(departamento: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT departamento FROM circuito WHERE departamento = %s", (departamento,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Departamento no encontrado")
        
        query_partidos = """
        SELECT 
            pp.direccionSede as partido,
            COUNT(i.IDVoto) as votos,
            ROUND((COUNT(i.IDVoto) * 100.0 / (SELECT COUNT(*) FROM voto v2 INNER JOIN circuito c2 ON v2.IDCircuito = c2.ID WHERE c2.departamento = %s AND v2.estado = 'VALIDO')), 2) as porcentaje
        FROM partidoPolitico pp
        LEFT JOIN lista l ON pp.ID = l.IDPartidoPolitico
        LEFT JOIN incluye i ON l.numero = i.numeroLista
        LEFT JOIN voto v ON i.IDVoto = v.ID AND v.estado = 'VALIDO'
        LEFT JOIN circuito c ON v.IDCircuito = c.ID AND c.departamento = %s
        GROUP BY pp.ID, pp.direccionSede
        HAVING COUNT(i.IDVoto) > 0
        ORDER BY votos DESC
        """
        
        cursor.execute(query_partidos, (departamento, departamento))
        resultados_partidos = cursor.fetchall()
        
        query_especiales = """
        SELECT 
            CASE 
                WHEN v.estado = 'EN_BLANCO' THEN 'En Blanco'
                WHEN v.estado = 'ANULADO' THEN 'Anulado'
                ELSE v.estado
            END as partido,
            COUNT(*) as votos,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM voto v2 INNER JOIN circuito c2 ON v2.IDCircuito = c2.ID WHERE c2.departamento = %s)), 2) as porcentaje
        FROM voto v
        INNER JOIN circuito c ON v.IDCircuito = c.ID
        WHERE c.departamento = %s AND v.estado IN ('EN_BLANCO', 'ANULADO')
        GROUP BY v.estado
        """
        
        cursor.execute(query_especiales, (departamento, departamento))
        votos_especiales = cursor.fetchall()
        
        return {
            "departamento": departamento,
            "resultados": resultados_partidos + votos_especiales
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/ganadores-departamentos")
def get_ganadores_departamentos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        WITH resultados_departamento AS (
            SELECT 
                c.departamento,
                pp.direccionSede as partido,
                v.nombre as candidato,
                COUNT(i.IDVoto) as votos,
                ROW_NUMBER() OVER (PARTITION BY c.departamento ORDER BY COUNT(i.IDVoto) DESC) as ranking
            FROM candidato ca
            INNER JOIN Votante v ON ca.CC = v.CC
            INNER JOIN partidoPolitico pp ON ca.IDPartidoPolitico = pp.ID
            INNER JOIN lista l ON ca.CC = l.CCCandidato
            LEFT JOIN incluye i ON l.numero = i.numeroLista
            LEFT JOIN voto vt ON i.IDVoto = vt.ID AND vt.estado = 'VALIDO'
            LEFT JOIN circuito c ON vt.IDCircuito = c.ID
            GROUP BY c.departamento, ca.CC, v.nombre, pp.direccionSede
        )
        SELECT 
            departamento,
            candidato,
            partido,
            votos
        FROM resultados_departamento
        WHERE ranking = 1
        ORDER BY departamento
        """
        
        cursor.execute(query)
        ganadores = cursor.fetchall()
        
        return {"ganadores_por_departamento": ganadores}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/abrir-votacion/{id_circuito}")
def abrir_votacion(id_circuito: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (id_circuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Circuito no encontrado")
        
        return {"message": f"Votación abierta en el circuito {id_circuito}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/cerrar-votacion/{id_circuito}")
def cerrar_votacion(id_circuito: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (id_circuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Circuito no encontrado")
        
        return {"message": f"Votación cerrada en el circuito {id_circuito}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 