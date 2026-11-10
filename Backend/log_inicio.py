
from parametros import MAX_CARACTERES, MIN_CARACTERES
from PyQt5.QtCore import pyqtSignal, QObject
from string import ascii_letters



class VentanaInicioBackend(QObject):
    senal_mensaje_error = pyqtSignal()
    senal_empezar_juego = pyqtSignal() # Modo constructor o juego
    senal_empezar = pyqtSignal() # para que se abra la ventana de inicio
    senal_nombre_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
    def verificar_usuario(self, usuario): # nombre ingresado por el usuario debe ser válido.
        letras_sin_tilde = list(ascii_letters)
        letras = letras_sin_tilde + ['á', 'Á', 'e', 'É', 'í', 'Í', 'ó', 'Ó', 'ú', 'Ú']
        letras_con_tilde = ['á', 'Á', 'e', 'É', 'í', 'Í', 'ó', 'Ó', 'ú', 'Ú']
        
        buen_nombre = True # se asume correcto
        tiene_numeros = False
        tiene_letras = False
        tiene_tildes = False
        tiene_normales = False # letras sin tildes

        if len(usuario) > MAX_CARACTERES or len(usuario) < MIN_CARACTERES:
            buen_nombre = False

        if buen_nombre: # incluyendo los extremos
            for letra in usuario:
                if buen_nombre: # no se encontrado caracter invalido en el string
                    if letra in '0123456789':
                        tiene_numeros = True
                    elif letra in letras:
                        tiene_letras = True
                        if letra in letras_con_tilde:
                            tiene_tildes = True
                        if letra in letras_sin_tilde:
                            tiene_normales = True
                    else: # caracter especial especial
                        buen_nombre = False
        valido = False
        # Por ahora ha pasado todas las condiciones
        if buen_nombre: # dentro del rango de carácteres y no tiene carácteres especiales
            # solo se entra a una condicion
            if not tiene_numeros and not tiene_tildes:
                valido = True
            elif not tiene_letras and tiene_numeros:
                valido = True
            elif tiene_letras and tiene_numeros: 
                valido = True

        if valido:
            self.senal_empezar_juego.emit()
            self.senal_nombre_juego.emit(usuario)
        if not valido:
            self.senal_mensaje_error.emit()
            
    # Abre ventana de inicio una vez que se ejecuta el programa. Solo se activa al principio.
    def empezar(self):
        self.senal_empezar.emit()
        
# Ahora si terminé la tarea. 