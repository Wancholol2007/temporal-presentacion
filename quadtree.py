# quadtree.py
from rectangulo import Rectangulo

class Quadtree:
    """Estructura básica de un Quadtree para dividir el espacio 2D."""

    def __init__(self, frontera: Rectangulo, capacidad=4, profundidad=0, max_profundidad=8):
        # Cada nodo cubre una región rectangular (frontera)
        self.frontera = frontera
        self.capacidad = capacidad
        self.puntos = []           # Lista de puntos almacenados en este nodo
        self.dividido = False      # Indica si ya se subdividió
        self.profundidad = profundidad
        self.max_profundidad = max_profundidad

    # Subdivisión: divide el nodo actual en 4 cuadrantes
    def subdividir(self):
        x, y = self.frontera.x, self.frontera.y
        w, h = self.frontera.ancho / 2, self.frontera.alto / 2

        # Crear los 4 hijos: NW, NE, SW, SE
        self.noroeste = Quadtree(Rectangulo(x - w/2, y - h/2, w, h),
                                 self.capacidad, self.profundidad + 1, self.max_profundidad)
        self.noreste = Quadtree(Rectangulo(x + w/2, y - h/2, w, h),
                                 self.capacidad, self.profundidad + 1, self.max_profundidad)
        self.suroeste = Quadtree(Rectangulo(x - w/2, y + h/2, w, h),
                                 self.capacidad, self.profundidad + 1, self.max_profundidad)
        self.sureste = Quadtree(Rectangulo(x + w/2, y + h/2, w, h),
                                 self.capacidad, self.profundidad + 1, self.max_profundidad)

        self.dividido = True

    # Inserción de un punto

    def insertar(self, punto):
        # Si el punto no está dentro de esta frontera, se ignora
        if not self.frontera.contiene(punto):
            return False

        # Si hay espacio, se agrega aquí
        if len(self.puntos) < self.capacidad or self.profundidad >= self.max_profundidad:
            self.puntos.append(punto)
            return True

        # Si no hay espacio y no se ha subdividido, se divide
        if not self.dividido:
            self.subdividir()

        # Intentar insertar recursivamente en los hijos
        return (self.noroeste.insertar(punto) or
                self.noreste.insertar(punto) or
                self.suroeste.insertar(punto) or
                self.sureste.insertar(punto))

    
    # Búsqueda de puntos dentro de un rango

    def buscar(self, rango: Rectangulo, encontrados=None):
        if encontrados is None:
            encontrados = []

        # Si el rango no se cruza con este nodo, no hay nada que buscar
        if not self.frontera.intersecta(rango):
            return encontrados

        # Revisar los puntos almacenados en este nodo
        for p in self.puntos:
            if rango.contiene(p):
                encontrados.append(p)

        # Buscar en los hijos si existen
        if self.dividido:
            self.noroeste.buscar(rango, encontrados)
            self.noreste.buscar(rango, encontrados)
            self.suroeste.buscar(rango, encontrados)
            self.sureste.buscar(rango, encontrados)

        return encontrados


    # Eliminación de un punto

    def eliminar(self, punto):
        # Si el punto no está dentro de la frontera, ignorar
        if not self.frontera.contiene(punto):
            return False

        # Si está en esta hoja, eliminarlo
        if punto in self.puntos:
            self.puntos.remove(punto)
            return True

        # Si hay subdivisión, buscar en los hijos
        if self.dividido:
            return (self.noroeste.eliminar(punto) or
                    self.noreste.eliminar(punto) or
                    self.suroeste.eliminar(punto) or
                    self.sureste.eliminar(punto))

        return False

    # Dibujo del Quadtree (usado en demo.py)

    def dibujar(self, ax):
        """Dibuja la frontera y sus subdivisiones recursivamente."""
        rect = self.frontera

        # Dibujar el borde del rectángulo
        ax.plot([rect.x - rect.ancho/2, rect.x + rect.ancho/2],
                [rect.y - rect.alto/2, rect.y - rect.alto/2], 'k-', linewidth=0.8)
        ax.plot([rect.x - rect.ancho/2, rect.x + rect.ancho/2],
                [rect.y + rect.alto/2, rect.y + rect.alto/2], 'k-', linewidth=0.8)
        ax.plot([rect.x - rect.ancho/2, rect.x - rect.ancho/2],
                [rect.y - rect.alto/2, rect.y + rect.alto/2], 'k-', linewidth=0.8)
        ax.plot([rect.x + rect.ancho/2, rect.x + rect.ancho/2],
                [rect.y - rect.alto/2, rect.y + rect.alto/2], 'k-', linewidth=0.8)

        # Dibujar recursivamente los hijos
        if self.dividido:
            self.noroeste.dibujar(ax)
            self.noreste.dibujar(ax)
            self.suroeste.dibujar(ax)
            self.sureste.dibujar(ax)
