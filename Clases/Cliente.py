import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class cliente:
    def __init__(self,num_cliente,telefono):
     self.num_cliente = num_cliente 
     self.telefono = telefono
    staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)
    

    def guardad_cliente_nuevo(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute('''
    



''')



