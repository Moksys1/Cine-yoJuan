import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
from config import DB_PATH, DIR_REPORTES

class Reportes:

    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_PATH)

    # -----------------------------------------------------------
    # 1) Ventas por película
    # -----------------------------------------------------------
    @staticmethod
    def ventas_por_pelicula():
        print("Generando reporte de ventas por película...")
        conexion = Reportes._get_connection()

        # CORRECCIÓN IMPORTANTE:
        # La tabla 'Entrada' NO tiene 'idPelicula'. 
        # Hacemos JOIN con 'Funcion' para llegar a la 'Pelicula'.
        query = """
        SELECT Pelicula.titulo AS Pelicula, 
               COUNT(Entrada.idEntrada) AS EntradasVendidas
        FROM Entrada
        JOIN Funcion ON Entrada.idFuncion = Funcion.idFuncion
        JOIN Pelicula ON Funcion.idPelicula = Pelicula.idPelicula
        GROUP BY Pelicula.idPelicula
        ORDER BY EntradasVendidas DESC;
        """

        try:
            df = pd.read_sql_query(query, conexion)
        except Exception as e:
            print(f"Error ejecutando consulta SQL (Ventas): {e}")
            conexion.close()
            return

        conexion.close()

        if df.empty:
            print("⚠ No hay ventas registradas para generar el reporte.")
            return

        # Guardar CSV
        csv_path = os.path.join(DIR_REPORTES, "ventas_por_pelicula.csv")
        df.to_csv(csv_path, index=False)
        print(f"✔ CSV generado: {csv_path}")

        # Guardar Gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(df["Pelicula"], df["EntradasVendidas"], color='skyblue')
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Cantidad de Entradas")
        plt.title("Ventas por Película")
        plt.tight_layout()

        img_path = os.path.join(DIR_REPORTES, "ventas_por_pelicula.png")
        plt.savefig(img_path)
        plt.close()
        print(f"✔ Gráfico generado: {img_path}")

    # -----------------------------------------------------------
    # 2) Clientes que más compran
    # -----------------------------------------------------------
    @staticmethod
    def clientes_top():
        print("Generando reporte de clientes top...")
        conexion = Reportes._get_connection()
        
        # CORRECCIÓN: Usamos los nombres exactos de tu tabla Cliente
        # (idCliente, nombre, dni, email)
        query = """
        SELECT Cliente.nombre AS Cliente,
               COUNT(Entrada.idEntrada) AS Compras
        FROM Entrada
        JOIN Cliente ON Entrada.idCliente = Cliente.idCliente
        GROUP BY Cliente.idCliente
        ORDER BY Compras DESC
        LIMIT 10; 
        """

        try:
            df = pd.read_sql_query(query, conexion)
        except Exception as e:
            print(f"Error SQL (Clientes): {e}")
            conexion.close()
            return
            
        conexion.close()

        if df.empty:
            print("⚠ No hay compras registradas de clientes.")
            return

        # Guardar CSV
        csv_path = os.path.join(DIR_REPORTES, "clientes_top.csv")
        df.to_csv(csv_path, index=False)
        print(f"✔ CSV generado: {csv_path}")

        # Guardar Gráfico
        plt.figure(figsize=(8, 8))
        plt.pie(df["Compras"], labels=df["Cliente"], autopct="%1.1f%%", startangle=140)
        plt.title("Clientes con más compras")
        plt.tight_layout()

        img_path = os.path.join(DIR_REPORTES, "clientes_top.png")
        plt.savefig(img_path)
        plt.close()
        print(f"✔ Gráfico generado: {img_path}")

    # -----------------------------------------------------------
    # 3) Películas con más funciones (Ocupación de cartelera)
    # -----------------------------------------------------------
    @staticmethod
    def peliculas_mas_funciones():
        print("Generando reporte de funciones...")
        conexion = Reportes._get_connection()

        # CORRECCIÓN: Relación directa entre Funcion y Pelicula
        query = """
        SELECT Pelicula.titulo AS Pelicula,
               COUNT(Funcion.idFuncion) AS CantidadFunciones
        FROM Funcion
        JOIN Pelicula ON Funcion.idPelicula = Pelicula.idPelicula
        GROUP BY Pelicula.idPelicula
        ORDER BY CantidadFunciones DESC;
        """

        try:
            df = pd.read_sql_query(query, conexion)
        except Exception as e:
            print(f"Error SQL (Funciones): {e}")
            conexion.close()
            return

        conexion.close()

        if df.empty:
            print("⚠ No hay funciones cargadas.")
            return

        # Guardar CSV
        csv_path = os.path.join(DIR_REPORTES, "peliculas_mas_funciones.csv")
        df.to_csv(csv_path, index=False)
        print(f"✔ CSV generado: {csv_path}")

        # Guardar Gráfico
        plt.figure(figsize=(10, 5))
        plt.bar(df["Pelicula"], df["CantidadFunciones"], color='lightgreen')
        plt.xticks(rotation=45, ha="right")
        plt.title("Películas con más funciones programadas")
        plt.tight_layout()

        img_path = os.path.join(DIR_REPORTES, "peliculas_mas_funciones.png")
        plt.savefig(img_path)
        plt.close()
        print(f"✔ Gráfico generado: {img_path}")

# Bloque para probarlo ejecutando este archivo directamente
if __name__ == "__main__":
    Reportes.ventas_por_pelicula()
    Reportes.clientes_top()
    Reportes.peliculas_mas_funciones()