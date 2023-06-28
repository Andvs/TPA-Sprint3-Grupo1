from dataclasses import dataclass

@dataclass
class Reserva:
    nombre: str
    tipo_reserva: str
    opcion_reserva: str
    

    def __str__(self):
        return f'La persona es {self.nombre}(rut:{self.rut}) fecha_nacimiento: {self.fecha_nacimiento}'
