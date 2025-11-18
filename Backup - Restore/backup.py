import sqlite3
import os
import csv

# Ruta base del proyecto (igual que usás vos)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

# Carpeta donde se guardan los backups
BACKUP_DIR = os.path.join(BASE_DIR, "Backups")
os.makedirs(BACKUP_DIR, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def export_table_to_csv(table_name):
    """Exporta una tabla a un archivo CSV."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # nombres de columnas
    column_names = [description[0] for description in cursor.description]

    csv_path = os.path.join(BACKUP_DIR, f"{table_name}_backup.csv")

    with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerows(rows)

    conn.close()
    print(f"[OK] Backup generado: {csv_path}")


def hacer_backup_de_todo():
    """
    Exporta TODAS las tablas de la base.
    Si querés agregar más, las agregás acá.
    """

    tablas = [
        "Pelicula",
        "Sala",
        "Butaca",
        "Funcion",
        "Cliente",
        "Entrada",
        "TipoEntrada",
        "Venta",
        "ButacaFuncion",
    ]

    for tabla in tablas:
        try:
            export_table_to_csv(tabla)
        except Exception as e:
            print(f"[ERROR] No se pudo exportar {tabla}: {e}")


if __name__ == "__main__":
    hacer_backup_de_todo()
