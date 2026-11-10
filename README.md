# Tarea 2: DCCazafantasmas 👻🧱🔥


## Consideraciones generales :octocat:

<La tarea cumple con los requisitos en modo juego, menos el hecho de que no se comporta fluidamente. No supe como hacer los movimientos de esta forma, por lo que solo usé los sprites que me parecían más atractivos para el juego. Con respecto al modo constructor, este está implementado completa y correctamente. Los detalles sobre requisitos incompletos está más adelante, en la autoevaluación. Es importante mencionar que a grandes rarasgos, la organización de esta tarea consistió en un backend y frontend para CADA VENTANA. Es decir, se separó la ventana de juego en 2, el modo constructor y el del juego en sí. Se prefirió hacer de esta manera por el orden y porque se encontraba permitido, tal como se explica en la issue 292 de la tarea.>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item:
- ❌  **NO** se completó lo pedido
- ✅ se completastó **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores


#### Ventanas: 27 pts (27%) ✅ 
##### Ventana de Inicio ✅ 
<Se visualiza correctamente todos los elementos pedidos.>

##### Ventana de Juego ✅ 
<Se visualizan correctamente los elementos mínimos y no se superponen. Las estadísticas se van actualizando. Se logra carga de mapa o modo constructor dependiendo de elección. El panel de construcción contiene todas las entidades. El panel de construcción señala cuántos elementos de cada entidad van quedando a medida que se ubican. Si uno llega a 0, no se puede volver a poner. El juego inicia cuando se presiona el botón jugar si es que ya se ubicó Luigi y la estrella. El botón salir aparece solo si termina el juego, pues no se pide que el modo constructor tenga uno.>

#### Mecánicas de juego: 47 pts (47%) ✅ 
##### Luigi ✅ 
<Luigi tiene todas las funcionalidades de la pauta.>

##### Fantasmas ✅ 
<Los tienen todas las funcionalidades descritas en la distribución del puntaje (los fantasmas no chocan entre sí, los fantasmas verticales y horizontales se mueven con sus respectivas velocidades aleatorias, se implementan características de ambos tipos, como que el chocar con un fuego los elimina o sus choques). Es importante mencionar que se decidió que los fantasmas horizontales se moverán con una velocidad aleatoria, mientras que los verticales con otra. Esto definiendo la característica como un atributo de clase. En el issue 375 se indica que hay flexibilidad en cuanto a este aspecto, pues el enunciado no lo especifica.>

##### Modo Constructor ✅ 
<No se puede superponer bloques. Hay límites de elementos a ubicar por entidad. Ningún sprite se mueve. Al presionar jugar se verifican las condiciones pertinentes para empezar. Si no se cumplen, simplemente no se parte. En caso contrario inicia el modo juego.>

##### Fin de ronda ✅ 
<Se calcula correctamente el puntaje al terminar la partida (importante decir que se usan redondeos para no mostrar decimales). Se implementan las 3 formas de terminar la partida. Al terminar se indican puntaje, resultado y nombre del usuario. Además suena el sonido pertinente.  También aparece el botón de salir cuando el programa termina.>

#### Interacción con el usuario: 14 pts (14%) 🟠 
##### Clicks ✅ 
<El modo constructor es implementado completamente y correctamente con el click izquierdo.>

##### Animaciones ❌ 
<El movimiento del mapa no es fluido.>

#### Funcionalidades con el teclado: 8 pts (8%) 🟠 
##### Pausa ✅ 
<La pausa está implementada tanto con el botón p como el botón pausa de la ventana.>

##### K + I + L ✅ 
<Al presionar esta combinación de letras, desaparecen todos los fantasmas.>

##### I + N + F ❌ 
<No se implementó el modo invencible de Luigi.>

#### Archivos: 4 pts (4%) 🟠 
##### Sprites 🟠 
<No se usaron todos los archivos, pues no se hizo el juego fluido. Se utilizaron los considerados estéticamente apropiados para los personajes. Por otro lado, se importaron correctamente todos los elementos y el fondo.>

##### Parametros.py ✅ 
<Se cumple lo expuesto en la distribución del puntaje.>

#### Bonus: 8 décimas máximo ❌ 
##### Volver a Jugar ✅ 
##### Follower Villain ❌ 
##### Drag and Drop ❌ 

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Adicionalmente se crearon los siguientes archivos en el directorio (se abren los siguientes archivos con la tarea):

1. ```Backend```: Contiene todos los archivos python asociados a la lógica de las ventanas.
2. ```log_constructor.py``` en ```Backend```: Módulo asociado al backend de la ventana constructor.
3. ```log_inicio.py``` en ```Backend```: Módulo asociado al backend de la ventana inicio.
4. ```logica_juego.py``` en ```Backend```: Módulo asociado al backend de la ventana de juego.
5. ```Frontend```: Contiene todos los archivos python asociados a la visualización de las ventanas.
6. ```ventana_inicio.py``` en ```Frontend```: Módulo asociado al frontend de la ventana inicio.
7. ```ventana_juego.py``` en ```Frontend```: Módulo asociado al frontend de la ventana del juego.


## Librerías 
### Librerías externas utilizadas
Mi tarea está hecha principalmente con PyQt5 (debe instalarse):

