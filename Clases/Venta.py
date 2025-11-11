import sqlite3
import os
from datetime import datetime
from Entrada import Entrada

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Venta:
    def __init__(self, cliente, entradas=None):
        self.cliente = cliente
        self.entradas = entradas if entradas else []
        self.total = 0.0
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    def agregar_entrada(self, entrada: Entrada):
        self.entradas.append(entrada)
        self.total += entrada.precio_final

    def calcular_total(self):
        self.total = sum(e.precio_final for e in self.entradas)
        return self.total

    def guardar_venta(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO Venta (num_cliente, fecha, total)
            VALUES (?, ?, ?)
        """, (self.cliente.num_cliente, self.fecha, self.total))
        id_venta = cursor.lastrowid

        for entrada in self.entradas:
            entrada.guardar_entrada()

        conexion.commit()
        conexion.close()
        print(f"Venta registrada correctamente (ID {id_venta})")

    def generar_ticket_final(self):
        ticket = f"""
        Cine YoJuan
        ──────────────────────────────
        Cliente: {self.cliente.nombre}
        Fecha: {self.fecha}
        ──────────────────────────────
        """
        for entrada in self.entradas:
            ticket += f"{entrada.funcion.id_funcion} - Butaca {entrada.butaca.fila}{entrada.butaca.numero} - ${entrada.precio_final:.2f}\n"

        ticket += f"──────────────────────────────\nTotal: ${self.total:.2f}\n¡Gracias por su compra!\n"

        with open("ticket_final.txt", "w", encoding="utf-8") as f:
            f.write(ticket)

        print(ticket)
