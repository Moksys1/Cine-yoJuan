from .Butaca import Butaca
from .Funcion import Funcion


class ButacaFuncion:
    def __init__(self, id_butaca_funcion=None, funcion=None, butaca=None, estado="Libre"):
        self.id_butaca_funcion = id_butaca_funcion
        self.funcion = funcion
        self.butaca = butaca
        self.estado = estado

    def ocupar(self):
        if self.estado == "Libre":
            self.estado = "Ocupada"
            return True
        return False
    
    def liberar(self):
        if self.estado == "Ocupada":
            self.estado = "Libre"
            return True
        return False
    
    def mostrar_info(self):
        print(f"Butaca {self.butaca.fila}{self.butaca.numero} | "
              f"Función #{self.funcion.id_funcion} ({self.funcion.pelicula.titulo}) | "
              f"Estado: {self.estado}")