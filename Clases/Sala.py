import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Sala:
    def __init__(self, idSala=None, nombre="", tipo="", capacidad=0, precioBase=0.0):
        self.__idSala = idSala
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        self._precioBase = precioBase

    @property
    def idSala(self):
        return self.__idSala

    @property
    def precioBase(self):
        return self._precioBase

    def set_precio_base(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("Precio no puede ser negativo.")
        self._precioBase = nuevo_precio


    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def obtener_todas():
        conexion = Sala._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idSala, nombre, tipoSala, precioBase FROM Sala")
        filas = cursor.fetchall()
        conexion.close()
        return [Sala(*fila, capacidad=None) for fila in filas] 

    @staticmethod
    def buscar_por_id(id_sala):
        conexion = Sala._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idSala, nombre, tipoSala, precioBase FROM Sala WHERE idSala=?", (id_sala,))
        fila = cursor.fetchone()
        conexion.close()
        return Sala(*fila, capacidad=None) if fila else None

    @staticmethod
    def buscar_por_tipo(tipo):
        conexion = Sala._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idSala, nombre, tipoSala, precioBase FROM Sala WHERE tipoSala=?", (tipo,))
        filas = cursor.fetchall()
        conexion.close()
        return [Sala(*fila, capacidad=None) for fila in filas]

    def mostrar_info(self):
        print(f"[{self.idSala}] {self.nombre} - {self.tipo} - Precio base: ${self.precioBase}")
