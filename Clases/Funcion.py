import sqlite3
import os
from datetime import datetime
from Pelicula import Pelicula
from Sala import Sala

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Funcion:
    def __init__(self, id_funcion=None, pelicula=None, sala=None, fecha_hora=None, idioma="2D", formato="Español", precio_final= 0.0):
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

