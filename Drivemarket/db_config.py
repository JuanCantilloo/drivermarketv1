# db_config.py

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from db_settings import get_psycopg2_params

load_dotenv(encoding="utf-8")

# ---------------------------------------------------------------
# ⚙️ GESTIÓN CENTRALIZADA DE BASE DE DATOS (PostgreSQL)
# ---------------------------------------------------------------
_conexion_real = None

def get_db():
    """Retorna una conexión activa al servidor, reconectando si es necesario."""
    global _conexion_real
    
    try:
        # Si la conexión no existe o está cerrada, intentar reconectar
        if _conexion_real is None or (hasattr(_conexion_real, 'closed') and _conexion_real.closed):
            _conexion_real = psycopg2.connect(**get_psycopg2_params())
            _conexion_real.autocommit = False
    except UnicodeDecodeError:
        print(
            "[db_config] Error conectando a PostgreSQL. Revisa DB_HOST, "
            "DB_USER, DB_PASSWORD, DB_NAME y que el servicio este activo."
        )
        _conexion_real = None
    except (psycopg2.InterfaceError, psycopg2.OperationalError, Exception) as e:
        print("[db_config] Error reconectando a PostgreSQL:", e)
        _conexion_real = None
        
    return _conexion_real

class DBProxy:
    """Objeto Proxy que redirige todas las llamadas a la conexión real actual."""
    def __getattr__(self, name):
        conn = get_db()
        if conn is None:
            raise psycopg2.OperationalError("No se pudo establecer conexión con la base de datos.")
        return getattr(conn, name)

# Esta es la variable que todos los módulos importan
conexion = DBProxy()

# Inicialización primaria
get_db()
