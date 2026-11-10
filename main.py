# Archivo a ejecutar
# Este archivo es el "puente" de las señales entre backend y frontend
from sys import exit
from PyQt5.QtWidgets import QApplication

from Frontend.ventana_inicio import VentanaInicio
from Backend.log_inicio import VentanaInicioBackend
from Frontend.ventana_juego import VentanaJuego
from Frontend.ventana_constructor import VentanaConstructor
from Backend.logica_juego import Juego
from Backend.log_constructor import ModoConstructor

# Si

if __name__ == '__main__':
    app = QApplication([])

                                            # Instancias #

    # Ventana inicio: (front-end y back-end)
    ventana_inicio = VentanaInicio()
    ventana_inicio_backend = VentanaInicioBackend()

    # Ventana juego: (front-end y back-end)
    ventana_juego = VentanaJuego()
    logica_juego = Juego()

    # Ventana constructor: (front-end y back-end)
    ventana_constructor = VentanaConstructor()
    logica_constructor = ModoConstructor()
    # El backend estará asociado al archivo de lógica juego

                                            ## Señales ##

    # Verificar nombre de usuario y si está mal al tratar de empezar, arrojar error. 
    ventana_inicio.senal_verificar_usuario.connect(ventana_inicio_backend.verificar_usuario)
    ventana_inicio_backend.senal_mensaje_error.connect(ventana_inicio.error_usuario)
    
    ## Partida: Cierre ventana de inicio y comienzo de juego escogido o constructor ##
    ventana_inicio_backend.senal_empezar_juego.connect(ventana_inicio.jugar)
    ventana_inicio_backend.senal_nombre_juego.connect(ventana_juego.nombre_usuario)
    # Inicio modo juego desde ventana de inicio
    # se lee y parte la partida si se llega desde la ventana de inicio
    ventana_inicio.senal_empezar_juego.connect(logica_juego.leer_archivo) 
    # Se muestra ventana del juego con entidades
    ventana_inicio.senal_empezar_juego.connect(ventana_juego.show) 
    
    # Modo Constructor #
    ventana_inicio.senal_modo_constructor.connect(ventana_constructor.show)
    ventana_constructor.senal_construir.connect(logica_constructor.construir)
    logica_constructor.senal_ubicar_elemento.connect(ventana_constructor.actualizar_visualizacion)
    ventana_constructor.senal_limpiar.connect(logica_constructor.limpiar)
    logica_constructor.senal_vaciar_grilla.connect(ventana_constructor.vaciar_grilla)
    logica_constructor.senal_enviar_textos.connect(ventana_constructor.actualizar_textos)
    ventana_constructor.senal_jugar.connect(logica_constructor.jugar)
    # Se manda info de partida para que el juego inicie
    logica_constructor.senal_jugar.connect(logica_juego.leer_archivo) # logica
    logica_constructor.senal_jugar.connect(ventana_juego.show) # mostrar ventana de juego
    logica_constructor.senal_jugar.connect(ventana_constructor.close) # mostrar ventana de juego

    ## Conexiones de Ventana de juego ## 
    ventana_juego.senal_pausa.connect(logica_juego.pausar_reanudar)
    ventana_juego.senal_luigi.connect(logica_juego.mover_luigi)
    # Se apreta la letra g del teclado
    ventana_juego.senal_ganar.connect(logica_juego.ganar)
    ventana_juego.senal_eliminar_fantasmas.connect(logica_juego.eliminar_fantasmas)
    ventana_juego.senal_reiniciar_juego.connect(logica_juego.reiniciar_juego)
    # bonus de 2 décimas
    # logica_juego. con logica de movimiento
    logica_juego.senal_enviar_grilla.connect(ventana_juego.actualizar_grilla)
    logica_juego.senal_game_over.connect(ventana_juego.fin_del_juego)
    logica_juego.senal_tiempo.connect(ventana_juego.actualizar_tiempo)
    logica_juego.senal_vidas.connect(ventana_juego.actualizar_vidas)

    
    # Inicialización de la ventana de inicio y con ello, del programa.
    ventana_inicio_backend.senal_empezar.connect(ventana_inicio.show)
    ventana_inicio_backend.empezar()

    exit(app.exec())