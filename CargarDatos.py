from Clases.Pelicula import Pelicula
from Clases.Sala import Sala

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
        salita.guardar()
        print(f"Sala cargada: {salita.nombre} ({salita.tipo})")