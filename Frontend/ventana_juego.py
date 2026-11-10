from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QDesktopWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt5.QtGui import QPixmap
from os import path
from parametros import LARGO_GRILLA, ANCHO_GRILLA, CANTIDAD_VIDAS
from PyQt5.QtMultimedia import QSoundEffect


class VentanaJuego(QWidget):
    senal_luigi = pyqtSignal(str)
    empezar_senal_frontend = pyqtSignal()
    senal_pausa = pyqtSignal()
    senal_ganar = pyqtSignal()
    senal_eliminar_fantasmas = pyqtSignal()
    senal_invencible = pyqtSignal()
    senal_reiniciar_juego = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.init_gui()
        self._keys_fantasmas = {Qt.Key_I: False, Qt.Key_K: False, Qt.Key_L: False}
        #self._keys_invencible = {Qt.Key_I: False, Qt.Key_N: False, Qt.Key_F: False}

    def init_gui(self):
        self.setWindowTitle('MODO JUEGO') 
        self.setGeometry(0, 0, 750, 800)
        self.generar_widgets() # Crea Widgets de ventana de inicio
        self.generar_layouts() # Ubica widgets en la ventana
        self.center_window() # Método que centrará la ventana con respecto a pantalla

    def nombre_usuario(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario

    def generar_widgets(self):
        # Primer layout vertical. Los botones #
        # Creamos íconos
        # Tiempo
        self._tiempo = QLabel('Tiempo ', self) 
        self.tiempo = QLabel('0', self)
        # Vidas
        self._vidas = QLabel('Vidas ', self) 
        self.vidas = QLabel(f'{CANTIDAD_VIDAS}', self) # vidas iniciales
        # Puntaje
        self._puntaje = QLabel('PUNTAJE: ', self)
        self.puntaje = QLabel(self)
        # Fin del juego
        self.resultado = QLabel(self)
        self._salir = QPushButton('Salir', self) # botón para salir
        self._salir.clicked.connect(self.salir_de_partida)
        self._salir.hide()
        self.reiniciar_partida = QLabel(self)
        self.reiniciar_partida = QPushButton('Reiniciar Partida', self) # botón para salir
        self.reiniciar_partida.clicked.connect(self.reiniciar_juego)
        self.reiniciar_partida.hide()

        # Nombre usuario
        self.label_usuario = QLabel(self)
        # Botones
        self.boton_pausa = QPushButton('Pausar', self)
        self.boton_pausa.clicked.connect(self.pausa) # actualiza label de boton pausa_reanudar
        self.boton_limpiar = QPushButton('Limpiar', self)
        self.boton_limpiar.setEnabled(False)
        self.boton_jugar = QPushButton('Jugar', self)
        self.boton_jugar.setEnabled(False)
        # Segundo layout vertical. La grilla del juego # 
        self.grilla_juego = QGridLayout() # Añadiremos los bordes
        for fila in range(LARGO_GRILLA):
            for columna in range(ANCHO_GRILLA):
                if not (fila == 0 or fila == (LARGO_GRILLA - 1) or columna == 0 or \
                    columna == (ANCHO_GRILLA - 1)):
                    casil = QLabel(self)
                    casil.setFixedSize(30, 30) #
                    casil.setStyleSheet("background-color : black; \
                        border: 1px solid grey;")
                    self.grilla_juego.addWidget(casil, fila, columna) 
                    casil.setMinimumWidth(casil.sizeHint().height())
                    # Se añade celda base a toda la grilla
                    # Agregaremos paredes en celdas pertinentes
                label_borde = QLabel(self)
                pixeles_borde = QPixmap(path.join('sprites', 'Elementos', 'bordermap.png'))
                label_borde.setPixmap(pixeles_borde)

                if fila == 0 or fila == (LARGO_GRILLA - 1) or columna == 0 or \
                    columna == (ANCHO_GRILLA - 1):
                    self.grilla_juego.addWidget(label_borde, fila, columna) # columna, fila
                    


        self.grilla_juego.setContentsMargins(60, 100, 60, 100)
        self.grilla_juego.setSpacing(0) 

        # Tenemos grilla del juego con paredes.
    
    def reiniciar_juego(self):
        for fila in range(LARGO_GRILLA):
            for columna in range(ANCHO_GRILLA):
                if not (fila == 0 or fila == (LARGO_GRILLA - 1) or columna == 0 or \
                    columna == (ANCHO_GRILLA - 1)):
                    casil = QLabel(self)
                    casil.setFixedSize(30, 30) #
                    casil.setStyleSheet("background-color : black; \
                        border: 1px solid grey;")
                    self.grilla_juego.addWidget(casil, fila, columna) 
                    casil.setMinimumWidth(casil.sizeHint().height())
                    # Se añade celda base a toda la grilla
                    # Agregaremos paredes en celdas pertinentes
                label_borde = QLabel(self)
                pixeles_borde = QPixmap(path.join('sprites', 'Elementos', 'bordermap.png'))
                label_borde.setPixmap(pixeles_borde)

                if fila == 0 or fila == (LARGO_GRILLA - 1) or columna == 0 or \
                    columna == (ANCHO_GRILLA - 1):
                    self.grilla_juego.addWidget(label_borde, fila, columna) # columna, fila
        self.puntaje.setText('') # puntaje
        self.vidas.setText(f'{CANTIDAD_VIDAS}')
        self.label_usuario.setText('') # nombre del usuario
        self.resultado.setText('')
        self._salir.hide()
        self.reiniciar_partida.hide()
        self.senal_reiniciar_juego.emit()


    def generar_layouts(self): # Agregaremos widgets creados a la ventana de juego.
        self.hbox0 = QHBoxLayout()
        # Se crean los layouts
        # botones
        vbox1 = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hboxp = QHBoxLayout()
        hboxr = QHBoxLayout()
        hbox_username = QHBoxLayout()
        hbox_salir  = QHBoxLayout()

        hbox1.addStretch(1)
        hbox1.addWidget(self._tiempo) # label de texto "Tiempo"
        hbox1.addWidget(self.tiempo) # label de contador tiempo
        hbox1.addStretch(1)

        hbox2.addStretch(1)
        hbox2.addWidget(self._vidas) # label de texto "Vidas"
        hbox2.addWidget(self.vidas) # label de contador vidas
        hbox2.addStretch(1)


        hbox3.addStretch(1)
        hbox3.addWidget(self.boton_pausa) 
        hbox3.addStretch(1)

        hboxp.addStretch(1)
        hboxp.addWidget(self._puntaje) # label de texto puntaje
        hboxp.addWidget(self.puntaje) # label de puntaje
        hboxp.addStretch(1)


        hboxr.addStretch(1)
        hboxr.addWidget(self.resultado)
        hboxr.addStretch(1)

        hbox_username.addStretch(1)
        hbox_username.addWidget(self.label_usuario) 
        hbox_username.addStretch(1)

        hbox_salir.addStretch(1)
        hbox_salir.addWidget(self._salir) 
        hbox_salir.addWidget(self.reiniciar_partida)
        hbox_salir.addStretch(1)

        hbox4.addStretch(1)
        hbox4.addWidget(self.boton_limpiar) 
        hbox4.addWidget(self.boton_jugar) 
        hbox4.addStretch(1)

        vbox1.addStretch(1)
        vbox1.addLayout(hbox1) # tiempo
        vbox1.addLayout(hbox2) # vida
        vbox1.addLayout(hbox3) # pausa
        vbox1.addLayout(hboxp) # puntuacion
        vbox1.addLayout(hboxr) # Resultado
        vbox1.addLayout(hbox_username) # Nombre de usuario
        vbox1.addStretch(1)
        vbox1.addLayout(hbox_salir)
        vbox1.addStretch(5) # mucho espacio antes de boton limpiar y jugar
        vbox1.addLayout(hbox4) # limpiar y jugar

        # Grilla del juego
        vbox2 = QVBoxLayout()
        hbox5 = QHBoxLayout()
        #hbox5.addStretch(1)
        hbox5.addLayout(self.grilla_juego)
        #hbox5.addStretch(1)

        #vbox2.setStyleSheet("background-color: black;")
        vbox2.addLayout(hbox5) 
        
        # Unión de todos los layouts
        self.hbox0.addLayout(vbox1)
        self.hbox0.addLayout(vbox2)
        # Actualicemos cambios en la ventana
        self.setLayout(self.hbox0)

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

    # Se va llamando automáticamente.
    def actualizar_tiempo(self, tiempo): 
        self.tiempo.setText(str(tiempo)) # Llega de lógica juego.
    # Se llama si Luigi pierde una vida
    def actualizar_vidas(self, vidas): # Se actualicen vidas en pantalla
        self.vidas.setText(str(vidas)) 

       
    # Solo para actualizar lo de adentro del tablero, no los bordes
    def actualizar_grilla(self, diccionario_grilla): # Actualizar grid layouts
        for fila in range(1, LARGO_GRILLA - 1):
            for columna in range(1, ANCHO_GRILLA - 1):

                item = self.grilla_juego.itemAtPosition(fila, columna) # casilla
                widget = item.widget() # widget de la casilla
                self.grilla_juego.removeWidget(widget) # remover el widget
                casil = QLabel(self)
                casil.setStyleSheet("background-color: black; \
                    border: 1px solid grey;")
                if diccionario_grilla[columna, fila] == 'Luigi':
                    ruta_image = path.join('sprites', 'Personajes', 'luigi_down_1.png')
                    pixeles = QPixmap(ruta_image)
                    pixeles = pixeles.scaled(casil.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    casil.setPixmap(pixeles)
                    casil.setScaledContents(True)
                if diccionario_grilla[columna, fila] == 'FantasmaHorizontal':
                    ruta_image = path.join('sprites', 'Personajes', 'white_ghost_left_1.png')
                    pixeles = QPixmap(ruta_image)
                    pixeles = pixeles.scaled(casil.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    casil.setPixmap(pixeles)
                    casil.setScaledContents(True)
                if diccionario_grilla[columna, fila] == 'FantasmaVertical':
                    ruta_image = path.join('sprites', 'Personajes', 'red_ghost_vertical_1.png')
                    pixeles = QPixmap(ruta_image)
                    pixeles = pixeles.scaled(casil.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    casil.setPixmap(pixeles)
                    casil.setScaledContents(True)
                
                if diccionario_grilla[columna, fila] == 'Pared':
                    ruta_image = path.join('sprites', 'Elementos', 'wall.png')
                    pixeles = QPixmap(ruta_image)
                    pixeles = pixeles.scaled(casil.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    casil.setPixmap(pixeles)
                    casil.setScaledContents(True)
                    
                if diccionario_grilla[columna, fila] == 'Roca':
                    ruta_image = path.join('sprites', 'Elementos', 'rock.png')
                    pixeles = QPixmap(ruta_image)
                    pixeles = pixeles.scaled(casil.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    casil.setPixmap(pixeles)
                    casil.setScaledContents(True)
                    
                if diccionario_grilla[columna, fila] == 'Fuego':
                    ruta_image = path.join('sprites', 'Elementos', 'fire.png')
                    pixeles = QPixmap(ruta_image)
                    pixeles = pixeles.scaled(casil.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    casil.setPixmap(pixeles)
                    casil.setScaledContents(True)
                    
                if diccionario_grilla[columna, fila] == 'Estrella':
                    ruta_image = path.join('sprites', 'Elementos', 'osstar.png')
                    pixeles = QPixmap(ruta_image)
                    pixeles = pixeles.scaled(casil.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    casil.setPixmap(pixeles)
                    casil.setScaledContents(True) # contenido se ajusta a widget
                self.grilla_juego.addWidget(casil, fila, columna)

        self.grilla_juego.setSpacing(0)
        return
    
    def fin_del_juego(self, puntaje): # puntaje = int
        for fila in range(LARGO_GRILLA):
            for columna in range(ANCHO_GRILLA):
                casil = QLabel(self)
                casil.setStyleSheet("background-color: black; \
                    border: 1px solid grey;")
                self.grilla_juego.addWidget(casil, fila, columna) 
                # Sacamos todos los sprites
        self.puntaje.setText(str(puntaje)) # puntaje
        self.label_usuario.setText(self.nombre_usuario) # nombre del usuario
        self.musica = QSoundEffect() 
        # cancion
        if puntaje == 0:
            self.resultado.setText('DERROTA')
            ruta = path.join('sounds', 'gameOver.wav')
            self.musica.setSource(QUrl.fromLocalFile(ruta))
            
        if puntaje != 0:
            self.resultado.setText('VICTORIA')
            ruta = path.join('sounds', 'stageClear.wav')
            self.musica.setSource(QUrl.fromLocalFile(ruta))
        self.musica.play() 
        self._salir.show()
        self.reiniciar_partida.show() # el botón para reiniciar

        
    def salir_de_partida(self):
        QApplication.quit()
        return

    def pausa(self):
        texto = self.boton_pausa.text()
        if texto == 'Pausar': # Se quiere pausar el texto. Se tiene que actualizar label
            self.boton_pausa.setText('Reanudar')
            self.senal_pausa.emit()

        if texto == 'Reanudar':
            self.boton_pausa.setText('Pausar')
            self.senal_pausa.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.senal_luigi.emit('izquierda')
        if event.key() == Qt.Key_D:
            self.senal_luigi.emit('derecha')
        if event.key() == Qt.Key_W:
            self.senal_luigi.emit('arriba')
        if event.key() == Qt.Key_S:
            self.senal_luigi.emit('abajo')
        if event.key() == Qt.Key_G:
            self.senal_ganar.emit()
        if event.key() == Qt.Key_P:
            self.pausa()

        #self._keys_fantasmas = {Qt.Key_I: False, Qt.Key_K: False, Qt.Key_L: False}
        #self._keys_invencible = {Qt.Key_I: False, Qt.Key_N: False, Qt.Key_F: False}
        if event.key() in [Qt.Key_I, Qt.Key_K, Qt.Key_L]:
            self._keys_fantasmas[event.key()] = True
            if self._keys_fantasmas[Qt.Key_I] and self._keys_fantasmas[Qt.Key_K] and\
                 self._keys_fantasmas[Qt.Key_L]:
                self.senal_eliminar_fantasmas.emit()

    def keyReleaseEvent(self, event):
        if event.key() in [Qt.Key_I, Qt.Key_K, Qt.Key_L]:
            
            self._keys_fantasmas[event.key()] = False
        # if event.key() in [Qt.Key_I, Qt.Key_N, Qt.Key_F]:
        #    self._keys_invencible[event.key()] = False



