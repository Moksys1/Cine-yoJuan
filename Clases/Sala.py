import sqlite3
import os
from .Butaca import Butaca

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
    
    def guardar_sala(self):
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

    def generar_butacas(self):
        self.butacas = []
        if self.capacidad <= 0:
            print("No se pueden generar butacas sin capacidad definida.")
            return
        
        filas = columnas = int(self.capacidad ** 0.5)
        if filas * columnas < self.capacidad:
            columnas += 1

        contador = 0
        for f in range(1, filas + 1):
            letra_fila = chr(64 + f)
            for n in range(1, columnas + 1):
                if contador >= self.capacidad:
                    break
                nueva_butaca = Butaca(fila=letra_fila, numero=n, id_sala=self.idSala)
                self.butacas.append(nueva_butaca)
                contador += 1

    def mostrar_butacas(self):
        if not hasattr(self, "butacas") or not self.butacas:
            print("No hay butacas generadas aún.")
            return
        for butaca in self.butacas:
            print(butaca)
