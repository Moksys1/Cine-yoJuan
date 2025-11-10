import sqlite3
import os
from datetime import datetime
from Pelicula import Pelicula
from Sala import Sala

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Funcion:
    def __init__(self, id_funcion=None, pelicula=None, sala=None, fecha_hora=None, idioma="Español", formato="2D", precio_final= 0.0):
        self.id_funcion = id_funcion
        self.pelicula = pelicula
        self.sala = sala
        self.fecha_hora = fecha_hora or datetime.now()
        self.idioma = idioma
        self.formato = formato
        self.precio_final = self.sala.precioBase if sala else 0.0

        idiomas_validos = ["Español", "Ingles(Subtitulada)"]
        formatos_validos = ["2D", "3D"]

        if self.idioma not in idiomas_validos:
            raise ValueError(f"Idioma inválido. Debe ser uno de: {idiomas_validos}")
        if self.formato not in formatos_validos:
            raise ValueError(f"Formato inválido. Debe ser uno de: {formatos_validos}")
        
    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    def guardar_funcion(self, conexion):
        cursor = conexion.cursor()
        try:
            if self.id_funcion is None:
                cursor.execute("""
                    INSERT INTO Funcion (idpelicula, idSala, fechaHora, idioma, formato, precio_final)
                    VALUES (?, ?, ?, ?, ?, ?)                      
                """, (self.pelicula.id_pelicula if self.pelicula else None, 
                      self.sala.idSala if self.sala else None, 
                      self.fecha_hora, 
                      self.idioma, 
                      self.formato, 
                      self.precio_final
                ))
                self.id_funcion = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE Funcion
                    SET idPelicula=?, idSala=?, fechaHora=?, idioma=?, formato=?, precioFinal=?
                    WHERE idFuncion=?
                """, (self.pelicula.id_pelicula if self.pelicula else None, 
                      self.sala.idSala if self.sala else None, 
                      self.fecha_hora, 
                      self.idioma, 
                      self.formato, 
                      self.precio_final,
                      self.id_funcion
                ))
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def obtener_todas():
        conexion = Funcion._get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT idFuncion, idPelicula, IdSala, fechaHora, idioma, formato, precioFinal
            FROM Funcion
        """)
        filas = cursor.fetchall()
        conexion.close()
        return filas
    
    @staticmethod
    def buscar_por_id(id_funcion):
        conexion = Funcion._get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT idFuncion, idPelicula, idSala, fechaHora, idioma, formato, precioFinal
            FROM Funcion
            WHERE idFuncion=?
        """, (id_funcion,))
        fila = cursor.fetchone()
        conexion.close()
        return fila

    @staticmethod
    def buscar_por_pelicula(conexion, id_pelicula):
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT f.idFuncion, p.titulo, f.fecha_hora, f.idioma, s.formato, s.nombre AS Sala, f.precio_final
            FROM Funcion f
            INNER JOIN Pelicula p ON f.idPelicula = p.idPelicula
            INNER JOIN Sala s ON f.idSala = s.idSala
            WHERE p.idPelicula = ?
            ORDER BY f.fecha_hora ASC
        """, (id_pelicula,))
        return cursor.fetchall()
    
    def mostrar_info(self):
        print(f"Función #{self.id_funcion} | Película: {self.pelicula.titulo if self.pelicula else 'N/A'} | "
              f"Sala: {self.sala.nombre if self.sala else 'N/A'} | "
              f"Fecha/Hora: {self.fecha_hora} | Idioma: {self.idioma} | Formato: {self.formato} | "
              f"Precio: ${self.precio_final}")
    
