import sqlite3
import os
from datetime import datetime
from .Cliente import Cliente
from config import DB_PATH

class Venta:
    def __init__(self, cliente, entradas=None):
        self.cliente = cliente
        self.entradas = entradas if entradas else []
        self.total = 0.0
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    def agregar_entrada(self, entrada):
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
        """, (self.cliente.id_cliente, self.fecha, self.total))
        id_venta = cursor.lastrowid

        conexion.commit()
        conexion.close()
        print(f"Venta registrada correctamente (ID {id_venta})")
        return id_venta

    def generar_ticket_venta(self):
        from .Entrada import Entrada
        import os
        from datetime import datetime

        # Crear carpeta si no existe
        base_dir = os.path.dirname(os.path.abspath(__file__))
        tickets_dir = os.path.join(base_dir, "..", "Tickets de Venta")
        os.makedirs(tickets_dir, exist_ok=True)

        # Nombre del archivo
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nombre_archivo = f"ticket_venta_{self.cliente.nombre}_{fecha_actual}.txt"
        ruta_ticket = os.path.join(tickets_dir, nombre_archivo)

        # Construcción del ticket
        ticket = "-------------------------------------\n"
        ticket += "       CINE YOJUAN - TICKET DE VENTA\n"
        ticket += "-------------------------------------\n"
        ticket += f"Cliente: {self.cliente.nombre}\n"
        ticket += f"Fecha: {self.fecha}\n"
        ticket += "-------------------------------------\n"
        ticket += "Entradas compradas:\n"

        for entrada in self.entradas:
            ticket += (
                f"  - Película: {entrada.funcion.pelicula.titulo} | "
                f"Función: {entrada.funcion.fecha_hora} | "
                f"Butaca {entrada.butaca.fila}{entrada.butaca.numero} | "
                f"${entrada.precio_final:.2f}\n"
            )
        ticket += "-------------------------------------\n"
        ticket += f"Total: ${self.total:.2f}\n"
        ticket += "-------------------------------------\n"
        ticket += "¡Gracias por tu compra!\n"

        # Guardar ticket en archivo
        with open(ruta_ticket, "w", encoding="utf-8") as f:
            f.write(ticket)

        print(ticket)
        print(f"Ticket guardado en: {ruta_ticket}")
