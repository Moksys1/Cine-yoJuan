import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Butaca:
    def __init__(self, id_butaca=None, fila="", numero=0, id_sala=None, ocupada=False):
       self.id_butaca = id_butaca
       self.fila = fila
       self.numero = numero 
       self.id_sala = id_sala
       self.ocupada = ocupada

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)
    
    def ocupar(self):
        if not self.ocupada:
            self.ocupada = True
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute("UPDATE Butaca SET disponibilidad = 1 WHERE idButaca = ?", (self.id_butaca,))
            conexion.commit()
            conexion.close()
            return True
        return False

    def liberar(self):
        if self.ocupada:
            self.ocupada = False
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute("UPDATE Butaca SET disponibilidad = 0 WHERE idButaca = ?", (self.id_butaca,))
            conexion.commit()
            conexion.close()
            return True
        return False

    def __str__(self):
        estado = "Ocupada" if self.ocupada else "Libre"
        return f"butaca {self.fila}{self.numero}: ({estado})"

   