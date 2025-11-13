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
        if Pelicula.buscar_por_nombre(peli.titulo):
            print(f"Película ya existente: {peli.titulo}")
            continue
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

    salas_existentes = Sala.obtener_todas()
    nombres_existentes = [s.nombre for s in salas_existentes]

    for salita in salas:
        if salita.nombre in nombres_existentes:
            print(f"Sala ya existente: {salita.nombre} ({salita.tipo})")
            continue

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
    funciones_omitidas = 0

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

                conexion = Funcion._get_connection()
                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT idFuncion 
                    FROM Funcion
                    WHERE idPelicula=? AND idSala=? AND fechaHora=?
                """, (pelicula_obj.id_pelicula, sala_obj.idSala, fecha_hora))
                existe = cursor.fetchone()
                conexion.close()

                if existe:
                    print(f"Función ya existente: {pelicula_obj.titulo} | {formato} | {idioma} | {fecha_hora} | Sala {sala_obj.nombre}")
                    funciones_omitidas += 1
                else:
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

    tipos_existentes = TipoEntrada.listar_todos()
    descripciones_existentes = [t[1] for t in tipos_existentes]

    for tipo in tipos:
        if tipo.descripcion in descripciones_existentes:
            print(f"Tipo de entrada ya existente: {tipo.descripcion}")
            continue

        tipo.guardar_tipoEntrada()
        print(f"Tipo de entrada cargado: {tipo.descripcion} (Descuento {tipo.descuento * 100:.0f}%)")

if __name__ == "__main__":
    cargar_peliculas()
    cargar_salas()
    cargar_funciones()
    cargar_tipo_entradas()
    print("\n Base de datos del cine cargada correctamente.")