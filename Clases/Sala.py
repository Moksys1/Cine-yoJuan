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
    
    def guardar(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        try:
            if self.__idSala is None:
                cursor.execute("""
                    INSERT INTO Sala (nombre, tipoSala, capacidad, precioBase)
                    VALUES (?, ?, ?, ?)
                """, (self.nombre, self.tipo, self.capacidad, self._precioBase))
                self.__idSala = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE Sala
                    SET nombre=?, tipoSala=?, capacidad=?, precioBase=?
                    WHERE idSala=?
                """, (self.nombre, self.tipo, self.capacidad, self._precioBase, self.__idSala))
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = Sala._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idSala, nombre, tipoSala, capacidad, precioBase FROM Sala")
        filas = cursor.fetchall()
        conexion.close()
        return [Sala(*fila) for fila in filas] 

    @staticmethod
    def buscar_por_id(id_sala):
        conexion = Sala._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idSala, nombre, tipoSala, capacidad, precioBase FROM Sala WHERE idSala=?", (id_sala,))
        fila = cursor.fetchone()
        conexion.close()
        return Sala(*fila) if fila else None

    @staticmethod
    def buscar_por_tipo(tipo):
        conexion = Sala._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idSala, nombre, tipoSala, capacidad, precioBase FROM Sala WHERE tipoSala=?", (tipo,))
        filas = cursor.fetchall()
        conexion.close()
        return [Sala(*fila) for fila in filas]

    def mostrar_info(self):
        print(f"[{self.idSala}] {self.nombre} - {self.tipo} - Precio base: ${self.precioBase}")
