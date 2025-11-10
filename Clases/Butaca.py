class Butaca:
    def __init__(self, id_butaca=None, fila="", numero=0, id_sala=None, reservada=False):
       self.id_butaca = id_butaca
       self.fila = fila
       self.numero = numero 
       self.id_sala = id_sala
       self.reservada = reservada
    
    def reservar(self):
        if not self.reservada:
            self.reservada = True
            return True
        return False

    def liberar(self):
        if self.reservada:
            self.reservada = False
            return True
        return False

    def __str__(self):
        estado = "Reservada" if self.reservada else "Libre"
        return f"butaca {self.fila}{self.numero}: ({estado})"

   