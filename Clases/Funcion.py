import sqlite3
from datetime import date,time




class Funcion:
    def __init__(self,id_funcion:int, fecha: date,hora:time,precio:float):
        self.id_funcion=id_funcion
        self.fecha=fecha
        self.hora=hora
        self.precio=precio 
    def __str__(self):      #devuelve una cadena legible al imprimir el objeto
       return f"Funcion {self.id_funcion}:{self.fecha} {self.hora}- ${self.precio:.2f}"


#creacion de base de datos 
conn = sqlite3.connect('cine.db')
cursor=conn.cursor()
cursor.execute("""
    create table if not exists Funcion
        id_funcion interger primary key autoincrement ,
        fun_fecha date ,
        fun_hora time ,
        fun_precio float
            """)
conn.commit()  
conn.close()
print("la tabla funcion fue creada con exito")


# def getDisponibilidad(self):  


#     if total == 0:
#         return "no hay butacas disponibles"
#     return f"asientos disponibles: