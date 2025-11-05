import sqlite3
import os
from .Persona import Persona

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Cliente(Persona):
    def __init__(self, dni, nombre, apellido, email, num_cliente=None, telefono=""):
        super().__init__(dni, nombre, apellido, email)
        self.num_cliente = num_cliente
        self.telefono = telefono

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    def guardar_Clientes (self):
        conexion = self._get_connection()
        cursor = conexion.cursor()

        if self.num_cliente :
            cursor.execute("""
                INSERT INTO Cliente (dni, nombre, apellido, email, telefono)
                VALUES (?, ?, ?, ?, ?)
            """, (self.dni, self.nombre, self.apellido, self.email, self.telefono))
        else:
            cursor.execute("""
                UPDATE Cliente
                SET nombre= ?, apellido= ?, email= ?, telefono= ?
                WHERE num_cliente=?
            """, (self.nombre, self.apellido, self.email, self.telefono, self.num_cliente))

        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_dni(dni):
        conexion = Cliente._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT num_cliente, dni, nombre, apellido, email, telefono FROM Cliente WHERE dni=?", (dni,))
        fila = cursor.fetchone()
        conexion.close()
        return Cliente(fila[1], fila[2], fila[3], fila[4], fila[0], fila[5]) if fila else None

    def mostrar_info(self):
        print(f"Cliente N°{self.num_cliente}: {self.nombre} {self.apellido} (DNI {self.dni}) - Tel: {self.telefono}")
