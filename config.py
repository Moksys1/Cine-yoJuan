# Archivo: config.py
# Archivo: config.py
import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

# --- RUTAS BASE ---
BASE_DIR = get_base_path()
DATA_DIR = os.path.join(BASE_DIR, "Data")

# --- RUTAS DE BASE DE DATOS ---
DB_NAME = "SalaDeCine_DB.db"
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

# --- RUTAS DE TICKETS (NUEVO) ---
# Definimos carpetas específicas dentro de Data para tener orden
DIR_TICKETS_ENTRADAS = os.path.join(DATA_DIR, "Entradas")
DIR_TICKETS_VENTAS = os.path.join(DATA_DIR, "Tickets_Venta")

# --- CREACIÓN DE CARPETAS ---
# Aseguramos que existan TODAS las carpetas necesarias
carpetas_a_crear = [DATA_DIR, DIR_TICKETS_ENTRADAS, DIR_TICKETS_VENTAS]

for carpeta in carpetas_a_crear:
    if not os.path.exists(carpeta):
        try:
            os.makedirs(carpeta)
            print(f"Carpeta creada: {carpeta}")
        except OSError as e:
            print(f"Error creando carpeta {carpeta}: {e}")

# import os
# import sys

# def resource_path(relative_path):
#     # Si estamos en el exe
#     if hasattr(sys, '_MEIPASS'):
#         base_path = sys._MEIPASS
#     else:
#         # Modo desarrollo (PyCharm, VSCode, etc.)
#         base_path = os.path.abspath(".")
    
#     return os.path.join(base_path, relative_path)

# # Ruta absoluta SIEMPRE, para Python o .exe
# DB_PATH = resource_path(os.path.join("Data", "SalaDeCine_DB.db"))

# # Crear carpeta Data si no existe
# data_dir = resource_path("Data")
# if not os.path.exists(data_dir):
#     os.makedirs(data_dir)
