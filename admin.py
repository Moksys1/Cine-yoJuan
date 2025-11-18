import os
import sqlite3
from config import DB_PATH
from SalaDeCine_DB import crear_base
from CargarDatos import cargar_datos_iniciales
from reportes import Reportes

# --- HERRAMIENTAS DE BASE DE DATOS ---
def get_connection():
    return sqlite3.connect(DB_PATH)

def ejecutar_sql(sql, parametros=()):
    """Ejecuta una instrucción que modifica la BD (INSERT, UPDATE, DELETE)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql, parametros)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error de Base de Datos: {e}")
        return False

def obtener_datos(sql, parametros=()):
    """Ejecuta una consulta SELECT"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, parametros)
    datos = cursor.fetchall()
    conn.close()
    return datos

# --- GESTIÓN DE PELÍCULAS ---
def gestionar_peliculas():
    while True:
        print("\n--- GESTIÓN DE PELÍCULAS ---")
        print("1. Listar Películas")
        print("2. Agregar Película")
        print("3. Modificar Precio/Duración")
        print("4. Eliminar Película")
        print("5. Volver")
        op = input(">> ")

        if op == "1":
            pelis = obtener_datos("SELECT * FROM Pelicula")
            print(f"\n{'ID':<4} {'TÍTULO':<30} {'DURACIÓN':<10} {'GÉNERO':<15}")
            print("-" * 65)
            for p in pelis:
                print(f"{p[0]:<4} {p[1]:<30} {p[2]:<10} {p[3]:<15}")
        
        elif op == "2":
            titulo = input("Título: ")
            duracion = input("Duración (min): ")
            genero = input("Género: ")
            clasif = input("Clasificación (ATP, +13, etc): ")
            sql = "INSERT INTO Pelicula (titulo, duracion, genero, clasificacion) VALUES (?, ?, ?, ?)"
            if ejecutar_sql(sql, (titulo, duracion, genero, clasif)):
                print("✔ Película agregada.")

        elif op == "3":
            id_peli = input("ID de la película a modificar: ")
            nueva_dur = input("Nueva duración (Enter para no cambiar): ")
            
            if nueva_dur:
                ejecutar_sql("UPDATE Pelicula SET duracion = ? WHERE idPelicula = ?", (nueva_dur, id_peli))
                print("✔ Duración actualizada.")
            else:
                print("No se hicieron cambios.")

        elif op == "4":
            id_peli = input("ID de la película a eliminar: ")
            # Advertencia: Esto fallará si la película tiene funciones o entradas vendidas (Foreign Keys)
            if ejecutar_sql("DELETE FROM Pelicula WHERE idPelicula = ?", (id_peli,)):
                print("✔ Película eliminada.")
            else:
                print("⚠ No se puede eliminar si tiene funciones o entradas asociadas.")

        elif op == "5":
            break

# --- GESTIÓN DE SALAS ---
def gestionar_salas():
    while True:
        print("\n--- GESTIÓN DE SALAS ---")
        print("1. Listar Salas")
        print("2. Agregar Sala")
        print("3. Cambiar Precio Base")
        print("4. Volver")
        op = input(">> ")

        if op == "1":
            salas = obtener_datos("SELECT * FROM Sala")
            print(f"\n{'ID':<4} {'NOMBRE':<10} {'TIPO':<5} {'CAPACIDAD':<10} {'PRECIO':<10}")
            print("-" * 50)
            for s in salas:
                print(f"{s[0]:<4} {s[1]:<10} {s[2]:<5} {s[3]:<10} ${s[4]}")

        elif op == "2":
            nombre = input("Nombre (Ej: Sala 5): ")
            tipo = input("Tipo (2D/3D): ")
            capacidad = input("Capacidad: ")
            precio = input("Precio Base: ")
            sql = "INSERT INTO Sala (nombre, tipoSala, capacidad, precioBase) VALUES (?, ?, ?, ?)"
            if ejecutar_sql(sql, (nombre, tipo, capacidad, precio)):
                print("✔ Sala agregada.")

        elif op == "3":
            id_sala = input("ID de la Sala: ")
            nuevo_precio = input("Nuevo Precio Base: ")
            if ejecutar_sql("UPDATE Sala SET precioBase = ? WHERE idSala = ?", (nuevo_precio, id_sala)):
                print("✔ Precio actualizado.")

        elif op == "4":
            break

