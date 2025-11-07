from dataclasses import dataclass

@dataclass
class Rectangulo:
    """Representa una región rectangular en el plano 2D (centro, ancho, alto)."""
    x: float
    y: float
    ancho: float
    alto: float

    def contiene(self, punto):
        """Devuelve True si el punto está dentro del rectángulo."""
        px, py = punto
        return (self.x - self.ancho / 2 <= px <= self.x + self.ancho / 2 and
                self.y - self.alto / 2 <= py <= self.y + self.alto / 2)

    def intersecta(self, rango: 'Rectangulo') -> bool:
        """Devuelve True si este rectángulo se cruza con otro."""
        return not (rango.x - rango.ancho/2 > self.x + self.ancho/2 or
                    rango.x + rango.ancho/2 < self.x - self.ancho/2 or
                    rango.y - rango.alto/2 > self.y + self.alto/2 or
                    rango.y + rango.alto/2 < self.y - self.alto/2)
