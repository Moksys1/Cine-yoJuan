import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

BASE_DIR = get_base_path()
DATA_DIR = os.path.join(BASE_DIR, "Data")

DB_NAME = "SalaDeCine_DB.db"
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

DIR_TICKETS_ENTRADAS = os.path.join(DATA_DIR, "Entradas")
DIR_TICKETS_VENTAS = os.path.join(DATA_DIR, "Tickets_Venta")
DIR_REPORTES = os.path.join(DATA_DIR, "Reportes")

carpetas_a_crear = [DATA_DIR, DIR_TICKETS_ENTRADAS, DIR_TICKETS_VENTAS, DIR_REPORTES]

for carpeta in carpetas_a_crear:
    if not os.path.exists(carpeta):
        try:
            os.makedirs(carpeta)
            print(f"Carpeta creada: {carpeta}")
        except OSError as e:
            print(f"Error creando carpeta {carpeta}: {e}")