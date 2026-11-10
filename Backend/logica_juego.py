# Algoritmos detrás de una partida comenzada
from os import path
from parametros import ANCHO_GRILLA, LARGO_GRILLA, TIEMPO_CUENTA_REGRESIVA, CANTIDAD_VIDAS,\
    MULTIPLICADOR_PUNTAJE
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from entidades import Luigi, FantasmaHorizontal, FantasmaVertical, Fuego, Roca, Pared

class Juego(QObject):
    senal_enviar_grilla = pyqtSignal(dict) # Para actualizar grilla en front
    senal_game_over = pyqtSignal(int) # Actualización del puntaje al término del juego
    senal_tiempo = pyqtSignal(str) # Actualización de tiempo
    senal_vidas = pyqtSignal(str) # Actualización de vidas

    def __init__(self):
        super().__init__()
        # Dimensiones de grillas
        self.ancho = ANCHO_GRILLA
        self.alto = LARGO_GRILLA
        self.partida_inicial = [] # Lista de listas que representa a tablero. Reinicio partida.
        self.luigi = '' # Será la entidad de Luigi.
        self.posicion_estrella = '' # Ubicación de victoria.
        self.fantasmas_horiz = [] # Entidades de fantasmas horizontal. 
        self.fantasmas_verti = [] # Entidades de fantasmas vertical.
        self.paredes = [] # Entidades pared.
        self.rocas = [] # Entidades roca.
        self.fuegos = [] # Entidades fuego.
        self.perdidas = 0 # Veces que se ha perdido. Esto + 1 = Vidas usadas.
        self.termino = False # Saber si la partida ha terminado.
        # Timers
        self.timer_tiempo = QTimer()
        self.timer_tiempo.timeout.connect(self.actualizar_tiempo)
        self.timer_fantasmas_h = QTimer()
        self.timer_fantasmas_h.timeout.connect(self.mover_fantasmas_horizontales)
        self.timer_fantasmas_v = QTimer()
        self.timer_fantasmas_v.timeout.connect(self.mover_fantasmas_verticales)
        # Puntaje
        self.puntaje = 0
        self.diccionario_grilla = {} # Se manda para que main lo interprete. 
        # Tiempo
        self.contador_tiempo = TIEMPO_CUENTA_REGRESIVA # Cuenta el tiempo que va quedando. 
        # Pausa
        self.pausado = False
        
    def actualizacion_datos_partida(self):
        # Modificación de datos: (columna, fila)
        # Recordar que posiciones van de (1,1) a (9, 14). Esto por la forma de la grilla. 
        for fila in range(len(self.partida_inicial)):
            for columna in range(len(self.partida_inicial[0])):
                if self.partida_inicial[fila][columna] == 'L':  # posicion_y, posicion_x
                    self.luigi = Luigi(columna + 1, fila + 1, CANTIDAD_VIDAS) 
                if self.partida_inicial[fila][columna] == 'P':
                    self.paredes.append(Pared(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'F':
                    self.fuegos.append(Fuego(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'H':
                    self.fantasmas_horiz.append(FantasmaHorizontal(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'V':
                    self.fantasmas_verti.append(FantasmaVertical(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'S':
                    self.posicion_estrella = (columna + 1, fila + 1)
                if self.partida_inicial[fila][columna] == 'R':
                    self.rocas.append(Roca(columna + 1, fila + 1))

    def leer_archivo(self, archivo_partida): # El nombre del archivo. 
    # Ejecuta distintas concatenaciones dependiendo si se viene del constructor o no.
        if not type(archivo_partida) == type(list()): # Desde ventana de inicio.
            archivo_txt = archivo_partida + '.txt'
            ruta_partida = path.join('mapas', archivo_txt)
            with open(ruta_partida, 'r') as file:
                for linea in file: 
                    lista_linea = list(linea.strip())
                    self.partida_inicial.append(lista_linea)
            self.actualizacion_datos_partida()       
            self.comenzar_partida() 

        if archivo_partida == self.partida_inicial:
            self.actualizacion_datos_partida()       
            self.comenzar_partida() 

        elif type(archivo_partida) == type(list()): # Desde ventana constructor.
            for fila in range(len(archivo_partida)):
                fila_actual = []
                for columna in range(len(archivo_partida[0])):
                    if archivo_partida[fila][columna] == 'luigi':
                        fila_actual.append('L')
                    elif archivo_partida[fila][columna] == 'pared':
                        fila_actual.append('P')
                    elif archivo_partida[fila][columna] == 'estrella':
                        fila_actual.append('S')
                    elif archivo_partida[fila][columna] == 'fantasma_h':
                        fila_actual.append('H')
                    elif archivo_partida[fila][columna] == 'fantasma_v':
                        fila_actual.append('V')
                    elif archivo_partida[fila][columna] == 'fuego':
                        fila_actual.append('F')
                    elif archivo_partida[fila][columna] == 'roca':
                        fila_actual.append('R')
                    else:
                        fila_actual.append('-')
                self.partida_inicial.append(fila_actual)
               
            self.actualizacion_datos_partida()       
            self.comenzar_partida() 
    
    def reiniciar_juego(self):
        self.posicion_estrella = '' # Ubicación de victoria.
        self.fantasmas_horiz = [] # Entidades de fantasmas horizontal. 
        self.fantasmas_verti = [] # Entidades de fantasmas vertical.
        self.paredes = [] # Entidades pared.
        self.rocas = [] # Entidades roca.
        self.fuegos = [] # Entidades fuego.
        self.perdidas = 0 # Veces que se ha perdido. Esto + 1 = Vidas usadas.
        self.termino = False
        self.contador_tiempo = TIEMPO_CUENTA_REGRESIVA
        self.luigi.cantidad_vidas = CANTIDAD_VIDAS
        self.puntaje = 0
        self.diccionario_grilla = {}
        self.leer_archivo(self.partida_inicial)

    def comenzar_partida(self): # Solo para iniciar la partida.
            self.crear_grilla() # Crear diccionario de grilla. Se irá actualizando.
            self.actualizar_grilla() # Actualizamos diccionario de la grilla.
            # Activar QTimers de tiempo y fantasmas.
            self.timer_tiempo.start(1000)
            if len(self.fantasmas_horiz) > 0:
                self.timer_fantasmas_h.start((int(self.fantasmas_horiz[0].tiempo_movimiento * 1000\
                    )))
            if len(self.fantasmas_verti) > 0:
                self.timer_fantasmas_v.start((int(self.fantasmas_verti[0].tiempo_movimiento * 1000\
                    )))
            
    def mover_luigi(self, movimiento): # movimiento = señal de Frontend (un str)
        luigi_pierde = False 
        moverse = True
        horizontal = False
        vertical = False
        direccion = 0
        # Juego no está pausado ni terminado.
        if self.pausado == False and self.termino == False: 
            if movimiento == 'izquierda' or movimiento == 'derecha': # Movimiento horizontal.
                if movimiento == 'izquierda':
                    direccion = -1
                if movimiento == 'derecha':
                    direccion = 1
                horizontal = True
                posible_posicion = (self.luigi.posicion_x + direccion, self.luigi.posicion_y)
            if movimiento == 'abajo' or movimiento == 'arriba': # movimiento vertical
                if movimiento == 'abajo':
                    direccion = 1
                if movimiento == 'arriba':
                    direccion = -1
                vertical = True
                posible_posicion = (self.luigi.posicion_x, self.luigi.posicion_y + direccion)
            # Posible posición dentro del tablero.
            if posible_posicion[0] >= 1 and posible_posicion[0] <= ANCHO_GRILLA - 2 and\
                posible_posicion[1] >= 1 and posible_posicion[1] <= LARGO_GRILLA - 2:
                # No se mueve si hay pared.
                for pared in self.paredes:
                    if pared.posicion_x == posible_posicion[0]:
                         if pared.posicion_y == posible_posicion[1]:
                            moverse = False     
                # Se mueve si hay fantasma, fuego o roca. Luego ver si luigi pierde.
                for f_h in self.fantasmas_horiz:
                    if f_h.posicion_x == posible_posicion[0]:
                        if f_h.posicion_y == posible_posicion[1]:
                            # Choca con fantasma.
                            luigi_pierde = True        
                for f_v in self.fantasmas_verti: # Análogo a caso anterior.
                    if f_v.posicion_x == posible_posicion[0]:
                        if f_v.posicion_y == posible_posicion[1]:
                            luigi_pierde = True
                for fuego in self.fuegos:
                    if fuego.posicion_x == posible_posicion[0]:
                        if fuego.posicion_y == posible_posicion[1]:
                            luigi_pierde = True
                for roca in range(len(self.rocas)): 
                    # Ver si luigi y roca se mueven.
                    if self.rocas[roca].posicion_x == posible_posicion[0]:
                        if self.rocas[roca].posicion_y == posible_posicion[1]:
                            if horizontal: # luigi se movió horizontalmente
                                pos_roca = (posible_posicion[0] + direccion, \
                                    posible_posicion[1])      
                            if vertical: # luigi se movió verticalmente
                                pos_roca = (posible_posicion[0], \
                                    posible_posicion[1] + direccion)
                            # Ver si la posible posicion está adentro. Si es asi la roca y luigo
                            # se mueven. Se usará diccionario. pos_roca = posible posicion_roca.
                            if pos_roca[0] >= 1 and pos_roca[0] <= ANCHO_GRILLA - 2\
                                and pos_roca[1] >= 1 and pos_roca[1] <= LARGO_GRILLA - 2:                     
                                if self.diccionario_grilla[pos_roca] != 'EspacioVacio':
                                    # Se impide movimiento.
                                    moverse = False                             
                                if self.diccionario_grilla[pos_roca] == 'EspacioVacio': 
                                    # Se mueven luigi y la roca.
                                    self.rocas[roca].moverse(movimiento)
                                    moverse = True
                            else: # ni luigi ni la roca se mueven porque la roca saldria del mapa.
                                moverse = False
                self.actualizar_grilla()
                if moverse: # Se mueve
                    self.luigi.moverse(movimiento)
                self.actualizar_grilla()
                if luigi_pierde:
                    self.perder_vidas() # Reinicia o termina partida dependiendo del caso.

    def mover_fantasmas_horizontales(self):
        if self.pausado == False: # Juego no está pausado. 
            # Posiciones de fantasmas de self.fantasmas_horiz que desaparecerán.
            posiciones_fantasmas_desaparecen = [] 
            reinicio = False
            nuevos_fantasmas = []
            lista = self.fantasmas_horiz.copy() # Para que no haya problemas con el for.
            for fantas in range(len(lista)):
                direccion = '' # Valor de posible movimiento del fantasma.
                if lista[fantas].moviendose_derecha:
                    direccion = 1
                if not lista[fantas].moviendose_derecha:
                    direccion = -1
                posible_posicion_x = lista[fantas].posicion_x + direccion
                # Dentro del tablero, se puede mover.
                if posible_posicion_x >= 1 and posible_posicion_x <= (ANCHO_GRILLA - 2):
                    # Ver si choca algo. 
                    for fuego in self.fuegos:
                        if fuego.posicion_x == posible_posicion_x and \
                            fuego.posicion_y == lista[fantas].posicion_y:
                            posiciones_fantasmas_desaparecen.append(fantas)
                            self.fantasmas_horiz[fantas].moverse() # fantasma se mueve.
                    for pared in self.paredes:
                        if pared.posicion_x == posible_posicion_x and \
                            pared.posicion_y == lista[fantas].posicion_y:
                            self.fantasmas_horiz[fantas].cambio_movimiento()
                            # Se cambia de direccion 
                    for roca in self.rocas:
                        if roca.posicion_x == posible_posicion_x and \
                            roca.posicion_y == lista[fantas].posicion_y:
                            # Se cambia de direccion
                            self.fantasmas_horiz[fantas].cambio_movimiento()
                    if self.luigi.posicion_x == posible_posicion_x and\
                        self.luigi.posicion_y == lista[fantas].posicion_y:
                        self.fantasmas_horiz[fantas].moverse() # fantasma se mueve.
                        reinicio = True
                    else:
                        self.fantasmas_horiz[fantas].moverse() # fantasma se mueve.

                else: # Fantasma choca con borde. Actualizar orientación.
                    self.fantasmas_horiz[fantas].cambio_movimiento()
                
            self.actualizar_grilla() # Se actualiza frontend. 
            if posiciones_fantasmas_desaparecen != []: # Desaparecen algunos fantasmas.
                for pos in range(len(self.fantasmas_horiz)):
                    if pos not in posiciones_fantasmas_desaparecen:
                        nuevos_fantasmas.append(self.fantasmas_horiz[pos])
                self.fantasmas_horiz = nuevos_fantasmas # Fantasmas actualizados.
                self.actualizar_grilla() # Sacar fantasmas muertos.
            if reinicio == True: # Fantasma chocó con Luigi.
                self.perder_vidas() # Reinicio y actualización de vidas.
                
    def mover_fantasmas_verticales(self): # Análogo de mover fantasmas horizontales. 
        if self.pausado == False:  
            fantasmas_desaparecen = [] 
            nuevos_fantasmas = [] 
            reinicio = False
            lista = self.fantasmas_verti.copy()
            for fantas in range(len(lista)):
                direccion = ''
                if lista[fantas].moviendose_abajo:
                    direccion = 1
                if not lista[fantas].moviendose_abajo:
                    direccion = -1
                posible_posicion_y = lista[fantas].posicion_y + direccion 
                if posible_posicion_y >= 1 and posible_posicion_y <= (LARGO_GRILLA - 2):
                    for fuego in self.fuegos:
                        if fuego.posicion_x == lista[fantas].posicion_x and \
                            fuego.posicion_y == posible_posicion_y:
                            self.fantasmas_verti[fantas].moverse() 
                            fantasmas_desaparecen.append(fantas)
                    for pared in self.paredes:
                        if pared.posicion_x == lista[fantas].posicion_x and \
                            pared.posicion_y == posible_posicion_y:
                            self.fantasmas_verti[fantas].cambio_movimiento()
                    for roca in self.rocas:
                        if roca.posicion_x == lista[fantas].posicion_x and \
                            roca.posicion_y == posible_posicion_y:
                            self.fantasmas_verti[fantas].cambio_movimiento()
                    if self.luigi.posicion_x == lista[fantas].posicion_x and\
                        self.luigi.posicion_y == posible_posicion_y:
                        self.fantasmas_verti[fantas].moverse() 
                        reinicio = True 
                    else:
                        self.fantasmas_verti[fantas].moverse() 
                if posible_posicion_y < 1 or posible_posicion_y > (LARGO_GRILLA - 2): 
                    self.fantasmas_verti[fantas].cambio_movimiento()     
            self.actualizar_grilla() 
            if fantasmas_desaparecen != []: 
                for pos in range(len(self.fantasmas_verti)): 
                    if not pos in fantasmas_desaparecen:
                        nuevos_fantasmas.append(self.fantasmas_verti[pos])
                self.fantasmas_verti = nuevos_fantasmas 
                self.actualizar_grilla()   
            if reinicio == True: 
                self.perder_vidas()
    
    def crear_grilla(self):
        for fila in range(1, self.alto - 1):
            for columna in range(1, self.ancho - 1):
                self.diccionario_grilla[(columna, fila)] = 'EspacioVacio'

    def vaciar_grilla(self):
        for key in self.diccionario_grilla.keys():
            self.diccionario_grilla[key] = 'EspacioVacio'
            # Recordar que solo pone como espacio vacio lo que esta dentro de las paredes.

    def actualizar_grilla(self):
        self.vaciar_grilla()
        # Actualizar todos los elementos en el frontend
        for fantasma_hori in self.fantasmas_horiz:
            x, y = fantasma_hori.posicion_x, fantasma_hori.posicion_y
            self.diccionario_grilla[(x, y)] = 'FantasmaHorizontal'
        for fantasma_vert in self.fantasmas_verti:
            x, y = fantasma_vert.posicion_x, fantasma_vert.posicion_y
            self.diccionario_grilla[(x, y)] = 'FantasmaVertical'
        for pared in self.paredes:
            x, y = pared.posicion_x, pared.posicion_y
            self.diccionario_grilla[(x, y)] = 'Pared'
        for roca in self.rocas:
            x, y = roca.posicion_x, roca.posicion_y
            self.diccionario_grilla[(x, y)] = 'Roca'
        for fuego in self.fuegos:
            x, y = fuego.posicion_x, fuego.posicion_y
            self.diccionario_grilla[(x, y)] = 'Fuego'
        self.diccionario_grilla[self.posicion_estrella] = 'Estrella'
        x, y = self.luigi.posicion_x, self.luigi.posicion_y
        self.diccionario_grilla[(x,y)] = 'Luigi'
        # Señal para la ventana del juego.
        self.senal_enviar_grilla.emit(self.diccionario_grilla)

    def actualizar_tiempo(self): # Lo llama QTimer asociado al tiempo.
        if not self.pausado:
            self.contador_tiempo -= 1
            self.senal_tiempo.emit(str(self.contador_tiempo))
            if self.contador_tiempo == 0:
                self.game_over()

    def perder_vidas(self):
        self.perdidas += 1
        self.luigi.perder_vida()
        self.senal_vidas.emit(str(self.luigi.cantidad_vidas))
        if self.luigi.cantidad_vidas == 0:
            self.game_over() # Actualiza ventana.
        if self.luigi.cantidad_vidas != 0:
            self.reiniciar_partida() # La funcion actualiza grilla.

    def pausar_reanudar(self):
        # Se detienen o reanudan los QTimers dependiendo del caso.
        if self.pausado == False:
            self.pausado = True
            if self.timer_fantasmas_h.isActive() == True:
                self.timer_fantasmas_h.stop()
            if self.timer_fantasmas_v.isActive() == True:
                self.timer_fantasmas_v.stop()
            self.timer_tiempo.stop() # Para el tiempo y los fantasmas. Para luigi no.   
        elif self.pausado == True: # Se quiere reanudar el juego
            if len(self.fantasmas_horiz) > 0:
                self.timer_fantasmas_h.start((int(self.\
                    fantasmas_horiz[0].tiempo_movimiento * 1000)))
            if len(self.fantasmas_verti) > 0:
                self.timer_fantasmas_v.start((int(self.\
                fantasmas_verti[0].tiempo_movimiento * 1000)))
            self.timer_tiempo.start(1000)
            self.pausado = False

    def vaciar_partida(self): # Para el reinicio del juego.
            self.luigi = ''
            self.posicion_estrella = '' 
            self.fantasmas_horiz = [] 
            self.fantasmas_verti = [] 
            self.paredes = [] 
            self.rocas = [] 
            self.fuegos = [] 
            self.pausado = False

    def reiniciar_partida(self): # Para reiniciar juego cuando luigi pierde vida.
        if self.timer_fantasmas_h.isActive():
            self.timer_fantasmas_h.stop()
        if self.timer_fantasmas_v.isActive():
            self.timer_fantasmas_v.stop()
        self.vaciar_partida() # Para actualizar elementos necesarios de la partida.
        for fila in range(len(self.partida_inicial)):
            for columna in range(len(self.partida_inicial[0])):
                if self.partida_inicial[fila][columna] == 'L':
                    self.luigi = Luigi(columna + 1, fila + 1, CANTIDAD_VIDAS - self.perdidas ) 
                if self.partida_inicial[fila][columna] == 'P':
                    self.paredes.append(Pared(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'F':
                    self.fuegos.append(Fuego(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'H':
                    self.fantasmas_horiz.append(FantasmaHorizontal(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'V':
                    self.fantasmas_verti.append(FantasmaVertical(columna + 1, fila + 1))
                if self.partida_inicial[fila][columna] == 'S':
                    self.posicion_estrella = (columna + 1, fila + 1)
                if self.partida_inicial[fila][columna] == 'R':
                    self.rocas.append(Roca(columna + 1, fila + 1))
        self.actualizar_grilla() # Se actualiza frontend.
        if len(self.fantasmas_horiz) > 0: # Reiniciar fantasmas.
            self.timer_fantasmas_h.start((int(self.\
                    fantasmas_horiz[0].tiempo_movimiento * 1000))) 
        if len(self.fantasmas_verti) > 0:
            self.timer_fantasmas_v.start((int(self.\
                    fantasmas_verti[0].tiempo_movimiento * 1000))) 
        
    def ganar(self):
        if self.luigi.posicion_x == self.posicion_estrella[0]:
            if self.luigi.posicion_y == self.posicion_estrella[1]:
                self.puntaje = int(\
                    (self.contador_tiempo * MULTIPLICADOR_PUNTAJE) / (self.perdidas + 1))
                self.game_over()

    def game_over(self): # El juego se termina.
        self.termino = True
        self.vaciar_grilla()
        self.fantasmas_horiz = [] 
        self.fantasmas_verti = [] 
        self.paredes = [] 
        self.rocas = [] 
        self.fuegos = [] 
        self.senal_game_over.emit(self.puntaje)
        if self.timer_fantasmas_h.isActive():
            self.timer_fantasmas_h.stop()
        if self.timer_fantasmas_v.isActive():
            self.timer_fantasmas_v.stop()
        self.timer_tiempo.stop()

    def eliminar_fantasmas(self): # Para el uso del cheatcode.
        cantidadh = len(self.fantasmas_horiz.copy())
        cantidadv = len(self.fantasmas_verti.copy())
        for h in range(cantidadh):
            self.fantasmas_horiz.pop()
        for v in range(cantidadv):
            self.fantasmas_verti.pop()
        self.actualizar_grilla()
# Menos de 400 líneas de código. 





            
