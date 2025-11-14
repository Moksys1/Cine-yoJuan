import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Data", "SalaDeCine_DB.db")

# Crear carpeta /Data si no existe
if not os.path.exists(os.path.join(BASE_DIR, "Data")):
    os.makedirs(os.path.join(BASE_DIR, "Data"))