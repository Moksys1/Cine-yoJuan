import sqlite3
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SalaDeCine_DB.db")

BACKUP_DIR = os.path.join(BASE_DIR, "Backups")


def get_connection():
    return sqlite3.connect(DB_PATH)


def import_csv_to_table(table_name):
    """Importa un CSV a una tabla (restore)."""
    conn = get_connection()
    cursor = conn.cursor()

    csv_path = os.path.join(BACKUP_DIR, f"{table_name}_backup.csv")

    if not os.path.exists(csv_path):
        print(f"[SKIP] No existe backup para {table_name}")
        return

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        columns = next(reader)  # header
        rows = list(reader)

    # vaciar tabla antes de restaurar
    cursor.execute(f"DELETE FROM {table_name}")

    # construir INSERT dinámico según cantidad de columnas
    placeholders = ",".join(["?"] * len(columns))
    insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

    cursor.executemany(insert_query, rows)

    conn.commit()
    conn.close()
    print(f"[OK] Restore hecho: {table_name}")


def restore_de_todo():
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
            import_csv_to_table(tabla)
        except Exception as e:
            print(f"[ERROR] No se pudo restaurar {tabla}: {e}")


if __name__ == "__main__":
    restore_de_todo()