# --- GESTIÓN DE FUNCIONES ---
def gestionar_funciones():
    while True:
        print("\n--- GESTIÓN DE FUNCIONES ---")
        print("1. Ver cartelera completa")
        print("2. Agregar Función Manualmente")
        print("3. Eliminar Función")
        print("4. Volver")
        op = input(">> ")

        if op == "1":
            sql = """
            SELECT f.idFuncion, f.fechaHora, p.titulo, s.nombre 
            FROM Funcion f
            JOIN Pelicula p ON f.idPelicula = p.idPelicula
            JOIN Sala s ON f.idSala = s.idSala
            ORDER BY f.fechaHora
            """
            func = obtener_datos(sql)
            print(f"\n{'ID':<4} {'FECHA/HORA':<20} {'SALA':<10} {'PELÍCULA'}")
            print("-" * 60)
            for f in func:
                print(f"{f[0]:<4} {f[1]:<20} {f[3]:<10} {f[2]}")

        elif op == "2":
            print("Para agregar función necesitas los IDs.")
            fecha = input("Fecha y Hora (YYYY-MM-DD HH:MM): ")
            idioma = input("Idioma: ")
            id_sala = input("ID Sala: ")
            id_peli = input("ID Película: ")
            
            # Verificamos si la sala o peli existen antes de insertar
            if not obtener_datos("SELECT * FROM Sala WHERE idSala=?", (id_sala,)):
                print("❌ Error: Esa sala no existe.")
                continue
                
            sql = "INSERT INTO Funcion (fechaHora, idioma, idSala, idPelicula) VALUES (?, ?, ?, ?)"
            if ejecutar_sql(sql, (fecha, idioma, id_sala, id_peli)):
                print("✔ Función agregada a la cartelera.")

        elif op == "3":
            id_func = input("ID de la función a eliminar: ")
            if ejecutar_sql("DELETE FROM Funcion WHERE idFuncion = ?", (id_func,)):
                print("✔ Función eliminada.")
            else:
                print("⚠ No se puede eliminar si ya tiene entradas vendidas.")

        elif op == "4":
            break

# --- MENÚ PRINCIPAL DE ADMINISTRADOR ---
def mostrar_menu_admin():
    while True:
        print("\n" + "="*40)
        print("      PANEL DE ADMINISTRACIÓN - CINE")
        print("="*40)
        print("   --- REPORTES ---")
        print("1. Ventas por Película (Gráfico)")
        print("2. Mejores Clientes (Gráfico)")
        print("3. Ocupación de Cartelera (Gráfico)")
        print("\n   --- GESTIÓN (ABM) ---")
        print("4. Gestionar PELÍCULAS")
        print("5. Gestionar SALAS")
        print("6. Gestionar FUNCIONES")
        print("\n   --- SISTEMA ---")
        print("7. ⚠ REINICIAR BASE DE DATOS (Factory Reset)")
        print("0. SALIR")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            Reportes.ventas_por_pelicula()
            input("Enter para continuar...")
        elif opcion == "2":
            Reportes.clientes_top()
            input("Enter para continuar...")
        elif opcion == "3":
            Reportes.peliculas_mas_funciones()
            input("Enter para continuar...")
            
        elif opcion == "4":
            gestionar_peliculas()
        elif opcion == "5":
            gestionar_salas()
        elif opcion == "6":
            gestionar_funciones()

        elif opcion == "7":
            confirmacion = input("\n⚠ ¿ESTÁ SEGURO? Se perderán todas las ventas y clientes nuevos (s/n): ")
            if confirmacion.lower() == 's':
                print("Eliminando base de datos actual...")
                if os.path.exists(DB_PATH):
                    try:
                        os.remove(DB_PATH)
                    except Exception as e:
                        print(f"Error borrando archivo: {e}")
                
                print("Recreando estructura...")
                crear_base(DB_PATH)
                print("Cargando datos por defecto...")
                cargar_datos_iniciales()
                print("✔ Base de datos restaurada a estado de fábrica.")
            else:
                print("Operación cancelada.")
            input("\nPresione ENTER para continuar...")

        elif opcion == "0":
            print("Saliendo del panel de administración...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    # Verificamos que la base exista antes de intentar administrarla
    if not os.path.exists(DB_PATH):
        print("⚠ No se encontró la base de datos. Creándola primero...")
        crear_base(DB_PATH)
        cargar_datos_iniciales()
        
    mostrar_menu_admin()