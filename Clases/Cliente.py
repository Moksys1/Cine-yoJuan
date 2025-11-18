import sqlite3
import os
from .Persona import Persona
from config import DB_PATH

class Cliente(Persona):
    def __init__(self, dni, nombre, email, id_cliente=None):
        super().__init__(dni, nombre, email)
        self.id_cliente = id_cliente

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    def guardar_clientes(self):
        self.dni = input("Ingrese DNI del cliente: ")
        self.nombre = input("Ingrese nombre completo: ")
        self.email = input("Ingrese email: ")

        conexion = self._get_connection()
        cursor = conexion.cursor()

        if self.id_cliente is None:
            cursor.execute("""
                INSERT INTO Cliente (dni, nombre, email)
                VALUES (?, ?, ?)
            """, (self.dni, self.nombre, self.email))
            print(f"\nCliente {self.nombre} registrado correctamente.")
        else:
            cursor.execute("""
                UPDATE Cliente
                SET nombre= ?, email= ?
                WHERE idCliente=?
            """, (self.nombre, self.email, self.id_cliente))
            print(f"\nCliente {self.nombre} actualizado correctamente.")

        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_dni(dni):
        conexion = Cliente._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idCliente, dni, nombre, email FROM Cliente WHERE dni=?", (dni,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            id_cliente, dni, nombre, email = fila
            return Cliente(dni, nombre, email, id_cliente)
        else:
            print("No se encontró ningún cliente con ese DNI.")
            return None
        
    def eliminar(self):
        if self.id_cliente is None:
            print("El cliente no existe en la base de datos.")
            return
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Cliente WHERE idCliente = ?", (self.id_cliente,))
        conexion.commit()
        conexion.close()
        print(f"Cliente {self.nombre} eliminado correctamente.")
        
    def mostrar_info(self):
        print(f"Cliente N°{self.id_cliente}: Nombre y Apellido: {self.nombre} - DNI: {self.dni} - Email: {self.email}")

    def identificacion(self):
        return f"Cliente registrado: {self.nombre}"

