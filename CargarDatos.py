from Clases.Pelicula import Pelicula
from Clases.Sala import Sala
from Clases.Funcion import Funcion
from Clases.Butaca import Butaca
from Clases.TipoEntrada import TipoEntrada
from Clases.Cliente import Cliente

def cargar_peliculas():
    peliculas = [
        Pelicula(None, "Super Mario Galaxy: La Pelicula", 92, "Animada", "ATP"),
        Pelicula(None, "Avengers: Doomsday", 150, "Acción", "+13"),
        Pelicula(None, "Toy Story 5", 130, "Animada", "ATP"), 
        Pelicula(None, "Scary Movie 6", 120, "Comedia", "+16"),
        Pelicula(None, "Spider-Man: Brand New Day", 140, "Acción", "+13"),
        Pelicula(None, "Resident Evil", 125, "Suspenso", "+18"),
        Pelicula(None, "Scream 7", 132, "Terror", "+18"),
        Pelicula(None, "Nada es lo que parece 3", 112, "Thriller", "+13"),
        Pelicula(None, "Anaconda", 90, "Comedia", "ATP"),
    ]

    for peli in peliculas:
        peli.guardar_pelicula()
        print(f"Pelicula cargada: {peli.titulo}")

def cargar_salas():
    salas = [
        Sala(None, "Sala 1", "2D", 100, 12500),
        Sala(None, "Sala 2", "2D", 120, 12500),
        Sala(None, "Sala 3", "3D", 90, 15700),
        Sala(None, "Sala 4", "2D", 110, 12500),
        Sala(None, "Sala 5", "3D", 120, 15700),
    ]

    for salita in salas:
        salita.guardar_sala()
        print(f"Sala cargada: {salita.nombre} ({salita.tipo})")

        salita.generar_butacas()
        print(f"  → {len(salita.butacas)} butacas generadas para {salita.nombre}")

def cargar_funciones():
    dias = ["2025-11-18", "2025-11-19", "2025-11-20", "2025-11-21"]
    horarios = ["18:00", "20:15", "22:30"]
    idiomas = ["Español", "Ingles(Subtitulada)"]
    formatos = ["2D", "3D"]

    funciones = []
    precio_por_formato = {"2D": 12500, "3D": 15700}

    id_sala = 1
    for id_pelicula in range(1, 10):  # 9 películas
        for dia in dias:
            for hora in horarios:
                dias = ["2025-11-18", "2025-11-19", "2025-11-20", "2025-11-21"]
                horarios = ["18:00", "20:15", "22:30"]
                idioma = idiomas[(id_pelicula + len(hora)) % 2]  # alterna idioma
                formato = formatos[(id_pelicula + len(dia)) % 2]  # alterna formato
                fecha_hora = f"{dia} {hora}"
                precio = precio_por_formato[formato]

                pelicula_obj = Pelicula.buscar_por_id(id_pelicula)
                sala_obj = Sala.buscar_por_id(id_sala)

                if not pelicula_obj or not sala_obj:
                    print(f"Error: No se encontró Pelicula {id_pelicula} o Sala {id_sala}")
                    continue

                funcion = Funcion(
                    pelicula_obj,
                    sala_obj,
                    fecha_hora=fecha_hora,
                    idioma=idioma,
                    formato=formato,
                    precio_final=precio

                )
                funciones.append(funcion)

                id_sala += 1
                if id_sala > 5:
                    id_sala = 1

    for func in funciones:
        func.guardar_funcion()
        print(f"Función cargada: Película {func.pelicula.id_pelicula} | {func.formato} | {func.idioma} | {func.fecha_hora} | Sala {func.sala.idSala}")

    print(f"\n Se cargaron {len(funciones)} funciones correctamente.")

def cargar_tipo_entradas():
    tipos = [
        TipoEntrada(None, "General", 0.00),
        TipoEntrada(None, "Menores 12 años", 0.20),
        TipoEntrada(None, "Jubilados", 0.30),
    ]

    for tipo in tipos:
        tipo.guardar_tipoEntrada()
        print(f"Tipo de entrada cargado: {tipo.descripcion} (Descuento {tipo.descuento * 100:.0f}%)")

def cargar_butacas():
    salas = Sala.obtener_todas()
    for sala in salas:
        sala.generar_butacas()
        conexion = Butaca._get_connection()
        cursor = conexion.cursor()
        for butaca in sala.butacas:
            cursor.execute("""
                INSERT INTO Butaca (idSala, fila, numero, disponibilidad)
                VALUES (?, ?, ?, 0)
            """, (butaca.id_sala, butaca.fila, butaca.numero))
        conexion.commit()
        conexion.close()
        print(f"Butacas generadas para {sala.nombre}")

if __name__ == "__main__":
    cargar_peliculas()
    cargar_salas()
    cargar_funciones()
    cargar_tipo_entradas()
    cargar_butacas()
    print("\n Base de datos del cine cargada correctamente.")