1. ```PyQt5.QtCore```: ```pyqtSignal```, ```QObject```, ```QTimer```, ```Qt```, ```QUrl```
2. ```PyQt5.QtWidgets```: ```QWidget```, ```QLabel```, ```QPushButton```, ```QDesktopWidget```, ```QHBoxLayout```, ```QVBoxLayout```, 
```QGridLayout```, ```QComboBox```, ```QLineEdit```, ```QApplication```
3. ```PyQt5.QtGui```: ```QPixmap```, ```QIcon```
4. ```os```: ```path```, ```listdir```
5. ```PyQt5.QtMultimedia```: ```QSoundEffect```
6. ```random```: ```uniform```
6. ```sys```: ```exit```
6. ```string```: ```ascii_letters```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```log_constructor```: Contiene a ```ModoConstructor``` (lógica del modo constructor)
2. ```log_inicio```: Contiene a ```VentanaInicioBackend``` (lógica de ventana de inicio)
3. ```logica_juego```: Contiene a ```Juego``` (lógica del juego)
4. ```ventana_constructor```: Contiene a ```VentanaConstructor``` (visualización de ventana constructor)
5. ```ventana_inicio```: Contiene a ```VentanaInicio``` (visualización de ventana inicio)
6. ```ventana_juego```: Contiene a ```VentanaJuego``` (visualización de ventana inicio)
7. ```entidades```: Contiene a ```Luigi```, ```FantasmaHorizontal```, ```FantasmaVertical```, ```Pared```, ```Roca```, ```Fuego```. Son las clases para definir a los elementos del juego. 
8. ```parametros```: Contiene todos los parámetros utilizados para la creación del juego.



## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Supuse que no afectaba la forma aleatoria escogida en que se mueven los fantasmas. Esto es válido ya que en ninguna parte del enunciado se especifica y es necesario escoger el criterio para el movimiento de estos personajes, pues si no se hubiese hecho no habría habido claridad sobre la mecánica del juego./a> 
2. <Con respecto a la superposición de posibles sprites en el modo juego (por ejemplo, el caso de que 2 fantasmas usen el mismo espacio o que Luigi se ponga sobre la estrella), solo se mostrará uno de los sprites. Esto es importante de definir para que haya claridad en cuanto a la mecánica de la ventana de juego. Cabe destacar que si Luigi se ubica en la posición de la estrella, la estrella no se verá, solo Luigi. Esto porque Luigi es el personaje que está controlando el usuario, por lo que se debería ver en todo momento./a>
3. <Si bien se podía crear un solo módulo para la ventana de juego, la quise separar en dos. Para el modo constructor y el flujo del juego en sí. Lo quise hacer porque de esta forma pude ordenar de mejor manera el código entre Frontend y Backend./a>
4. <Al final del juego, en vez de poner toda la ventana en negro, quise simplemente esconder los sprites. Se me hizo más simple de esta manera con el código de actualización de grillas que en su momento ya había creado./a>
5. <El movimiento de rocas solo se efectúa si no hay otro elemento en la casilla de destino. Importante para definir el movimiento de Luigi./a>

PD: <No alcancé a producir la animación en el juego. Me quise enfocar en criterios más relevantes para la correción. >


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://stackoverflow.com/questions/44707794/pyqt-combo-box-change-value-of-a-label>: el comando que aparece en la siguiente página permite que el cambiar el texto escogido esté conectado a una función. Está implementado en el archivo ventana_constructor.py en las líneas 31 a 35. Cuando se cambia la elección para de QBox asociado a los elementos que se puede poner, se activa el método filtrar, que luego de un flujo hace que algunos botones asociados los elementos aparezcan o desaparezcan.>
2. \<http://localhost:8929/lab/tree/frontend>: la lógica utilizada para armar los botones del control remoto del siguiente enlace fue usada para la creación de la grilla del modo constructor. Cada casilla es un botón distinto que manda como señal su posición. Está implementado en el archivo ventana_constructor.py en las líneas 82 a 114 y 228 a 286. El código mostrado en el material del curso permite diferenciar los botones de las casillas.>
3. \<https://stackoverflow.com/questions/47226092/how-to-set-qpushbutton-size-in-qgridlayout-in-qt>: si bien este link de ayuda es de otro leguaje de programación, el comando setSpacing() me ayudó a disminuir el espacio entre casillas de las grillas tanto en ventana_constructor.py y ventana_juego.py. Está implementado en el archivo ventana_constructor.py en las líneas 302 a 319 y en ventana_juego.py de las líneas 69 a 88.>
4. \<https://stackoverflow.com/questions/5899826/pyqt-how-to-remove-a-widget>: se encuentran presentes comandos para remover widgets a la hora de tener que actualizar las grillas. Está implementado en el archivo ventana_constructor.py en las líneas 81 a 117 y en ventana_juego.py en las líneas 228 a 286.>
5. \<https://www.youtube.com/watch?v=LJTdqNeQY50>: se encuentra presente el comando itemAtPosition que permite iterar sobre grillas y luego y actualizarlas. Está implementado en el archivo ventana_constructor.py de las lineas 302 a 308 y en ventana_juego.py de las lineas 193 a 251.>
6. \<https://stackoverflow.com/questions/70171022/multiple-key-register-event-pyqt5>: comando para detectar la presión de varias teclas a la vez. Usado en ventana_juego.py en las líneas 345 a 349.>
7. \<https://stackoverflow.com/questions/62579096/reduce-spacing-in-pyqt5-gridlayout-between-the-widgets>: Otro uso del comando setSpacing(). Me ayudó a comprender de mejor manera el método. Sirve para disminuir el espacio entre casillas de las grillas tanto en ventana_constructor.py y ventana_juego.py. Está implementado en el archivo ventana_constructor.py en las líneas 302 a 319 y en ventana_juego.py, igual que en el enlace (3.).>