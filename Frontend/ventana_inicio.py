# Encargado de la visual de la ventana de inicio
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QDesktopWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtGui import QPixmap
from os import path, listdir # listdir se usará para obtener nombres de los mapas



### Ventana de inicio
class VentanaInicio(QWidget):
    senal_verificar_usuario = pyqtSignal(str)
    senal_empezar_juego = pyqtSignal(str)
    senal_modo_constructor = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.inicializa_gui()

    def inicializa_gui(self):
        # Características
        self.setWindowTitle('MENÚ PRINCIPAL') 
        self.porte = (750, 800)
        self.setGeometry(0, 0, 750, 800)
        self.imagen = QLabel('', self)
        self.imagen.setGeometry(0, 0, *self.porte)
         # (Ancho, Alto). Dimensiones de la pantalla
        self.generar_widgets() # Crea Widgets de ventana de inicio
        self.agregar_estilo() # Otorga estilo a Widgets
        self.center_window() # Método que centrará la ventana con respecto a pantalla
        
    # Centrar ventana #
    def center_window(self):
        # Obtener geometría de la pantalla y ventana
        geometria_pantalla = QDesktopWidget().screenGeometry()
        geometria_ventana = self.frameGeometry()
        # Cálculo de coordenadas del centrado de la ventana
        # Se calcula coordenadas de esquina superior izquierda
        x = (geometria_pantalla.width() - geometria_ventana.width()) // 2
        y = (geometria_pantalla.height() - geometria_ventana.height()) // 2
        # Movemos la ventana
        self.move(x, y)
        
    def generar_widgets(self): # También genera layouts
        # Fondo
        pixeles = QPixmap(path.join('sprites', 'Fondos', 'fondo_inicio.png'))
        pixeles = pixeles.scaled(*self.porte, Qt.KeepAspectRatioByExpanding)
        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)
        # Creamos íconos
        # Título: Imagen a la que se le ajustó el tamaño
        self.titulo = QLabel(self)
        pixeles2 = QPixmap(path.join('sprites', 'Elementos', 'logo.png'))
        pixeles2 = pixeles2.scaled(550, 150)
        self.titulo.setPixmap(pixeles2)
        # Ingreso de datos del usuario #
        # Texto Username: 
        self.Username = QLabel('Username: ', self)
        # Qline edit
        self.username = QLineEdit('', self)
        # Creación del listado de opciones
        self.opciones = QComboBox(self)
        # lista con nombres de los mapas
        self.option = QLabel('Escoge una opción y empieza:', self)
        lista_mapas = listdir(path.join('mapas')) 
        for mapa in lista_mapas:
            mapa_sin_extension = mapa[:-4] # se saca extensión
            self.opciones.addItem(mapa_sin_extension)
        self.opciones.addItem('Modo Constructor')
        self.boton_login = QPushButton('Empezar', self)
        # Llama función de empezar partida dependiendo lo que escogió usuario
        self.boton_login.clicked.connect(self.verificar_usuario)

        # Se crean los layouts
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.titulo) # Imagen
        hbox1.addStretch(1)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.Username) # texto Username
        hbox2.addWidget(self.username) # QlineEdit
        hbox2.addStretch(1)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.option) # texto escoger opción.
        hbox3.addWidget(self.opciones) # listado de opciones.
        self.option.setMaximumWidth(180) # Ajusta el tamaño del texto para mejor visualización.
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.boton_login) # boton empiezo
        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox1)
        vbox.addStretch(4)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        #vbox.addStretch(0.5)
        vbox.addLayout(hbox4)
        self.setLayout(vbox)  
        self.salir = QPushButton('Salir', self) # botón para salir
        self.salir.clicked.connect(self.boton_salir)
        self.salir.move(0, 0)

    
    def agregar_estilo(self): # Agregar estilo a widgets una vez creados y posicionados

        # Fondo negro y letra blanca
        self.Username.setStyleSheet('''
            color: white;
            background: black;
        ''')
        self.option.setStyleSheet('''
            color: white;
            background: black;
        ''')
        # Un marco para escribir
        self.username.setStyleSheet("QLineEdit { border: 1px solid white; }")
        # Color de letras del botón
        self.boton_login.setStyleSheet("QPushButton { background-color: black; color: white; }")
        self.salir.setStyleSheet("QPushButton { background-color: black; color: white; }")
        # salir = al botón para salir

    def verificar_usuario(self):
        # Mandamos nombre de usuario al backend para verificarlo
        self.senal_verificar_usuario.emit(self.username.text())

        
    def error_usuario(self): # mensaje de error
        error_label = QLabel('Nombre de usuario inválido', self)
        error_label.setStyleSheet("""
            font-size: 16px;
            color: red;
            text-align: center;
    """)
        vbox = self.layout()
        vbox.insertWidget(4, error_label)
    
    def jugar(self): # Usuario ingreso correctamente un posible nombre
        if self.opciones.currentText() == 'Modo Constructor': # Se abre ventana de modo constructor
            self.senal_modo_constructor.emit() #
            self.close() # Se cierra ventana de inicio
            # señal para empezar el modo constructor:
           
            
        else: # Se escogió uno de los mapas predeterminados
            self.senal_empezar_juego.emit(self.opciones.currentText()) 
            self.close() # se cierra ventana de inicio
            # señal para empezar el juego 
           
    # Si se presion botón salir, el programa termina de ejecutarse. 
    def boton_salir(self):
        QApplication.quit()
        return
    


