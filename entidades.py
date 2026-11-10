
from parametros import MIN_VELOCIDAD, MAX_VELOCIDAD
from random import uniform # Números aleatorios entre floats.


                                ### Entidades del juego ###

class Luigi():
    def __init__(self, x, y, cantidad_vidas): 
        self.nombre = 'Luigi'
        self.posicion_x = x
        self.posicion_y = y
        self.cantidad_vidas = cantidad_vidas

    def perder_vida(self):
        self.cantidad_vidas -= 1
        
    def moverse(self, sentido): # sentido = str -> derecha, abajo, etc.
        if sentido == 'derecha':
            self.posicion_x += 1
        if sentido == 'izquierda':
            self.posicion_x -= 1
        if sentido == 'abajo':
            self.posicion_y += 1
        if sentido == 'arriba':
            self.posicion_y -= 1

        # Fantasmas #     
               
class FantasmaHorizontal():
    # ¡Atributo de clase!
    # Todos los fantasmas de este tipo se mueven a la misma velocidad #
    tiempo_movimiento = 1 / (uniform(MIN_VELOCIDAD, MAX_VELOCIDAD))
    def __init__(self, x, y): 
        self.nombre = 'FantasmaHorizontal'
        self.posicion_x = x
        self.posicion_y = y
        
        self.moviendose_derecha = True 
        self.direccion = 1 
        
    def moverse(self): # Se llama en caso pertinente.
        if self.moviendose_derecha == True:
            self.posicion_x += 1
        if self.moviendose_derecha == False:
            self.posicion_x -= 1

    def cambio_movimiento(self):
        if self.moviendose_derecha == True:
            self.moviendose_derecha = False
        else:
            self.moviendose_derecha = True
      
            
class FantasmaVertical():
    # Todos los fantasmas de este tipo se mueven a la misma velocidad #
    tiempo_movimiento = 1 / (uniform(MIN_VELOCIDAD, MAX_VELOCIDAD))
    def __init__(self, x, y): 
        self.nombre = 'FantasmaVertical'
        self.posicion_x = x
        self.posicion_y = y
        self.moviendose_abajo = True # 

    def moverse(self): 
        if self.moviendose_abajo == True:
            self.posicion_y += 1
        else:
            self.posicion_y -= 1

    def cambio_movimiento(self):
        if self.moviendose_abajo == True:
            self.moviendose_abajo = False
        else:
            self.moviendose_abajo = True
            
        # Bloques #
                           
class Pared():
    def __init__(self, x, y): 
            self.nombre = 'Pared'
            self.posicion_x = x
            self.posicion_y = y
            # Inamovible e impenetrable.
            # Ni Luigi ni Fantasmas pueden atravesarla o moverla.
   

class Roca():
    def __init__(self, x, y):
            self.nombre = 'Roca'
            self.posicion_x = x
            self.posicion_y = y
            # Impenetrable.
            # Fantasma debe chocar y devolverse.
            # Si Luigi choca con él, la roca debe moverse en la misma dirección de Luigi. Si 
            # es que esa casilla está ocupada, la roca no se mueve.

    def moverse(self, sentido):
        if sentido == 'derecha':
            self.posicion_x += 1
        if sentido == 'izquierda':
            self.posicion_x -= 1
        if sentido == 'abajo':
            self.posicion_y += 1
        if sentido == 'arriba':
            self.posicion_y -= 1
          
class Fuego():
    def __init__(self, x, y): 
            self.nombre = 'Fuego'
            self.posicion_x = x
            self.posicion_y = y
            # Daño e inamovible.
            # Si fantasma choca con fuego, entonces desaparece. 
            # Si Luigi choca con fuego, entonces pierde una vida y se reinicia el nivel. 

# (Los métodos más complejos asociados al movimiento estarán en clase juego) #