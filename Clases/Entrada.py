import sqlite3
import os
from .Cliente import Cliente
from .Pelicula import Pelicula
from .Funcion import Funcion
from .Butaca import Butaca
from .TipoEntrada import TipoEntrada

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
    
    def guardar_entrada(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()

        print("DEBUG BUTACA:", self.butaca)
        print("DEBUG id_butaca:", getattr(self.butaca, "id_butaca", None))


        cursor.execute("""
            INSERT INTO Entrada (idFuncion, idButaca, idCliente, idTipoEntrada, precioFinal)
            VALUES (?, ?, ?, ?, ?)
        """, (self.funcion.id_funcion, self.butaca.id_butaca, self.cliente.id_cliente, self.tipoEntrada.id_tipo, self.precio_final))

        conexion.commit()
        conexion.close()
        print("Entrada registrada correctamente.")

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
            WHERE num_cliente = ?
        """, (self.cliente.id_cliente,))
        cliente_info = cursor.fetchone()

        cursor.execute("""
            SELECT nombreButaca
            FROM Butaca
            WHERE idButaca = ?
        """, (self.butaca.id_butaca,))
        butaca_info = cursor.fetchone()

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

        ticket = f"""
        Cine YoJuan
    ──────────────────────────────
    Cliente: {nombre_cliente}
    Película: {titulo}
    Fecha y hora: {fecha_hora}
    Sala: {tipo_sala}
    Butaca: {butaca_nombre}
    Tipo de entrada: {tipo_entrada}
    ──────────────────────────────
    Total: ${self.precio_final:.2f}
    ¡Gracias por su compra!
    """

        with open("ticket_{nombre_cliente}.txt", "w") as f:
            f.write(ticket)

        print(ticket)
