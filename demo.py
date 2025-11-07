# demo.py
import matplotlib.pyplot as plt
from quadtree import Quadtree
from rectangulo import Rectangulo

# Crear área inicial
ancho_total = 200
qt = Quadtree(Rectangulo(0, 0, ancho_total, ancho_total), capacidad=4)

# Crear figura sin barra de herramientas
plt.rcParams['toolbar'] = 'none'  # elimina los botones inferiores
fig, ax = plt.subplots(figsize=(8, 8))
fig.canvas.manager.set_window_title("Quadtree Interactivo")

ax.set_xlim(-ancho_total/2, ancho_total/2)
ax.set_ylim(-ancho_total/2, ancho_total/2)
ax.set_title("Haz clic para insertar puntos", fontsize=14)
ax.set_aspect('equal', adjustable='box')

# Lista de puntos añadidos
puntos = []

# Función para redibujar el árbol
def dibujar():
    ax.clear()
    ax.set_xlim(-ancho_total/2, ancho_total/2)
    ax.set_ylim(-ancho_total/2, ancho_total/2)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Haz clic para insertar puntos", fontsize=14)
    qt.dibujar(ax)
    if puntos:
        xs, ys = zip(*puntos)
        ax.scatter(xs, ys, color='red', s=15)
    fig.canvas.draw_idle()

# Evento de clic del mouse
def onclick(event):
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        punto = (x, y)
        puntos.append(punto)
        qt.insertar(punto)
        dibujar()

# Conectar evento
fig.canvas.mpl_connect('button_press_event', onclick)

# Dibujar inicial
dibujar()
plt.show()

