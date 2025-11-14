import sqlite3
import os
from config import DB_PATH

class TipoEntrada:
    def __init__(self, id_tipo=None, descripcion= "", descuento=0.0):
        self.id_tipo = id_tipo
        self.descripcion = descripcion
        self.descuento = descuento

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)
    
    def guardar_tipoEntrada(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO tipoEntrada (descripcion, descuento)
            VALUES (?, ?)
            """, (self.descripcion, self.descuento))
        conexion.commit()
        conexion.close()
    
    def listar(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM tipoEntrada")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    
    @staticmethod
    def buscar_por_id(self, id_tipo):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM tipoEntrada WHERE idTipoEntrada = ?", (id_tipo,))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            return TipoEntrada(resultado[0], resultado[1], resultado[2])
        return None
    
    @staticmethod
    def listar_todos():
        conexion = TipoEntrada._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idTipoEntrada, descripcion, descuento FROM tipoEntrada")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados