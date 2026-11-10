# Algoritmos detrás de una partida comenzada

from parametros import MAXIMO_FANTASMAS_VERTICAL, MAXIMO_FANTASMAS_HORIZONTAL, MAXIMO_FUEGO,\
    MAXIMO_PARED, MAXIMO_ROCA, LARGO_GRILLA, ANCHO_GRILLA
from PyQt5.QtCore import pyqtSignal, QObject


class ModoConstructor(QObject):

    senal_ubicar_elemento = pyqtSignal(list)
    senal_vaciar_grilla = pyqtSignal()
    senal_enviar_textos = pyqtSignal(list)
    senal_jugar = pyqtSignal(list) # info de la partida

    def __init__(self):
        super().__init__()
        # Elementos disponibles
        self.luigi = 1
        self.fantasmas_h = MAXIMO_FANTASMAS_HORIZONTAL
        self.fantasmas_v = MAXIMO_FANTASMAS_VERTICAL
        self.fuegos = MAXIMO_FUEGO
        self.paredes = MAXIMO_PARED
        self.rocas = MAXIMO_ROCA
        self.estrella = 1
        self.posiciones_usadas = []
        self.elementos_posiciones = {}
        
    def construir(self, lista):
        # lista = [posicion, elemento seleccionado]
        cantidad = 0
        ubicacion_valida = False 
        for i in range(len(lista[0])):
            lista[0][i] = int(lista[0][i]) 
        posicion = lista[0] # [columna, fila]
        elemento = lista[1] # str con nombre
        # El método seguirá si y solo si la ubicacion es valida
        if elemento == 'luigi':
            if self.luigi == 1: # se puede poner. 
                if posicion not in self.posiciones_usadas: # Ver ubicación
                    ubicacion_valida = True
                    self.luigi -= 1 # Se pone luigi
                    cantidad = self.luigi
        if elemento == 'pared':
            if self.paredes > 0: # se puede poner. 
                if posicion not in self.posiciones_usadas: 
                    ubicacion_valida = True
                    self.paredes -= 1 
                    cantidad = self.paredes
        if elemento == 'estrella':
            if self.estrella > 0: # se puede poner. 
                if posicion not in self.posiciones_usadas: 
                    ubicacion_valida = True
                    self.estrella -= 1 
                    cantidad = self.estrella
        if elemento == 'fantasma_h':
            if self.fantasmas_h > 0: # se puede poner. 
                if posicion not in self.posiciones_usadas: 
                    ubicacion_valida = True
                    self.fantasmas_h -= 1 
                    cantidad = self.fantasmas_h
        if elemento == 'fantasma_v':
            if self.fantasmas_v > 0: # se puede poner. 
                if posicion not in self.posiciones_usadas: 
                    ubicacion_valida = True
                    self.fantasmas_v -= 1 
                    cantidad = self.fantasmas_v
        if elemento == 'fuego':
            if self.fuegos > 0: # se puede poner. 
                if posicion not in self.posiciones_usadas: 
                    ubicacion_valida = True
                    self.fuegos -= 1 
                    cantidad = self.fuegos
        if elemento == 'roca':
            if self.rocas > 0: # se puede poner. 
                if posicion not in self.posiciones_usadas: 
                    ubicacion_valida = True
                    self.rocas -= 1 
                    cantidad = self.rocas
        if ubicacion_valida: # se manda señal con elemento y lugar donde se debe poner
            # actualizar posiciones
            self.posiciones_usadas.append(posicion) # lista de enteros con coordenadas
            self.senal_ubicar_elemento.emit([posicion, elemento, cantidad])
            # Se usará para enviar información de juego.
            self.elementos_posiciones[(posicion[0], posicion[1])] = elemento
            # (columna, fila)
    
    def jugar(self):
        if self.luigi == 0 and self.estrella == 0:
            llaves_posiciones = []
            for key in self.elementos_posiciones.keys(): # las llaves son tuplas
                llaves_posiciones.append(key) 
            lista_partida = []
            # Se arman filas y se van agregando a lista_partida
            for fila in range(1, LARGO_GRILLA - 1):
                fila_actual = []
                for columna in range(1, ANCHO_GRILLA - 1):
                    if (columna, fila) in llaves_posiciones:
                        fila_actual.append(self.elementos_posiciones[(columna, fila)])
                        # el valor es un str
                    #if not ((columna, fila) in llaves_posiciones):
                    else:
                        fila_actual.append('-') # espacio vacío
                lista_partida.append(fila_actual)
                
            self.senal_jugar.emit(lista_partida)
            # Se tiene una lista de listas con info de la partida. Al estilo de la que se lee
            # en el archivo "logica_juego"
        return


    def limpiar(self): # Actualiza los datos
        self.senal_vaciar_grilla.emit()
        self.senal_vaciar_grilla.emit()
        self.elementos_posiciones = {}
        self.luigi = 1
        self.fantasmas_h = MAXIMO_FANTASMAS_HORIZONTAL
        self.fantasmas_v = MAXIMO_FANTASMAS_VERTICAL
        self.fuegos = MAXIMO_FUEGO
        self.paredes = MAXIMO_PARED
        self.rocas = MAXIMO_ROCA
        self.estrella = 1
        # Para actualizar textos de los botones
        textos = [f'({self.luigi})', f'({self.fantasmas_h})', f'({self.fantasmas_v})', \
            f'({self.fuegos})', f'({self.paredes})', f'({self.rocas})', \
                f'({self.estrella})']
        self.senal_enviar_textos.emit(textos)
        self.posiciones_usadas = []

    



            


        