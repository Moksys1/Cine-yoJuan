class Butaca:
    def __init__(self, id_butaca=None, fila="", numero=0, id_sala=None, ocupada=False):
       self.id_butaca = id_butaca
       self.fila = fila
       self.numero = numero 
       self.id_sala = id_sala
       self.ocupada = ocupada
    
    def reservar(self):
        if not self.ocupada:
            self.ocupada = True
            return True
        return False

    def liberar(self):
        if self.ocupada:
            self.ocupada = False
            return True
        return False

    def __str__(self):
        estado = "Ocupada" if self.ocupada else "Libre"
        return f"butaca {self.fila}{self.numero}: ({estado})"

   