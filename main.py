from Clases.Pelicula import Pelicula
from Clases.Sala import Sala
from Clases.Funcion import Funcion
from Clases.Cliente import Cliente
from Clases.Butaca import Butaca
from Clases.TipoEntrada import TipoEntrada
from Clases.Entrada import Entrada
from Clases.Venta import Venta

def mostrar_menu():
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Mostrar películas disponibles")
    print("2. Mostrar salas disponibles")
    print("3. Comprar entrada")
    print("4. Registrar cliente")
    print("5. Listar tipos de entradas")
    print("6. Salir")
    opcion = input("Seleccione una opción (1-6): ")
    return opcion

def main():
    while True:
        try:
            opcion = mostrar_menu()
            
            if opcion == "1":
                print("\n=== PELÍCULAS DISPONIBLES ===")
                peliculas = Pelicula.obtener_todas()
                if not peliculas:
                    print("No hay peliculas registradas.")
                else:
                    for peli in peliculas:
                        peli.mostrar_info()
                
            elif opcion == "2":
                print("\n=== SALAS DISPONIBLES ===")
                salas = Sala.obtener_todas()
                if not salas:
                    print("No hay salas registradas.")
                else:
                    for sala in salas:
                        sala.mostrar_info()
                
            elif opcion == "3":
                print("\n=== FUNCIONES DISPONIBLES ===")

                # Paso 1: Mostrar películas
                peliculas = Pelicula.obtener_todas()
                if not peliculas:
                    print("No hay peliculas registradas.")
                    continue
                
                print("\nPelículas disponibles:")
                for i, peli in enumerate(peliculas, start=1):
                    print(f"{i}. {peli.titulo} (Genero: {peli.genero}, Clasificacion: {peli.clasificacion}, Duración: {peli.duracion} minutos.)")

                try:
                    opcion_peli = int(input("Seleccione el número de película: ")) - 1
                    pelicula_seleccionada = peliculas[opcion_peli]

                except (ValueError, IndexError):
                    print("Opción inválida. Intente nuevamente.")
                    continue

                # Paso 2: Mostrar funciones de la película
                funciones = Funcion.buscar_por_pelicula(pelicula_seleccionada.id_pelicula)
                if not funciones:
                    print("No hay funciones para esta película")
                    continue

                print("\nFunciones disponibles:")
                for i, func in enumerate(funciones, start=1):
                    print(f"{i}. Fecha/Hora: {func[2]}, Sala: {func[4]}, Idioma: {func[3]}, Formato: {func[5]}, Precio Base: ${func[6]}")

                try:
                    opcion_func = int(input("Seleccione el número de función: ")) - 1
                    funcion_seleccionada = funciones[opcion_func]

                except (ValueError, IndexError):
                    print("⚠ Opción inválida. Intente nuevamente.")
                    continue

                # Paso 3: Seleccionar tipo de entrada
                tipo_entrada_obj = TipoEntrada()
                tipos = tipo_entrada_obj.listar()

                for i, t in enumerate(tipos, start=1):
                    print(f"{i}. {t[1]} (Descuento: {t[2]*100:.0f}%)")

                try:
                    opcion_tipo = int(input("Seleccione tipo de entrada: ")) - 1
                    tipo_elegido = tipos[opcion_tipo]

                except (ValueError, IndexError):
                    print("⚠ Opción inválida.")
                    continue

                # Paso 4: Cantidad de entradas
                try:
                    cantidad = int(input("Cantidad de entradas: "))
                    if cantidad <= 0:
                        raise ValueError
                    
                except ValueError:
                    print("⚠ Cantidad inválida.")
                    continue

                # Paso 5: Registrar cliente si no existe
                dni_cliente = input("Ingrese DNI del cliente: ")
                if not dni_cliente.isdigit() or len(dni_cliente) < 8:
                    print("⚠ DNI inválido.")
                    continue

                cliente = Cliente.buscar_por_dni(dni_cliente)
                if not cliente:
                    print("Cliente no registrado, por favor ingrese sus datos. ")
                    cliente = Cliente(None, "", "")
                    cliente.guardar_clientes()

                # Paso 6: Elegir butacas disponibles
                sala = Sala.buscar_por_id(funcion_seleccionada[7])
                butacas = Butaca.obtener_por_sala(sala.idSala)
                butacas_libres = [b for b in butacas if not b.ocupada]


                if len(butacas_libres) < cantidad:
                    print("No hay suficientes butacas disponibles.")
                    continue

                print("\nButacas disponibles:")
                for b in butacas_libres:
                    print(f"- {b.fila}{b.numero} ({'Libre' if not b.ocupada else 'Ocupada'})")

                butacas_elegidas = []
                
                for i in range(cantidad):
                    nombre_butaca = input("Seleccione el nombre de la butaca (ej. H7): ").strip().upper()
                    b = next((but for but in butacas_libres if (but.fila + str(but.numero)).upper() == nombre_butaca), None)

                    if b is None:
                        print("⚠ Butaca no válida o ya ocupada.")
                        continue
                    b.ocupar()
                    butacas_elegidas.append(b)
                    print(f"✅ Butaca {b.fila}{b.numero} reservada correctamente.")

                # Paso 7: Crear entradas y calcular total

                if isinstance(funcion_seleccionada, tuple):
                    id_funcion = funcion_seleccionada[0]
                    titulo_pelicula = funcion_seleccionada[1]
                    fecha_hora = funcion_seleccionada[2]
                    idioma = funcion_seleccionada[3]
                    nombre_sala = funcion_seleccionada[4]
                    formato = funcion_seleccionada[5]
                    precio_base = funcion_seleccionada[6]
                    id_sala = funcion_seleccionada[7]

                    pelicula = Pelicula(id_pelicula=None, titulo=titulo_pelicula, genero=None, duracion=None)
                    sala = Sala(idSala=id_sala, nombre=nombre_sala, capacidad=None)

                    idiomas_validos = ["Español", "Ingles(Subtitulada)"]
                    if idioma not in idiomas_validos:
                        print(f"⚠ Idioma '{idioma}' inválido, se asignará 'Español' por defecto.")
                        idioma = "Español"

                    funcion_seleccionada = Funcion(
                        pelicula_obj=pelicula,
                        sala_obj=sala,
                        id_funcion=id_funcion,
                        fecha_hora=fecha_hora,
                        idioma=idioma,
                        formato=formato,
                        precio_final=precio_base
                    )

                if isinstance(tipo_elegido, tuple):
                    id_tipo, descripcion, descuento = tipo_elegido
                    tipo_elegido = TipoEntrada(id_tipo, descripcion, descuento)

                butacas_elegidas = [
                    Butaca(
                        id_butaca=b[0],
                        fila=b[1],
                        numero=b[2],
                        id_sala=b[3]
                    ) if isinstance(b, tuple) else b
                    for b in butacas_elegidas
                ]

                if cliente.id_cliente is None:
                    cliente.guardar_clientes()

                entradas = []
                total = 0

                for butaca in butacas_elegidas:
                    entrada = Entrada(
                        cliente=cliente,
                        funcion=funcion_seleccionada,
                        butaca=butaca,
                        tipoEntrada=tipo_elegido,
                        precio_final=funcion_seleccionada.precio_final 
                    )
                    total += entrada.calcular_total()
                    entrada.guardar_entrada()
                    entradas.append(entrada)

                # Paso 8: Generar tickets
                for entrada in entradas:
                    entrada.generar_ticket()

                print(f"\nTotal a pagar: ${total:.2f}")
                print("Compra exitosa. Tickets generados correctamente.\n")
                
            elif opcion == "4":
                print("\n=== REGISTRAR CLIENTE ===")
                dni = input("Ingrese el DNI del cliente: ")
                if not dni.isdigit():
                    print("⚠ DNI inválido.")
                    continue

                cliente = Cliente.buscar_por_dni(dni)

                if cliente:
                    print("\nCliente encontrado:")
                    cliente.mostrar_info()
                    actualizar = input("¿Desea actualizar sus datos? (s/n): ").lower()
                    if actualizar == "s":
                        cliente.guardar_clientes()
                else:
                    nuevo_cliente = Cliente(None, "", "")
                    nuevo_cliente.guardar_clientes()
                
            elif opcion == "5":
                print("\n=== LISTAR TIPOS DE ENTRADA ===")
                tipos = TipoEntrada.listar_todos()

                if tipos:
                    print(f"{'ID':<5} {'Descripción':<20} {'Descuento':<10}")
                    print("-" * 40)
                    for t in tipos:
                        id_tipo, descripcion, descuento = t
                        print(f"{id_tipo:<5} {descripcion:<20} {descuento*100:.0f}%")
                else:
                    print("No hay tipos de entrada registrados.")
                

            elif opcion == "6":
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            
            else:
                print("Opción inválida. Intente nuevamente.")

        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()