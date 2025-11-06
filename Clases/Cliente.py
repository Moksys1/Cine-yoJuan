import sqlite3
import os
from .Persona import Persona

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Cliente(Persona):
    def __init__(self, dni, nombre, email, num_cliente=None, telefono=""):
        super().__init__(dni, nombre, email)
        self.num_cliente = num_cliente
        self.telefono = telefono

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    def guardar_clientes(self):
        self.dni = input("Ingrese DNI del cliente: ")
        self.nombre = input("Ingrese nombre completo: ")
        self.email = input("Ingrese email: ")
        self.telefono = input("Ingrese teléfono: ")

        conexion = self._get_connection()
        cursor = conexion.cursor()

        if self.num_cliente is None:
            cursor.execute("""
                INSERT INTO Cliente (dni, nombre, email, telefono)
                VALUES (?, ?, ?, ?)
            """, (self.dni, self.nombre, self.email, self.telefono))
            print(f"\nCliente {self.nombre} registrado correctamente.")
        else:
            cursor.execute("""
                UPDATE Cliente
                SET nombre= ?, email= ?, telefono= ?
                WHERE num_cliente=?
            """, (self.nombre, self.email, self.telefono, self.num_cliente))
            print(f"\nCliente {self.nombre} actualizado correctamente.")

        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_dni(dni):
        conexion = Cliente._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT num_cliente, dni, nombre, email, telefono FROM Cliente WHERE dni=?", (dni,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            num_cliente, dni, nombre, email, telefono = fila
            return Cliente(dni, nombre, email, num_cliente, telefono)
        else:
            print("No se encontró ningún cliente con ese DNI.")
            return None
        
    def eliminar(self):
        if self.num_cliente is None:
            print("El cliente no existe en la base de datos.")
            return
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Cliente WHERE num_cliente = ?", (self.num_cliente,))
        conexion.commit()
        conexion.close()
        print(f"Cliente {self.nombre} eliminado correctamente.")
        
    def mostrar_info(self):
        print(f"Cliente N°{self.num_cliente}: Nombre y Apellido: {self.nombre} - DNI: {self.dni} - Email: {self.email} - Tel: {self.telefono}")
