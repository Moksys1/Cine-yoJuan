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
    opcion = input("Seleccione una opción (1-5): ")
    return opcion

def main():
    while True:
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
            
            for i, peli in enumerate(peliculas, start=1):
                print(f"{i}. {peli.titulo} ({peli.genero}, {peli.clasificacion}, {peli.duracion})")

            opcion_peli = int(input("Seleccione el número de película: ")) - 1
            pelicula_seleccionada = peliculas[opcion_peli]

            # Paso 2: Mostrar funciones de la película
            funciones = Funcion.buscar_por_pelicula(pelicula_seleccionada.id_pelicula)
            if not funciones:
                print("No hay funciones para esta película")
                continue

            for i, func in enumerate(funciones, start=1):
                print(f"{i}. Fecha/Hora: {func.fecha_hora}, Sala: {func.id_sala}, Idioma: {func.idioma}, Formato: {func.formato}, Precio Base: ${func.precio_final}")

            opcion_func = int(input("Seleccione el número de función: ")) - 1
            funcion_seleccionada = funciones[opcion_func]
            
            # Paso 3: Seleccionar tipo de entrada
            tipos = TipoEntrada.listar()
            for i, t in enumerate(tipos, start=1):
                print(f"{i}. {t.descripcion} (Descuento: {t.descuento*100:.0f}%)")

            opcion_tipo = int(input("Seleccione tipo de entrada: ")) - 1
            tipo_elegido = tipos[opcion_tipo]

            # Paso 4: Cantidad de entradas
            cantidad = int(input("Cantidad de entradas: "))

            # Paso 5: Registrar cliente si no existe
            dni_cliente = input("Ingrese DNI del cliente: ")
            cliente = Cliente.buscar_por_dni(dni_cliente)
            if not cliente:
                print("Cliente no registrado, por favor ingrese sus datos. ")
                cliente = Cliente(None, "", "")
                cliente.guardar_clientes()

            # Paso 6: Elegir butacas disponibles
            sala = Sala.buscar_por_id(funcion_seleccionada.id_sala)
            sala.generar_butacas()
            butacas_libres = [b for b in sala.butacas if not b.ocupada]

            if len(butacas_libres) < cantidad:
                print("No hay suficientes butacas disponibles.")
                continue

            print("\nButacas disponibles:")
            for i, b in enumerate(butacas_libres, start=1):
                print(f"{i}. {b}")

            butacas_elegidas = []
            for but in range(cantidad):
                opcion_butaca = int(input("Seleccione número de butaca: ")) - 1
                b = butacas_libres[opcion_butaca]
                b.ocupar()
                butacas_elegidas.append(b)

            # Paso 7: Crear entradas y calcular total
            entradas = []
            total = 0
            for butaca in butacas_elegidas:
                entrada = Entrada(cliente, funcion_seleccionada, butaca, tipo_elegido)
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
            cliente = Cliente.buscar_por_dni(dni)

            if cliente:
                print("\nCliente encontrado:")
                cliente.mostrar_info()
                actualizar = input("¿Desea actualizar sus datos? (s/n): ").lower()
                if actualizar == "s":
                    cliente.guardar_clientes()
            else:
                print("\nCliente no encontrado. Registrando nuevo cliente:")
                nuevo_cliente = Cliente(None, "", "")
                nuevo_cliente.guardar_clientes()

            # Aquí luego llamaremos al método para crear un cliente
            
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

if __name__ == "__main__":
    main()