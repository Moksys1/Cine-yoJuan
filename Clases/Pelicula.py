import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Pelicula:
    def __init__(self, id_pelicula=None, titulo="", duracion=0, genero="", clasificacion=""):
        self.id = id
        self.titulo = titulo
        self.duracion = duracion
        self.genero = genero
        self.clasificacion = clasificacion

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)
    
    def guardar_pelicula(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        if self.id_pelicula is None:
            cursor.execute("""
                INSERT INTO Pelicula (titulo, duracion, genero, clasificacion)
                VALUES (?, ?, ?, ?)
            """, (self.titulo, self.duracion, self.genero, self.clasificacion))
        else:
            cursor.execute("""
                UPDATE Pelicula
                SET titulo=?, duracion=?, genero=?, clasificacion=?
                WHERE idPelicula=?
            """, (self.titulo, self.duracion, self.genero, self.clasificacion, self.id_pelicula))
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = Pelicula._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idPelicula, titulo, duracion, genero, clasificacion FROM Pelicula")
        filas = cursor.fetchall()
        conexion.close()
        return [Pelicula(*fila) for fila in filas]
    
    @staticmethod
    def buscar_por_id(id_pelicula):
        conexion = Pelicula._get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT idPelicula, titulo, duracion, genero, clasificacion FROM Pelicula WHERE idPelicula=?", (id_pelicula,))
        fila = cursor.fetchone()
        conexion.close()
        return Pelicula(*fila) if fila else None
    
    def eliminar(self):
        if self.id_pelicula is None:
            print("No se puede eliminar: la película no tiene ID asignado.")
            return
        conexion = self._get_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Pelicula WHERE idPelicula=?", (self.id_pelicula,))
        conexion.commit()
        conexion.close()

    def mostrar_info(self):
        print(f"Titulo: {self.titulo} - Duracion: {self.duracion} - Genero: {self.genero} - Clasificacion: {self.clasificacion}")