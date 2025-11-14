import sqlite3
import os

def crear_base():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "SalaDeCine_DB.db")

    conexion = sqlite3.connect(DB_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()

    cursor.execute("DROP TABLE IF EXISTS Butaca;")
    cursor.execute("DROP TABLE IF EXISTS Sala;")

    cursor.execute("""
        DROP TABLE IF EXISTS Sala;
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sala (
        idSala INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipoSala TEXT NOT NULL,
        capacidad INTEGER NOT NULL,
        precioBase REAL NOT NULL
        ); """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pelicula (
        idPelicula INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        duracion INTEGER NOT NULL,
        genero TEXT NOT NULL,
        clasificacion TEXT NOT NULL
        ); """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Funcion (
        idFuncion INTEGER PRIMARY KEY AUTOINCREMENT,
        fechaHora TEXT NOT NULL,
        idioma TEXT NOT NULL,
        idSala INTEGER NOT NULL,
        idPelicula INTEGER NOT NULL,
        CONSTRAINT 'fk_idsala' FOREIGN KEY (idSala) REFERENCES Sala(idSala) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT 'fk_idpelicula' FOREIGN KEY (idPelicula) REFERENCES Pelicula(idPelicula) ON DELETE CASCADE ON UPDATE CASCADE
        ); """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Butaca (
        idButaca INTEGER PRIMARY KEY AUTOINCREMENT,
        idSala INTEGER NOT NULL,
        fila TEXT NOT NULL,
        numero INTEGER NOT NULL,
        disponibilidad INTEGER DEFAULT 0,
        CONSTRAINT 'fk_idsala2' FOREIGN KEY (idSala) REFERENCES Sala(idSala) ON DELETE CASCADE ON UPDATE CASCADE
        ); """)

    cursor.execute("""
        DROP TABLE IF EXISTS Butaca;
    """)

    cursor.execute("""
        CREATE TABLE Butaca (
        idButaca INTEGER PRIMARY KEY AUTOINCREMENT,
        idSala INTEGER NOT NULL,
        fila TEXT NOT NULL,
        numero INTEGER NOT NULL,
        disponibilidad INTEGER DEFAULT 0,
        CONSTRAINT 'fk_idsala2' FOREIGN KEY (idSala) REFERENCES Sala(idSala) ON DELETE CASCADE ON UPDATE CASCADE
    ); """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cliente (
        idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        dni INTEGER NOT NULL,
        email TEXT UNIQUE
        ); """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipoEntrada (
        idTipoEntrada INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        descuento REAL NOT NULL
        ); """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Entrada (
        idEntrada INTEGER PRIMARY KEY AUTOINCREMENT,
        idFuncion INTEGER NOT NULL,
        idButaca INTEGER NOT NULL,
        idCliente INTEGER NOT NULL,
        idTipoEntrada INTEGER NOT NULL,
        precioFinal REAL NOT NULL,
        CONSTRAINT 'fk_idfuncion' FOREIGN KEY (idFuncion) REFERENCES Funcion(idFuncion) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT 'fk_idbutaca' FOREIGN KEY (idButaca) REFERENCES Butaca(idButaca) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT 'fk_idcliente' FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT 'fk_idtipoentrada' FOREIGN KEY (idTipoEntrada) REFERENCES tipoEntrada(idTipoEntrada) ON DELETE CASCADE ON UPDATE CASCADE
        ); """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Venta (
        idVenta INTEGER PRIMARY KEY AUTOINCREMENT,
        num_cliente INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        total REAL NOT NULL,
        CONSTRAINT fk_cliente FOREIGN KEY (num_cliente) REFERENCES Cliente(num_cliente)
    ); """)


    conexion.commit()
    conexion.close()