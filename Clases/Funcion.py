import sqlite3
import os
from datetime import datetime
from .Pelicula import Pelicula
from .Sala import Sala
from config import DB_PATH

class Funcion:
    def __init__(self, pelicula_obj: Pelicula, sala_obj: Sala, id_funcion=None, fecha_hora=None, idioma="Español", formato="2D", precio_final= 0.0):
        self.id_funcion = id_funcion
        self.pelicula = pelicula_obj
        self.sala = sala_obj
        self.fecha_hora = fecha_hora or datetime.now()
        self.idioma = idioma
        self.formato = formato
        self.precio_final = precio_final

        idiomas_validos = ["Español", "Ingles(Subtitulada)"]
        formatos_validos = ["2D", "3D"]

        if self.idioma not in idiomas_validos:
            raise ValueError(f"Idioma inválido. Debe ser uno de: {idiomas_validos}")
        if self.formato not in formatos_validos:
            raise ValueError(f"Formato inválido. Debe ser uno de: {formatos_validos}")
        
    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    def guardar_funcion(self):
        conexion = self._get_connection()
        cursor = conexion.cursor()
        try:
            if self.id_funcion is None:
                cursor.execute("""
                    INSERT INTO Funcion (fechaHora, idioma, idSala, idpelicula)
                    VALUES (?, ?, ?, ?)                      
                """, (self.fecha_hora, 
                      self.idioma,
                      self.sala.idSala,
                      self.pelicula.id_pelicula
                ))
                self.id_funcion = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE Funcion
                    SET fechaHora=?, idioma=?,  idSala=?, idPelicula=?
                    WHERE idFuncion=?
                """, (self.fecha_hora, 
                      self.idioma,
                      self.sala.idSala,
                      self.pelicula.id_pelicula,
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
    def buscar_por_pelicula(id_pelicula):
        conexion = Funcion._get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT f.idFuncion, p.titulo, f.fechaHora, f.idioma, s.nombre AS Sala, s.tipoSala, s.precioBase, f.idSala
            FROM Funcion f
            INNER JOIN Pelicula p ON f.idPelicula = p.idPelicula
            INNER JOIN Sala s ON f.idSala = s.idSala
            WHERE p.idPelicula = ?
            ORDER BY f.fechaHora ASC
        """, (id_pelicula,))
        return cursor.fetchall()
    
    def mostrar_info(self):
        print(f"Función #{self.id_funcion} | Película: {self.pelicula.titulo if self.pelicula else 'N/A'} | "
              f"Sala: {self.sala.nombre if self.sala else 'N/A'} | "
              f"Fecha/Hora: {self.fecha_hora} | Idioma: {self.idioma} | Formato: {self.formato} | "
              f"Precio: ${self.precio_final}")
    
