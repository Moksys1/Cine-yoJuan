import sqlite3
import os
from .Cliente import Cliente
from .Pelicula import Pelicula
from .Funcion import Funcion
from .Butaca import Butaca
from .TipoEntrada import TipoEntrada
from datetime import datetime
from .Venta import Venta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Entrada:
    def __init__(self, cliente: Cliente, funcion: Funcion, butaca: Butaca, tipoEntrada: TipoEntrada, cantidad=1, precio_final=0.0):
        self.cliente = cliente
        self.funcion = funcion
        self.butaca = butaca
        self.tipoEntrada = tipoEntrada
        self.cantidad = cantidad
        self.precio_final = precio_final

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)
    
    def calcular_total(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT s.tipoSala, s.precioBase
            FROM Funcion f
            JOIN Sala s ON f.idSala = s.idSala
            WHERE f.idFuncion = ?
        """, (self.funcion.id_funcion,))
        sala = cursor.fetchone()

        cursor.execute("""
            SELECT descuento
            FROM tipoEntrada
            WHERE idTipoEntrada = ?
        """, (self.tipoEntrada.id_tipo,))
        tipoEntrada = cursor.fetchone()

        conexion.close()

        if not sala or not tipoEntrada:
            print("No se encontro la función o el tipo de entrada.")
            return
        
        precioBase = float(sala[1])         
        descuento = float(tipoEntrada[0])
        self.precio_final = round(precioBase * self.cantidad * (1 - descuento), 2)

        return self.precio_final
    
    def guardar_entrada(self, id_venta=None):
        conexion = self._get_connection()
        cursor = conexion.cursor()

        if id_venta is not None:
            cursor.execute("""
                INSERT INTO Entrada (idFuncion, idButaca, idCliente, idTipoEntrada, precioFinal)
                VALUES (?, ?, ?, ?, ?)
            """, (self.funcion.id_funcion, self.butaca.id_butaca, self.cliente.id_cliente, self.tipoEntrada.id_tipo, self.precio_final))
        else:
            cursor.execute("""
                INSERT INTO Entrada (idFuncion, idButaca, idCliente, idTipoEntrada, precioFinal)
                VALUES (?, ?, ?, ?, ?)
            """, (self.funcion.id_funcion, self.butaca.id_butaca, self.cliente.id_cliente, self.tipoEntrada.id_tipo, self.precio_final))

        conexion.commit()
        conexion.close()
        print("Entrada registrada correctamente.")

    @staticmethod
    def obtener_por_funcion(id_funcion):
        """
        Devuelve todas las entradas asociadas a una función específica.
        """
        conexion = Entrada._get_connection()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT idEntrada, idFuncion, idButaca, idCliente, idTipoEntrada, precioFinal
            FROM Entrada
            WHERE idFuncion = ?
        """, (id_funcion,))

        entradas = cursor.fetchall()
        conexion.close()
        return entradas

    def generar_ticket(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT p.titulo, f.fechaHora, s.tipoSala
            FROM Funcion f
            JOIN Pelicula p ON f.idPelicula = p.idPelicula
            JOIN Sala s ON f.idSala = s.idSala
            WHERE f.idFuncion = ?
        """, (self.funcion.id_funcion,))
        funcion_info = cursor.fetchone()

        cursor.execute("""
            SELECT nombre
            FROM Cliente
            WHERE idCliente = ?
        """, (self.cliente.id_cliente,))
        cliente_info = cursor.fetchone()

        cursor.execute("""
            SELECT fila, numero
            FROM Butaca
            WHERE idButaca = ?
        """, (self.butaca.id_butaca,))
        butaca_info = cursor.fetchone()
        fila, numero = butaca_info
        butaca_texto = f"{fila}{numero}"

        cursor.execute("""
            SELECT descripcion
            FROM TipoEntrada
            WHERE idTipoEntrada = ?
        """, (self.tipoEntrada.id_tipo,))
        tipo_info = cursor.fetchone()

        conexion.close()

        if not (funcion_info and cliente_info and butaca_info and tipo_info):
            print("Faltan datos para generar el ticket.")
            return

        titulo, fecha_hora, tipo_sala = funcion_info
        nombre_cliente = cliente_info[0]
        butaca_nombre = butaca_info[0]
        tipo_entrada = tipo_info[0]

        fecha_hora_obj = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")

        ticket = f"""
        Cine YoJuan
    ──────────────────────────────
    Cliente: {nombre_cliente}
    Película: {titulo}
    Fecha y hora: {fecha_hora}
    Sala: {tipo_sala}
    Butaca: {butaca_texto}
    Tipo de entrada: {tipo_entrada}
    ──────────────────────────────
    Total: ${self.precio_final:.2f}
    ¡Gracias por su compra!
    """

        base_dir = os.path.dirname(os.path.abspath(__file__))
        tickets_dir = os.path.join(base_dir, "..", "Entradas")
        os.makedirs(tickets_dir, exist_ok=True)

        nombre_archivo = f"ticket_{nombre_cliente}_{fecha_hora_obj.strftime('%Y-%m-%d_%H-%M')}_{butaca_texto}.txt"
        ruta_ticket = os.path.join(tickets_dir, nombre_archivo)

        with open(ruta_ticket, "w", encoding="utf-8") as f:
            f.write(ticket)

        print(f"Ticket generado: {ruta_ticket}")
