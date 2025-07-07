from fastapi import APIRouter, HTTPException, Depends
from typing import List
import pymysql
from ..db import get_connection
from ..models import OperadorLogin, OperadorResponse, OperadorCreate
from ..utils import verify_password, hash_password

router = APIRouter(prefix="/operadores", tags=["Operadores"])

@router.post("/login", response_model=OperadorResponse)
def login_operador(login_data: OperadorLogin):
    """Login de operador y retorna el ID del circuito al que pertenece"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Buscar operador por CC
        cursor.execute(
            "SELECT CC, organismoEstado, IDCircuito, password, rol FROM miembroMesa WHERE CC = %s",
            (login_data.CC,)
        )
        operador = cursor.fetchone()
        
        if not operador:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        # Verificar contraseña
        if not verify_password(login_data.password, operador['password']):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        return OperadorResponse(
            CC=operador['CC'],
            organismoEstado=operador['organismoEstado'],
            IDCircuito=operador['IDCircuito'],
            rol=operador['rol']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/{cc}", response_model=OperadorResponse)
def get_operador(cc: str):
    """Obtener operador por CC"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT CC, organismoEstado, IDCircuito, password, rol FROM miembroMesa WHERE CC = %s",
            (cc,)
        )
        operador = cursor.fetchone()
        
        if not operador:
            raise HTTPException(status_code=404, detail="Operador no encontrado")
        
        return OperadorResponse(
            CC=operador['CC'],
            organismoEstado=operador['organismoEstado'],
            IDCircuito=operador['IDCircuito'],
            rol=operador['rol']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/{cc}")
def delete_operador(cc: str):
    """Eliminar operador por CC"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT CC FROM miembroMesa WHERE CC = %s", (cc,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Operador no encontrado")
        
        # Eliminar operador
        cursor.execute("DELETE FROM miembroMesa WHERE CC = %s", (cc,))
        
        return {"message": "Operador eliminado exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=OperadorResponse)
def create_operador(operador_data: OperadorCreate):
    """Crear nuevo operador"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si el votante existe
        cursor.execute("SELECT CC FROM Votante WHERE CC = %s", (operador_data.CC,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="El votante no existe")
        
        # Verificar si el circuito existe
        cursor.execute("SELECT ID FROM circuito WHERE ID = %s", (operador_data.IDCircuito,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="El circuito no existe")
        
        # Verificar si ya existe un operador con ese CC
        cursor.execute("SELECT CC FROM miembroMesa WHERE CC = %s", (operador_data.CC,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Ya existe un operador con ese CC")
        
        # Hash de la contraseña
        hashed_password = hash_password(operador_data.password)
        
        # Insertar operador
        cursor.execute(
            "INSERT INTO miembroMesa (CC, organismoEstado, IDCircuito, password, rol) VALUES (%s, %s, %s, %s, %s)",
            (operador_data.CC, operador_data.organismoEstado, operador_data.IDCircuito, hashed_password, operador_data.rol)
        )
        
        return OperadorResponse(
            CC=operador_data.CC,
            organismoEstado=operador_data.organismoEstado,
            IDCircuito=operador_data.IDCircuito,
            rol=operador_data.rol
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        cursor.close()
        conn.close() 