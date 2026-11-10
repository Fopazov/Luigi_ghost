from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QDesktopWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox)
from PyQt5.QtGui import QPixmap, QIcon
from os import path
from parametros import MAXIMO_FANTASMAS_HORIZONTAL, MAXIMO_FANTASMAS_VERTICAL, MAXIMO_FUEGO,\
    MAXIMO_PARED, MAXIMO_ROCA, LARGO_GRILLA, ANCHO_GRILLA
from PyQt5.QtCore import Qt


class VentanaConstructor(QWidget):

    senal_construir = pyqtSignal(list) 
    senal_limpiar = pyqtSignal()
    senal_jugar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.seleccionado = ''
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('MODO CONSTRUCTOR') 
        self.setGeometry(0, 0, 750, 800)
        self.generar_widgets() # Crea Widgets de ventana.
        self.generar_layouts() # Organiza widgets en layouts.
        self.center_window() # Centra la ventana.
        
    def generar_widgets(self):
        # Lista de filtros
        self.filtro = QComboBox(self)
        self.filtro.addItem('Todos')
        self.filtro.addItem('Bloques')
        self.filtro.addItem('Entidades')
        self.filtro.currentTextChanged.connect(self.filtrar)
        # Botones
        self.boton_luigi = QPushButton(' (1)', self)
        self.boton_luigi.setIcon(QIcon(path.join('sprites', 'Personajes', 'luigi_left_1.png')))
        self.boton_luigi.setStyleSheet("text-align: right; image-position: center")
        self.boton_luigi.clicked.connect(self.seleccionado_luigi)

        self.boton_pared = QPushButton(f' ({MAXIMO_PARED})', self)
        self.boton_pared.setIcon(QIcon(path.join('sprites', 'Elementos', 'wall.png')))
        self.boton_pared.setStyleSheet("text-align: right; image-position: center")
        self.boton_pared.clicked.connect(self.seleccionado_pared)

        self.boton_roca = QPushButton(f' ({MAXIMO_ROCA})', self)
        self.boton_roca.setIcon(QIcon(path.join('sprites', 'Elementos', 'rock.png')))
        self.boton_roca.setStyleSheet("text-align: right; image-position: center")
        self.boton_roca.clicked.connect(self.seleccionado_roca)

        self.boton_estrella = QPushButton(f' (1)', self)
        self.boton_estrella.setIcon(QIcon(path.join('sprites', 'Elementos', 'osstar.png')))
        self.boton_estrella.setStyleSheet("text-align: right; image-position: center")
        self.boton_estrella.clicked.connect(self.seleccionado_estrella)

        self.boton_fantasma_h = QPushButton(f' ({MAXIMO_FANTASMAS_HORIZONTAL})', self)
        self.boton_fantasma_h.setIcon(QIcon(path.join\
            ('sprites', 'Personajes', 'white_ghost_left_1.png')))
        self.boton_fantasma_h.setStyleSheet("text-align: right; image-position: center")
        self.boton_fantasma_h.clicked.connect(self.seleccionado_fantasma_h)

        self.boton_fantasma_v = QPushButton(f' ({MAXIMO_FANTASMAS_VERTICAL})', self)
        self.boton_fantasma_v.setIcon(QIcon(path.join\
            ('sprites', 'Personajes', 'red_ghost_vertical_1.png')))
        self.boton_fantasma_v.setStyleSheet("text-align: right; image-position: center")
        self.boton_fantasma_v.clicked.connect(self.seleccionado_fantasma_v)

        self.boton_fuego = QPushButton(f' ({MAXIMO_FUEGO})', self)
        self.boton_fuego.setIcon(QIcon(path.join('sprites', 'Elementos', 'fire.png')))
        self.boton_fuego.setStyleSheet("text-align: right; image-position: center")
        self.boton_fuego.clicked.connect(self.seleccionado_fuego)

        self.boton_limpiar = QPushButton('Limpiar', self)
        self.boton_limpiar.clicked.connect(self.limpiar)
        self.boton_jugar = QPushButton('Jugar', self)
        self.boton_jugar.clicked.connect(self.jugar)

        # Botones casillas
        # Columna, fila
        self.casillas = {}
        # Grilla: Pero en vez de casillas, tiene botones
        self.grilla_constructor = QGridLayout()
        for fila in range(LARGO_GRILLA):
            for columna in range(ANCHO_GRILLA): 
                label = QLabel(self) # Puede ser borde o casilla de tablero (boton)
                pixeles_borde = QPixmap(path.join('sprites', 'Elementos', 'bordermap.png'))
                if fila == 0 or fila == (LARGO_GRILLA - 1) or columna == 0 or \
                    columna == (ANCHO_GRILLA - 1):
                    label.setFixedSize(30, 30)
                    label.setPixmap(pixeles_borde)
                    label.setMinimumWidth(label.sizeHint().height())
                    label.setStyleSheet("background-color : black; \
                        border: 1px solid grey;")
                    self.grilla_constructor.addWidget(label, fila, columna)
                    # Hace que mapa tiemble:
                    #label.setMinimumHeight(label.sizeHint().width())
                    
                if fila > 0 and fila < (LARGO_GRILLA - 1) and columna > 0 and \
                    columna < (ANCHO_GRILLA - 1):
                    # Cada botón queda conectado a la función apretar casilla
                    boton_casilla = QPushButton(f'{columna},{fila}', self) # info que se lleva
                    boton_casilla.setFixedSize(30, 30)
                    boton_casilla.setMinimumWidth(label.sizeHint().height())
                    boton_casilla.setStyleSheet("background-color : black; \
                        border: 1px solid grey;")
                    boton_casilla.clicked.connect(self.apretar_casilla)
                    self.casillas[(columna, fila)] = boton_casilla
                    # No se podrían ejecutar los siguientes comandos
                    #self.casillas[(columna, fila)].setMinimumWidth(label.sizeHint().height())
                    #self.casillas[(columna, fila)].setMinimumHeight(label.sizeHint().width())
                    #self.casillas[(columna, fila)].clicked.connect(self.apretar_casilla)
                    # Fin comandos.
                    self.grilla_constructor.addWidget(self.casillas[(columna, fila)], fila, columna)
                    
        self.grilla_constructor.setContentsMargins(60, 100, 60, 100)
        self.grilla_constructor.setSpacing(0) 
         
    
    def generar_layouts(self):
        self.hbox0 = QHBoxLayout()
        # Se crean los layouts
        vbox1 = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hboxr = QHBoxLayout()
        hboxe = QHBoxLayout()
        hbox_fantasma_h = QHBoxLayout()
        hbox_v  = QHBoxLayout()
        hbox_f = QHBoxLayout()

        hbox1.addStretch(1)
        hbox1.addWidget(self.filtro) 
        hbox1.addStretch(1)

        hbox2.addStretch(1)
        hbox2.addWidget(self.boton_luigi) 
        hbox2.addStretch(1)

        hbox3.addStretch(1)
        hbox3.addWidget(self.boton_pared)
        hbox3.addStretch(1)

        hboxr.addStretch(1)
        hboxr.addWidget(self.boton_roca)
        hboxr.addStretch(1)

        hboxe.addStretch(1)
        hboxe.addWidget(self.boton_estrella)
        hboxe.addStretch(1)

        hbox_fantasma_h.addStretch(1)
        hbox_fantasma_h.addWidget(self.boton_fantasma_h)
        hbox_fantasma_h.addStretch(1)

        hbox_v.addStretch(1)
        hbox_v.addWidget(self.boton_fantasma_v) 
        hbox_v.addStretch(1)

        hbox_f.addStretch(1)
        hbox_f.addWidget(self.boton_fuego) 
        hbox_f.addStretch(1)

        hbox4.addStretch(1)
        hbox4.addWidget(self.boton_limpiar) 
        hbox4.addWidget(self.boton_jugar) 
        hbox4.addStretch(1)

        vbox1.addStretch(1)
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2) 
        vbox1.addLayout(hbox3) 
        vbox1.addLayout(hboxr) 
        vbox1.addLayout(hboxe) 
        vbox1.addLayout(hbox_fantasma_h) 
        vbox1.addLayout(hbox_v)
        vbox1.addLayout(hbox_f)
        vbox1.addStretch(5) # Mucho espacio antes de boton limpiar y jugar.
        vbox1.addLayout(hbox4) # Boton limpiar y jugar.

        # Grilla del constructor #
        vbox2 = QVBoxLayout()
        hbox5 = QHBoxLayout()
        hbox5.addLayout(self.grilla_constructor)

        vbox2.addLayout(hbox5) 
        
        # Unión de todos los layouts #
        self.hbox0.addLayout(vbox1)
        self.hbox0.addLayout(vbox2)
        # Actualicemos cambios en la ventana #
        self.setLayout(self.hbox0)


    def center_window(self): # Igual que en otras ventanas
        
        geometria_pantalla = QDesktopWidget().screenGeometry()
        geometria_ventana = self.frameGeometry()
        x = (geometria_pantalla.width() - geometria_ventana.width()) // 2
        y = (geometria_pantalla.height() - geometria_ventana.height()) // 2
        self.move(x, y)
        return

    def filtrar(self): # Cuando se cambia elección en QComboBox
        if self.filtro.currentText() == 'Todos':
            self.boton_luigi.show()
            self.boton_pared.show()
            self.boton_roca.show()
            self.boton_estrella.show()
            self.boton_fantasma_h.show()
            self.boton_fantasma_v.show()
            self.boton_fuego.show()
        if self.filtro.currentText() == 'Bloques':
            self.boton_luigi.hide()
            self.boton_pared.show()
            self.boton_roca.show()
            self.boton_estrella.show()
            self.boton_fantasma_h.hide()
            self.boton_fantasma_v.hide()
            self.boton_fuego.show()
        if self.filtro.currentText() == 'Entidades':
            self.boton_luigi.show()
            self.boton_pared.hide()
            self.boton_roca.hide()
            self.boton_estrella.hide()
            self.boton_fantasma_h.show()
            self.boton_fantasma_v.show()
            self.boton_fuego.hide()
        return
    
    def apretar_casilla(self): 
        if self.seleccionado != '': # Se tiene seleccionado algo
            # (self.sender().text()) # str de formato "columna,fila"
            posicion = (self.sender().text()).split(',') #transformas posicion en lista
            self.senal_construir.emit([posicion, self.seleccionado])
            # se manda a backend para que lo analice

    # Lista contiene una lista de enteros que representan la posicion 
    # y un string asociado al elemento. Además de cantidad de elementos que quedan.
    def actualizar_visualizacion(self, lista): 
        posicion = lista[0]
        elemento = lista[1]
        cantidad = lista[2]
        ruta_imagen = ''
        if elemento == 'luigi':
            ruta_imagen = path.join('sprites', 'Personajes', 'luigi_down_1.png')
            self.boton_luigi.setText(f'({cantidad})')
        
        if elemento == 'pared':
            ruta_imagen = path.join('sprites', 'Elementos', 'wall.png')
            self.boton_pared.setText(f'({cantidad})')
        if elemento == 'estrella':
            ruta_imagen = path.join('sprites', 'Elementos', 'osstar.png')
            self.boton_estrella.setText(f'({cantidad})')
        if elemento == 'fantasma_h':
            ruta_imagen = path.join('sprites', 'Personajes', 'white_ghost_left_1.png')
            self.boton_fantasma_h.setText(f'({cantidad})')
        if elemento == 'fantasma_v':
            ruta_imagen = path.join('sprites', 'Personajes', 'red_ghost_vertical_1.png')
            self.boton_fantasma_v.setText(f'({cantidad})')
        if elemento == 'fuego':
            ruta_imagen = path.join('sprites', 'Elementos', 'fire.png')
            self.boton_fuego.setText(f'({cantidad})')
        if elemento == 'roca':
            ruta_imagen = path.join('sprites', 'Elementos', 'rock.png')
            self.boton_roca.setText(f'({cantidad})')
        # Ubicar en la grilla. No es necesario remover botón
        label = QLabel(self) # Puede ser borde o casilla de tablero (boton)
        pixeles = QPixmap(ruta_imagen)
        pixeles = pixeles.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(pixeles)
        self.grilla_constructor.addWidget(label, posicion[1], posicion[0])
        return 

    # Funciones que se activan al apretar botones. 
    def seleccionado_luigi(self): 
        self.seleccionado = 'luigi'
      
    def seleccionado_pared(self):
        self.seleccionado = 'pared'

    def seleccionado_estrella(self):
        self.seleccionado = 'estrella'

    def seleccionado_fantasma_h(self):
        self.seleccionado = 'fantasma_h'

    def seleccionado_fantasma_v(self):
        self.seleccionado = 'fantasma_v'

    def seleccionado_fuego(self):
        self.seleccionado = 'fuego'

    def seleccionado_roca(self):
        self.seleccionado = 'roca'

    def limpiar(self):
        self.senal_limpiar.emit()

    def vaciar_grilla(self): # Se reinicializan los botones
        self.casillas = {}
        for fila in range(1, LARGO_GRILLA - 1):
            for columna in range(1, ANCHO_GRILLA - 1):
                label = QLabel(self) #
                item = self.grilla_constructor.itemAtPosition(fila, columna) 
                widget = item.widget() 
                self.grilla_constructor.removeWidget(widget)
                widget.hide()
                widget.deleteLater()
                boton_casilla = QPushButton(f'{columna},{fila}', self) 
                boton_casilla.setFixedSize(30, 30)
                boton_casilla.setMinimumWidth(label.sizeHint().height())
                boton_casilla.setStyleSheet("background-color : black; border: 1px solid grey;")
                boton_casilla.clicked.connect(self.apretar_casilla)
                self.casillas[(columna, fila)] = boton_casilla
                self.grilla_constructor.addWidget(self.casillas[(columna, fila)], fila, columna)
            
    def actualizar_textos(self, lista): 
        # Lista de textos para botones (las cantidades)
        # textos = [f'({self.luigi})', f'({self.fantasmas_h})', f'({self.fantasmas_v})', \
        #    f'({self.fuegos})', f'({self.paredes})', f'({self.rocas})', \
        #        f'({self.estrella})']
        self.boton_luigi.setText(lista[0])
        self.boton_fantasma_h.setText(lista[1])
        self.boton_fantasma_v.setText(lista[2])
        self.boton_fuego.setText(lista[3])
        self.boton_pared.setText(lista[4])
        self.boton_roca.setText(lista[5])
        self.boton_estrella.setText(lista[6])

                
    def jugar(self):
        self.senal_jugar.emit()

        return
