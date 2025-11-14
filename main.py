import os
import sys

def resource_path(relative_path):
    """Permite acceder a archivos tanto en modo desarrollo como en EXE."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from Clases.Pelicula import Pelicula
from Clases.Sala import Sala
from Clases.Funcion import Funcion
from Clases.Cliente import Cliente
from Clases.Butaca import Butaca
from Clases.TipoEntrada import TipoEntrada
from Clases.Entrada import Entrada
from Clases.Venta import Venta
from Clases.ButacaFuncion import ButacaFuncion

from SalaDeCine_DB import crear_base
from CargarDatos import cargar_datos_iniciales

DB_PATH = resource_path("SalaDeCine_DB.db")

if not os.path.exists(DB_PATH):
    print("Base de datos no encontrada. Creando base...")
    crear_base()  # Crea la DB desde cero
    print("Cargando datos iniciales...")
    cargar_datos_iniciales()  # Inserta datos
    print("Base creada correctamente.\n")

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
                # Paso 1: Mostrar películas
                peliculas = Pelicula.obtener_todas()
                if not peliculas:
                    print("No hay peliculas registradas.")
                    continue
                
                print("\n" + "=" * 50)
                print("=== PELICULAS DISPONIBLES ===")
                print("=" * 50 + "\n")
                for i, peli in enumerate(peliculas, start=1):
                    print(f"{i}. {peli.titulo} (Genero: {peli.genero}, Clasificacion: {peli.clasificacion}, Duración: {peli.duracion} minutos.)")

                try:
                    opcion_peli = int(input("Seleccione el número de película: ")) - 1
                    pelicula_seleccionada = peliculas[opcion_peli]
                except (ValueError, IndexError):
                    print("Opción inválida. Intente nuevamente.")

                # Paso 2: Mostrar funciones de la película
                funciones = Funcion.buscar_por_pelicula(pelicula_seleccionada.id_pelicula)
                if not funciones:
                    print("No hay funciones para esta película")
                    input("Presione ENTER para volver al menú")
                    return
                
                print("\n" + "=" * 80)
                print(f"=== FUNCIONES DISPONIBLES PARA {pelicula_seleccionada.titulo.upper()}===")
                print("=" * 80 + "\n")
                for i, func in enumerate(funciones, start=1):
                    print(f"{i}. Fecha/Hora: {func[2]}, Sala: {func[4]}, Idioma: {func[3]}, Formato: {func[5]}, Precio Base: ${func[6]}")
                
                try:
                    opcion_func = int(input("Seleccione el número de función: ")) - 1
                    funcion_seleccionada = funciones[opcion_func]
                except (ValueError, IndexError):
                    print("⚠ Opción inválida. Intente nuevamente.")
                    continue

                if isinstance(funcion_seleccionada, tuple):
                    id_funcion = funcion_seleccionada[0]
                    titulo_pelicula = funcion_seleccionada[1]
                    fecha_hora = funcion_seleccionada[2]
                    idioma = funcion_seleccionada[3]
                    nombre_sala = funcion_seleccionada[4]
                    formato = funcion_seleccionada[5]
                    precio_base = float(funcion_seleccionada[6]) if funcion_seleccionada[6] is not None else 0.0
                    id_sala = funcion_seleccionada[7]

                    pelicula_temp = Pelicula(id_pelicula=None, titulo=titulo_pelicula, genero=None, duracion=None)
                    sala_temp = Sala(idSala=id_sala, nombre=nombre_sala, capacidad=None)

                    idiomas_validos = ["Español", "Ingles(Subtitulada)"]
                    if idioma not in idiomas_validos:
                        idioma = "Español"
                
                    funcion_obj = Funcion(
                        pelicula_obj=pelicula_temp,
                        sala_obj=sala_temp,
                        id_funcion=id_funcion,
                        fecha_hora=fecha_hora,
                        idioma=idioma,
                        formato=formato,
                        precio_final=precio_base
                    )
                else:
                    funcion_obj = funcion_seleccionada
                    id_funcion = funcion_obj.id_funcion

                # Paso 2.5: Mostrar estado de butacas (según entradas para la función)
                print("\n" + "=" * 50)
                print("=== ESTADO DE BUTACAS ===")
                print("=" * 50 + "\n")
                id_funcion = funcion_seleccionada[0]
                sala = Sala.buscar_por_id(funcion_seleccionada[7])
                butacas = Butaca.obtener_por_sala(sala.idSala)
                try:
                    entradas_ocupadas = Entrada.obtener_por_funcion(id_funcion)
                    ids_butacas_ocupadas = [e[2] for e in entradas_ocupadas] 
                except Exception:
                    ids_butacas_ocupadas = []
                for b in butacas:
                    estado = "Ocupada" if b.id_butaca in ids_butacas_ocupadas else "Libre"
                    print(f"Butaca {b.fila}{b.numero} → {estado}")

                # Paso 3: Registrar cliente si no existe
                print("\n" + "=" * 70)
                print("=== REGISTRO O VERIFICACION DE CLIENTES ===")
                print("=" * 70 + "\n")
                dni_cliente = input("Ingrese DNI del cliente: ")
                if not dni_cliente.isdigit() or len(dni_cliente) < 8:
                    print("⚠ DNI inválido.")
                    continue

                cliente = Cliente.buscar_por_dni(dni_cliente)
                if not cliente:
                    print("Cliente no registrado, por favor ingrese sus datos. ")
                    cliente = Cliente(None, "", "")
                    cliente.guardar_clientes()

                # Paso 4: Crear venta vacía
                venta = Venta(cliente, [])
                continuar = True
                while continuar:
                    print("\n" + "=" * 50)
                    print("=== TIPOS DE ENTRADA DISPONIBLES ===")
                    print("=" * 50 + "\n")
                    tipos = TipoEntrada().listar()
                    for i, t in enumerate(tipos, start=1):
                        print(f"{i}. {t[1]} (Descuento: {t[2]*100:.0f}%)")

                    try:
                        opcion_tipo = int(input("Seleccione tipo de entrada: ")) - 1
                        if opcion_tipo < 0 or opcion_tipo >= len(tipos):
                            print("Selección inválida de tipo de entrada.") 
                            continue

                        tipo_tuple = tipos[opcion_tipo]
                        tipo_obj = TipoEntrada(
                            id_tipo=tipo_tuple[0],
                            descripcion=tipo_tuple[1],
                            descuento=tipo_tuple[2]
                        )
                    except (ValueError, IndexError):
                        print("Selección inválida de tipo de entrada. Intente nuevamente.")
                        
                    try:
                        cantidad = int(input("¿Cuántas entradas desea comprar de este tipo?: "))
                        if cantidad <= 0:
                            raise ValueError
                    except ValueError:
                        print("⚠ Cantidad inválida.")

                    butacas_libres = [b for b in butacas if not b.ocupada]
                    if len(butacas_libres) < cantidad:
                        print("No hay más butacas disponibles.")
                        break

                    for i in range(cantidad):
                        print("\n" + "=" * 50)
                        print("=== BUTACAS DISPONIBLES ===")
                        print("=" * 50 + "\n")
                        for b in butacas_libres:
                            print(f"- {b.fila}{b.numero}")

                        nombre_butaca = input("Seleccione el nombre de la butaca (ej. H7): ").strip().upper()
                        b = next((but for but in butacas_libres if (but.fila + str(but.numero)).upper() == nombre_butaca), None)
                        if b is None:
                            print("⚠ Butaca no válida o ya ocupada.")
                            continue

                        b.ocupar()
                        butacas_libres.remove(b)

                        entrada = Entrada(cliente, funcion_obj, b, tipo_obj)
                        entrada.calcular_total()
                        entrada.guardar_entrada()
                        venta.agregar_entrada(entrada)
                        entrada.generar_ticket()

                    seguir = input("¿Desea agregar otro tipo de entrada? (s/n): ").strip().lower()
                    if seguir != "s":
                        continuar = False
                    
                    # Paso 5: Finalizar venta: calcular total, guardar y generar ticket de venta
                    venta.calcular_total()
                    id_venta = venta.guardar_venta()
                    venta.generar_ticket_venta()

                    print("\n" + "=" * 40)
                    print(f"Total a pagar: ${venta.total:.2f}" if hasattr(venta, "total") else "Total calculado.")
                    print("Compra exitosa. Tickets generados correctamente.\n")

            elif opcion == "4":
                try:
                    while True:
                        print("\n=== REGISTRAR CLIENTE ===")
                        dni = input("Ingrese el DNI del cliente: ")
                        if dni.isdigit() and len(dni) >= 8:
                            break
                        print("⚠ DNI inválido.")

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
                except Exception as e:
                    print(f"Error al registrar cliente: {e}")

            elif opcion == "5":
                try:
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
                except Exception as e:
                    print(f"Error al listar tipos de entrada: {e}")

            elif opcion == "6":
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            
            else:
                print("Opción inválida. Intente nuevamente.")

        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()