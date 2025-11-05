import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

class Persona:
    def __init__(self,dni,nombre,apellido,email):
        self.__dni = dni 
        self.nombre = nombre 
        self.apellido = apellido
        self.email = email
        
    @property
    def dni(self):
        return self.__dni
    
    @dni.setter
    def dni(self,nuevo_dni):
        self.__dni = nuevo_dni
