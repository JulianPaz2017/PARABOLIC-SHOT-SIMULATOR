from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt6.QtGui import QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import numpy as np

# Función auxiliar para ver si un string es un flotante
def is_float(str):
  try:
    float(str)
    return True
  except ValueError:
    return False

# Función que determina si un float es no negativo
def is_not_negative(x):
    return x >= 0

# Función que calcula la trayectoria de una partícula
def calculate_trajectory(r, v, tf, pasos):
    rx, ry, rz = r
    vx, vy, vz = v

    g = 9.81
    t = np.linspace(0, tf, pasos)

    xs = rx + vx * t
    ys = ry + vy * t
    zs = rz + vz * t - 0.5 * g * t**2

    mask = zs >= 0

    xs = xs[mask]
    ys = ys[mask]
    zs = zs[mask]

    return xs, ys, zs, (xs[-1], ys[-1], zs[-1])


# Definimos una clase para mantener todo más ordenado:
class TrajectorySimulator(QMainWindow):
  def __init__(self):
    super().__init__()
    
    # VENTANA
    # Configuración de la ventana
    self.setWindowTitle("Simulador tiro parabólico")     # Título             ventana
    self.setGeometry(0, 0, 1400, 575)                    # Tamaño y ubicación ventana
    self.setWindowIcon(QIcon("Icon.png"))                # Icono              ventana


    # BOTONES
    # Boton para comenzar a simular la trayectoria
    self.button = QPushButton("Simular trayectoria", self)     # Creación           botón
    self.button.setGeometry(950, 485, 120, 40)                 # Tamaño y ubicación botón
    self.button.clicked.connect(self.simulate_trajectory)      # Acción al tocar el boton


    # TEXTOS
    # Texto "Simulador tiro parabólico"
    self.sim = QLabel("SIMULADOR TIRO PARABÓLICO", self)            # Creación  del texto "Simulador tiro parabólico"
    self.sim.move(50, 50)                                           # Ubicación del texto "Simulador tiro parabólico"
    self.sim.resize(500, 50)                                        # Tamaño    del texto "Simulador tiro parabólico"
    self.sim.setFont(QFont("Times New Roman", 24))                  # Modificación de la fuente y el tamaño

    # Texto "Ingresar Coordenadas"
    self.coord = QLabel("INGRESA LAS COORDENADAS INICIALES:", self) # Creación del texto "Ingresar coordenadas"
    self.coord.move(50, 115)                                        # Ubicamos del texto "Ingresar coordenadas"
    self.coord.resize(500, 30)                                      # Tamaño   del texto "Ingresar coordenadas"
    self.coord.setFont(QFont("Times New Roman", 16))                # Modificación de la fuente y el tamaño

    # Texto "Ingresar Velocidad"
    self.speed = QLabel("INGRESA LA VELOCIDAD INICIAL:", self)      # Creación del texto "Ingresar velocidad"
    self.speed.move(50, 225)                                        # Ubicamos del texto "Ingresar velocidad"
    self.speed.resize(500, 30)                                      # Tamaño   del texto "Ingresar velocidad"
    self.speed.setFont(QFont("Times New Roman", 16))                # Modificación de la fuente y el tamaño

    # Texto "Ingresar Tiempo Final"
    self.time = QLabel("INGRESA EL TIEMPO FINAL:", self)            # Creación del texto "Ingresar tiempo final"
    self.time.move(50, 335)                                         # Ubicamos del texto "Ingresar tiempo final"
    self.time.resize(500, 30)                                       # Tamaño   del texto "Ingresar tiempo final"
    self.time.setFont(QFont("Times New Roman", 16))                 # Modificación de la fuente y el tamaño

    # Etiqueta para mostrar mensaje y resultados
    self.result = QLabel("POSICIÓN FINAL:", self)
    self.result.move(50, 445)                                         # Ubicamos del texto "Posición final"
    self.result.resize(500, 30)                                       # Tamaño   del texto "Posición final"
    self.result.setFont(QFont("Times New Roman", 16))                 # Modificación de la fuente y el tamaño


    # COORDENADAS INICIALES
    # Cuadro para agregar la coordenadas x
    self.rx = QLineEdit(self)                          # Variable x
    self.rx.setPlaceholderText("Coordenada x")         # Texto dentro de la caja
    self.rx.setGeometry(50, 165, 150, 30)              # Tamaño y ubicación caja
    
    # Cuadro para agregar la coordenadas y
    self.ry = QLineEdit(self)                          # Variable y
    self.ry.setPlaceholderText("Coordenada y")         # Texto dentro de la caja
    self.ry.setGeometry(250, 165, 150, 30)             # Tamaño caja
    
    # Cuadro para agregar la coordenadas z
    self.rz = QLineEdit(self)                          # Variable z
    self.rz.setPlaceholderText("Coordenada z")         # Texto dentro de la caja
    self.rz.setGeometry(450, 165, 150, 30)             # Tamaño caja


    # VELOCIDAD INICIAL
    # Cuadro para agregar la velocidad en x
    self.vx = QLineEdit(self)                          # Variable vx
    self.vx.setPlaceholderText("Velocidad en x")       # Texto dentro de la caja
    self.vx.setGeometry(50, 275, 150, 30)              # Tamaño caja
    
    # Cuadro para agregar la velocidad en y
    self.vy = QLineEdit(self)                          # Variable vy
    self.vy.setPlaceholderText("Velocidad en y")       # Texto dentro de la caja
    self.vy.setGeometry(250, 275, 150, 30)             # Tamaño caja

    # Cuadro para agregar la velocidad en z
    self.vz = QLineEdit(self)                          # Variable vz
    self.vz.setPlaceholderText("Velocidad en z")       # Texto dentro de la caja
    self.vz.setGeometry(450, 275, 150, 30)             # Tamaño caja
    

    # TIEMPO FINAL
    # Cuadro para agregar el tiempo final
    self.tf = QLineEdit(self)                          # Variable tf
    self.tf.setPlaceholderText("Tiempo final")         # Texto dentro de la caja
    self.tf.setGeometry(50, 385, 150, 30)              # Tamaño caja


    # PLOTEO 3D
    self.fig = Figure(figsize=(5, 4))                       # Creamos la figura donde poder plotear
    self.canvas = FigureCanvas(self.fig)                    # Creamos un canvas para que la figura que creamos sea compatible con PyQt
    self.ax = self.fig.add_subplot(111, projection='3d')    
    self.canvas.setGeometry(700, 50, 600, 400)              # Centramos el gráfico donde queremos
    self.canvas.setParent(self)                             # Conectamos el canvas con la ventana

  def plot_3D(self, xs, ys, zs):
    self.ax.clear()                     # Limpiamos lo que haya estado dibujado antes

    self.ax.plot(xs, ys, zs, lw=2)      # Dibujamos la trayectoria

    xmin, xmax = min(xs), max(xs)          # Calculamos los valores límites de la trayectoria en X
    ymin, ymax = min(ys), max(ys)          # Calculamos los valores límites de la trayectoria en Y
    zmax = max(zs)                         # Calculamos el límite superior  de la trayectoria en Z

    xmin, xmax = min(xmin,0), max(xmax,0)  # Calculamos nuevos límites de forma que 0 pertence [xmin, xmax]
    ymin, ymax = min(ymin,0), max(ymax,0)  # Calculamos nuevos límites de forma que 0 pertence [ymin, ymax]

    self.ax.set_xlim(xmin, xmax)           # Seteamos los límites del eje X
    self.ax.set_ylim(ymin, ymax)           # Seteamos los límites del eje Y
    self.ax.set_zlim(0, zmax)              # Seteamos los límites del eje Z


    self.ax.plot([xmin, xmax], [0,0], [0,0], color="black", linewidth=1.2)    # Ploteamos el eje X
    self.ax.plot([0,0], [ymin, ymax], [0,0], color="black", linewidth=1.2)    # Ploteamos el eje Y
    self.ax.plot([0,0], [0,0], [0   , zmax], color="black", linewidth=1.2)    # Ploteamos el eje Z
    self.ax.scatter([0],[0],[0], color="black", s=20)                         # Ploteamos el origen de coordenadas

    self.ax.set_xlabel("X")                                                   # Asignamos el label "X" al eje X
    self.ax.set_ylabel("Y")                                                   # Asignamos el label "Y" al eje Y
    self.ax.set_zlabel("Z")                                                   # Asignamos el label "Z" al eje Z

    self.canvas.draw()    # Finalmente dibijamos todo 

  def show_final_point(self, rf):
    rxf, ryf, rzf = rf
    
    # Construimos el mensaje
    mensaje = f"POSICIÓN FINAL: ({round(rxf, 2)}, {round(ryf, 2)}, {round(rzf, 2)})"

    # Lo mostramos al usuario
    self.result.setText(mensaje)

  def obtain_coord(self):
    if (self.rx.text() == "") or (self.ry.text() == "") or (self.rz.text() == ""):
      return "N"
    elif (is_float(self.rx.text()) and is_float(self.ry.text()) and is_float(self.rz.text())):
      return (float(self.rx.text()), float(self.ry.text()), float(self.rz.text()))
    else:
      return "T"

  def obtain_speed(self):
    if (self.vx.text() == "") or (self.vy.text() == "") or (self.vz.text() == ""):
      return "N"
    elif (is_float(self.vx.text()) and is_float(self.vy.text()) and is_float(self.vz.text())):
      return (float(self.vx.text()), float(self.vy.text()), float(self.vz.text()))
    else:
      return "T"
   
  def obtain_final_time(self):
    if self.tf.text() == "":
      return "N"
    elif is_float(self.tf.text()):
      return float(self.tf.text())
    else: 
      return "T"
    
  def error_message(self, msj):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(msj)
    msg.setIcon(QMessageBox.Icon.Critical)  # Icono de error
    msg.exec()

  def simulate_trajectory(self):
    # Primero obtenemos la lista de valores
    coord      = self.obtain_coord()
    speed      = self.obtain_speed()
    final_time = self.obtain_final_time()

    if coord == "N":
      self.error_message("Error al ingresar la posición inicial! No ingresaste un argumento")
    elif coord == "T":
      self.error_message("Error al ingresar la posición inicial! Tipo erroneo en un argumento")

    elif speed == "N":
      self.error_message("Error al ingresar la velocidad inicial! No ingresaste un argumento")
    elif speed == "T":
      self.error_message("Error al ingresar la velocidad inicial! Tipo erroneo en un argumento")

    elif final_time == "N":
      self.error_message("Error al ingresar la tiempo final! No ingresaste un argumento")
    elif final_time == "T":
      self.error_message("Error al ingresar la tiempo final! Tipo erroneo en un argumento")

    else:
      xs, ys, zs, rf = calculate_trajectory(coord, speed, final_time, 100000)
      self.show_final_point(rf)
      self.plot_3D(xs, ys, zs)


# Ejecución del programa
if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = TrajectorySimulator()
    window.show()
    app.exec()


