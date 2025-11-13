import sqlite3
import os
from .Butaca import Butaca
from .Funcion import Funcion

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class ButacaFuncion:
    def __init__(self, id_butaca_funcion=None, funcion=None, butaca=None, estado="Libre"):
        self.id_butaca_funcion = id_butaca_funcion
        self.funcion = funcion
        self.butaca = butaca
        self.estado = estado

    def ocupar(self):
        if self.estado == "Libre":
            self.estado = "Ocupada"
            return True
        return False
    
    def liberar(self):
        if self.estado == "Ocupada":
            self.estado = "Libre"
            return True
        return False
    
    def mostrar_info(self):
        print(f"Butaca {self.butaca.fila}{self.butaca.numero} | "
              f"Función #{self.funcion.id_funcion} ({self.funcion.pelicula.titulo}) | "
              f"Estado: {self.estado}")

    # 🧠 Nuevo método para mostrar mapa de butacas
    @staticmethod
    def mostrar_mapa(funcion):
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # 1️⃣ Obtener todas las butacas de la sala de esa función
        cursor.execute("""
            SELECT idButaca, fila, numero 
            FROM Butaca 
            WHERE idSala = ?
        """, (funcion.sala.id_sala,))
        butacas = cursor.fetchall()

        # 2️⃣ Obtener las butacas ocupadas de esa función
        cursor.execute("""
            SELECT idButaca 
            FROM Entrada 
            WHERE idFuncion = ?
        """, (funcion.id_funcion,))
        ocupadas = {fila[0] for fila in cursor.fetchall()}

        conexion.close()

        # 3️⃣ Crear lista de ButacaFuncion
        butacas_funcion = []
        for id_butaca, fila, numero in butacas:
            estado = "Ocupada" if id_butaca in ocupadas else "Libre"
            butaca_obj = Butaca(id_butaca, fila, numero, funcion.sala.id_sala, estado == "Ocupada")
            butacas_funcion.append(ButacaFuncion(None, funcion, butaca_obj, estado))

        # 4️⃣ Mostrar mapa visual
        print(f"\n=== Mapa de butacas - {funcion.pelicula.titulo} ({funcion.fecha_hora}) ===")
        filas = sorted(set([b.butaca.fila for b in butacas_funcion]))
        numeros = sorted(set([b.butaca.numero for b in butacas_funcion]))

        for f in filas:
            fila_str = f"{f}: "
            for n in numeros:
                b = next((bf for bf in butacas_funcion if bf.butaca.fila == f and bf.butaca.numero == n), None)
                if b:
                    fila_str += "🟥 " if b.estado == "Ocupada" else "🟩 "
            print(fila_str)
        print("\n🟩 Libre   🟥 Ocupada")

        return butacas_funcion