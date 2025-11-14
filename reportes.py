import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

class Reportes:

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "SalaDeCine_DB.db")
    REPORT_DIR = os.path.join(BASE_DIR, "data", "reportes")

    @staticmethod
    def _get_connection():
        return sqlite3.connect(Reportes.DB_PATH)

    @staticmethod
    def _asegurar_directorio():
        if not os.path.exists(Reportes.REPORT_DIR):
            os.makedirs(Reportes.REPORT_DIR)

    # -----------------------------------------------------------
    # 1) Ventas por película
    # -----------------------------------------------------------
    @staticmethod
    def ventas_por_pelicula():
        Reportes._asegurar_directorio()

        conexion = Reportes._get_connection()

        query = """
        SELECT Peliculas.nombre AS Pelicula,
               COUNT(Entradas.idEntrada) AS EntradasVendidas
        FROM Entradas
        JOIN Peliculas ON Entradas.idPelicula = Peliculas.idPelicula
        GROUP BY Peliculas.idPelicula
        ORDER BY EntradasVendidas DESC;
        """

        df = pd.read_sql_query(query, conexion)
        conexion.close()

        csv_path = os.path.join(Reportes.REPORT_DIR, "ventas_por_pelicula.csv")
        df.to_csv(csv_path, index=False)
        print("✔ Reporte CSV generado:", csv_path)

        # gráfico
        plt.figure(figsize=(10, 5))
        plt.bar(df["Pelicula"], df["EntradasVendidas"])
        plt.xticks(rotation=45, ha="right")
        plt.title("Ventas por película")
        plt.tight_layout()

        img_path = os.path.join(Reportes.REPORT_DIR, "ventas_por_pelicula.png")
        plt.savefig(img_path)
        plt.close()

        print("✔ Gráfico generado:", img_path)

    # -----------------------------------------------------------
    # 2) Clientes que más compran
    # -----------------------------------------------------------
    @staticmethod
    def clientes_top():
        Reportes._asegurar_directorio()

        conexion = Reportes._get_connection()
        query = """
        SELECT Clientes.nombre || ' ' || Clientes.apellido AS Cliente,
               COUNT(Entradas.idEntrada) AS Compras
        FROM Entradas
        JOIN Clientes ON Entradas.idCliente = Clientes.idCliente
        GROUP BY Clientes.idCliente
        ORDER BY Compras DESC;
        """

        df = pd.read_sql_query(query, conexion)
        conexion.close()

        csv_path = os.path.join(Reportes.REPORT_DIR, "clientes_top.csv")
        df.to_csv(csv_path, index=False)
        print("✔ Reporte CSV generado:", csv_path)

        # gráfico (torta / pie)
        plt.figure(figsize=(7, 7))
        plt.pie(df["Compras"], labels=df["Cliente"], autopct="%1.1f%%")
        plt.title("Clientes con más compras")

        img_path = os.path.join(Reportes.REPORT_DIR, "clientes_top.png")
        plt.savefig(img_path)
        plt.close()

        print("✔ Gráfico generado:", img_path)

    # -----------------------------------------------------------
    # 3) Películas con más funciones
    # -----------------------------------------------------------
    @staticmethod
    def peliculas_mas_funciones():
        Reportes._asegurar_directorio()

        conexion = Reportes._get_connection()

        query = """
        SELECT Peliculas.nombre AS Pelicula,
               COUNT(Funciones.idFuncion) AS CantidadFunciones
        FROM Funciones
        JOIN Peliculas ON Funciones.idPelicula = Peliculas.idPelicula
        GROUP BY Peliculas.idPelicula
        ORDER BY CantidadFunciones DESC;
        """

        df = pd.read_sql_query(query, conexion)
        conexion.close()

        csv_path = os.path.join(Reportes.REPORT_DIR, "peliculas_mas_funciones.csv")
        df.to_csv(csv_path, index=False)

        print("✔ Reporte CSV generado:", csv_path)

        # gráfico de barras
        plt.figure(figsize=(10, 5))
        plt.bar(df["Pelicula"], df["CantidadFunciones"])
        plt.xticks(rotation=45, ha="right")
        plt.title("Películas con más funciones")
        plt.tight_layout()

        img_path = os.path.join(Reportes.REPORT_DIR, "peliculas_mas_funciones.png")
        plt.savefig(img_path)
        plt.close()

        print("✔ Gráfico generado:", img_path)
