#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Proyecto Laboratorio Algoritmos 1 Sep-Dic 2016

# Descripcion: "Solitaire Chess" es un juego de ingenio y logica, esta basado en el juego de ajedrez tradicional
# pero este es de un solo jugador. El tablero es de un cuarto de tamano del tablero original y el objetivo del juego
# es dejar el tablero con solo una pieza. Las piezas son las del ajedrez original y se comportan de la misma manera.
# Este proyecto consiste en la implementacion del juego.

# Autores:
# 	German Robayo e Ian Goldberg

# Aspectos a revisar: * Prints líneas 90, 102
# 					  * Correccion: Postcondicion: c<=10 and c>0
# 					  * Variable j no declarada y usada en la línea 264, c en la línea 346, i_beg, j_beg, i_end, j_end de la línea 374 
# 						a la 377.
		
# Modificaciones:

# Fecha	    Modificacion

# 23-11-16  * Creacion del videojuego

# 24-11-16  * Adicion de las funciones obtenerPosicionMouse() (linea 164), get_key() (linea 98),
#			  display_box() (linea 117) y ask() (linea 133). Creacion de la pantalla para ingresar 
#			  el nombre del jugador. Creacion del Menu Principal y del menu secundario "Nueva Partida"

# 27-11-16  * Optimizacion de codigo, eliminacion de funciones que no se usaban, adicion de las funciones:
#			  cuadroCentrado(), cuadroALaIzq(), escribeUsuario() y cierraJuego(). Finalizacion de la ptablero_finaltablero_finalantalla
#			  de ingreso de datos de parte del usuario y de la pantalla de menu principal. Retoque de la pantalla
#			  principal, ahora cuando el jugador selecciona opciones no disponibles aparece el recuadro adecuado.

# 29-11-16  * Creacion de la pantalla de modo de carga y pantalla de configuracion. Anadimos lo tableros por defecto.
#			  Creacion del archivo de partidas por defecto y de la funcion de crear un tablero personalizado.Creacion 
#			  de las funciones inicializaTablero y llenaTablero, falta acomodar llenaTablero. Ya acepta mayusculas

# 01-12-16  * Creacion del temporizador, creacion de la funcion que monta las piezas en el tablero.

# 09-12-16  * Ya el juego salva partidas, falta hacer que las cargue. El boton de pausa es un poco problematico, hay que cambiar la manera en 
#			  que hice el tiempo

# 11-12-16  * Ya el juego carga partidas. La funcion movimientosDisponibles() ya funciona de manera adecuada. El boton de pausa ya funciona a la
#			  perfeccion.

# 12-12-16  * Ya el juego esta listo. Se estan haciendo ahora las animaciones. La funcion movimientosDisponibles() fue dividida en subfunciones para
#			  cada pieza. Faltan sonidos, animaciones y backgrounds.

# NOTA IMPORTANTE: Si la computadora en la que se ejecute este codigo no tiene instalada pygame, soltara error
# NOTA IMPORTANTE: Si la computadora en la que se ejecute este codigo es de gama baja, puede que se experimenten bajones de fps. Sobre todo 
# 				   en la pantalla de partida se notara que el tiempo va a ir un poco mas lento de lo normal.


#Declaracion de varibles:

import pygame, sys, datetime, time, random
from pygame.locals import *
import pygame.font

pygame.init()
pygame.font.init()

# Variables iniciales:

FPS = 20
fpsClock = pygame.time.Clock()
ancho_ventana = 600 # Ancho de la ventana
alto_ventana = 580 # Alto de la ventana
pantalla_principal = False # Para saber si me encuentro en la pantalla principal
ingreso = True # Para saber si el usuario ingreso por primera vez al programa
pantalla_pnueva = False # Para saber si el usuario se encuentra en la pantalla "partida nueva"
pantalla_pcarga =False # Para saber si el usuario se encuentra en la pantalla "cargar partida"
pantalla_records = False # Para saber si el usuario se encuentra en la pantalla "records"
pantalla_mcarga = False # Para saber si el usuariose encuentra en la pantalla "modo de carga"
cargar_disponible = False # Para saber si es posible entrar al menu de carga de partida.
records_disponible = False # Para saber si es posible entrar al menu de records
pantalla_tablero = False # Para saber si el usuario se encuentra en la pantalla de "tablero".
pantalla_configuracion = False # Para saber si el usuario se encuentra en la pantalla de configuracion de tablero.
pantalla_juego = False # Para saber si el usuario se encuentra en la pantalla de juego
tablero_final = [[None, None, None, None],\
				 [None, None, None, None],\
				 [None, None, None, None],\
				 [None, None, None, None]] # Arreglo que contenera cada pieza
n_tablero = 0 # Numero del tablero escogido de la lista de tableros por defecto.
tablero = [] # Tablero escogido para resolver.
tablerosdefecto = [] # Lista de los posibles tableros que trae por defecto el archivo "tablerodefecto.txt".
datos = [] # Variable que almacena datos ingresados por el usuario.
listo = False # Variable que indica cuando el usuario termina de ingresar datos.
muestra_error = False # Variable que indica si el usuario ingresa datos erroneos.


# Colores:
#           R    G    B
marron 	= (139,  69,  19)
negro  	= (0  ,   0,   0)
marfil 	= (255, 228, 181)
blanco 	= (255, 255, 255)
verde  	= (144, 238, 144)
gris   	= (128, 128, 128)
cafe   	= ( 70,  35,   9)
cafe_os	= ( 28,  14,   3)
rojo   	= (255,   0,   0)
azul   	= (  0,   0, 255)
transp  = (255, 255, 255, 0)

# Verificando si hay partidas guardadas:
with open('ArchivosDeTexto/PartidasGuardadas.txt','r+') as f:
	if len(f.readlines())==1:
		color1 = gris
		color2 = blanco
		cargar_disponible = False
	else:
		color1 = negro
		color2 = marfil
		cargar_disponible = True

# Verificando si se hay records existentes:
with open("ArchivosDeTexto/Records.txt") as f:
	if len(f.readlines())==1:
		color3 = gris
		color4 = blanco
		records_disponible = False
	else:
		color3 = negro
		color4 = marfil
		records_disponible = True

# Guardando las configuraciones por defecto:

tablerosdefecto = []
tableros_faciles = []
tableros_dificiles = []
tableros_mdificiles = []
with open('ArchivosDeTexto/tablerosdefecto.txt','r+') as f:
	a = f.readlines()[1:]
	for i in a:
		tablero = i.split('\t')
		if tablero[1] == 'Facil\n':
			# Agregando los tableros faciles a tableros_faciles
			tableros_faciles.append(tablero[0].split('-'))
		elif tablero[1] == 'Dificil\n':
			# Agregando los tableros dificiles a tableros_dificiles
			tableros_dificiles.append(tablero[0].split('-'))
			#tableros_mdificiles.append(tablero[0].split('-'))
		elif tablero[1] == 'Muy Dificil\n':
			tableros_mdificiles.append(tablero[0].split('-'))
		tablerosdefecto.append(tablero[0].split('-'))

# Carga de imagenes:

try:
	# Piezas
	peon    = pygame.image.load('Imagenes/Peon.png')
	alfil   = pygame.image.load('Imagenes/Alfil.png')
	torre   = pygame.image.load('Imagenes/Torre.png')
	caballo = pygame.image.load('Imagenes/Caballo.png')
	rey     = pygame.image.load('Imagenes/Rey.png')
	reina   = pygame.image.load('Imagenes/Reina.png')

	# Botones:

	play     = pygame.image.load('Imagenes/Play.png')
	play     = pygame.transform.smoothscale(play, (80,80))

	pause    = pygame.image.load('Imagenes/Pausa.png')
	pause    = pygame.transform.smoothscale(pause, (80,80))

	terminar = pygame.image.load('Imagenes/Terminar.png')
	terminar = pygame.transform.smoothscale(terminar, (80,80))

	deshacer = pygame.image.load('Imagenes/Deshacer.png')
	deshacer = pygame.transform.smoothscale(deshacer, (80,80))

	pista    = pygame.image.load('Imagenes/Solucion.png')
	pista    = pygame.transform.smoothscale(pista, (80,80))

	# Fondos de Pantalla:

	menu1 = pygame.image.load('Imagenes/Menu1')
	menu1 = pygame.transform.smoothscale(menu1, (ancho_ventana, alto_ventana))

	menu2 = pygame.image.load('Imagenes/Menu2')
	menu2 = pygame.transform.smoothscale(menu2, (ancho_ventana, alto_ventana))

	fondo_tablero = pygame.image.load('Imagenes/Tablero2.0.png')
	fondo_tablero = pygame.transform.smoothscale(fondo_tablero, (ancho_ventana, alto_ventana))

	img_victoria = pygame.image.load('Imagenes/Victoria.jpg')
	img_victoria = pygame.transform.smoothscale(img_victoria, (ancho_ventana, alto_ventana))

	img_derrota = pygame.image.load('Imagenes/Derrota.jpg')
	img_derrota = pygame.transform.smoothscale(img_derrota, (ancho_ventana, alto_ventana))

	puerta = pygame.image.load('Imagenes/Puerta.jpg')
	puerta = pygame.transform.smoothscale(puerta, (ancho_ventana, alto_ventana))

	img_records = pygame.image.load('Imagenes/Telon.jpg')
	img_records = pygame.transform.smoothscale(img_records, (ancho_ventana, alto_ventana))

except:
	print('Revisa que esten todos los archivos. Al parecer hay algunos faltantes')
	cierraJuego()

# Declaracion de Ventana:

ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Solitaire Chess.")


# Descripcion: Funcion que cierra el juego.
# Parametros:
#		ninguno
def cierraJuego():
# Precondicion: True
	pygame.quit()
	sys.exit()
# Postcondicion: True


# Descripcion: Funcion que dibuja un cuadro de texto
# Parametros:
#		mensaje: string con el mensaje a imprimir
#		tamano: tamano de fuente del mensaje
#		x, y: coordenadas del centro del cuadro
#		pantalla: lugar donde se mostrara el texto
#		color_texto: color del texto
#		color_cuadro: color del fondo del cuadro
#		color_borde: color del borde del cuadro
def cuadroCentrado(mensaje, tamano, x, y, pantalla, color_texto, color_cuadro, color_borde):
	try:
		# Precondicion:
		assert(len(mensaje)>=0 and tamano > 0 and x > 0 and y > 0)
		fuente = pygame.font.Font('freesansbold.ttf', tamano)
		texto = fuente.render(mensaje,True, color_texto, color_cuadro)
		cuadro_texto = texto.get_rect()
		cuadro_texto.center = (x, y)
		pygame.draw.rect(ventana, color_borde, (cuadro_texto.left-2, cuadro_texto.top-2,\
		 cuadro_texto.width+4, cuadro_texto.height+4))
		ventana.blit(texto, cuadro_texto)
		return (cuadro_texto.left, cuadro_texto.top, cuadro_texto.width, cuadro_texto.height)
	except AssertionError:
		print("Revise si le paso parametros validos a la funcion cuadroCentrado().")
		cierraJuego()
# Postcondicion: True


# Descripcion: Funcion que dibuja un cuadro de texto donde el usuario ingresara datos
# Parametros:
#		mensaje: string con el mensaje a imprimir
#		tamano: tamano de fuente del mensaje
#		x, y: coordenadas de la esquina superior izquierda
#		pantalla: lugar donde se mostrara el texto
#		color_texto: color del texto
#		color_cuadro: color del fondo del cuadro
#		color_borde: color del borde del cuadro
def cuadroALaIzq(mensaje, tamano, x, y, pantalla, color_texto, color_cuadro, color_borde):
	try:
		# Precondicion:
		assert(len(mensaje)>=0 and tamano > 0 and x > 0 and y > 0)
		fuente = pygame.font.Font('freesansbold.ttf', tamano)
		texto = fuente.render(mensaje,True, color_texto, color_cuadro)
		cuadro_texto = texto.get_rect()
		cuadro_texto.topleft = (x, y)
		pygame.draw.rect(ventana, color_borde, (x-2, y-2,\
		 cuadro_texto.width+4, cuadro_texto.height+4))
		ventana.blit(texto, cuadro_texto)
		#return (cuadro_texto.left, cuadro_texto.top, cuadro_texto.width, cuadro_texto.height
	except:
		print("Revise si le paso parametros validos a la funcion cuadroALaIzq().")
		cierraJuego()
# Postcondicion: True


# Definicion: Funcion que le permite al jugador escribir datos mediante el GUI. Devuelve el string
#			  escrito y True si el jugador presiono ENTER 
# Parametros:
# 		datos: arreglo de caracteres
def escribeJugador(datos):
	try:
		# Precondicion:
		assert(len(datos) >= 0 )
		fine = False
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					datos = datos[0:-1]
				elif event.key == K_RETURN:
					fine = True
				elif event.key <= 127:
					if event.unicode in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm-_1234567890 ":
						datos.append(event.unicode.encode('ascii', 'ignore'))
		return (datos, fine)
	except:
		print("Revise si en la funcion escribeJugador() el arreglo es el adecuado")
		cierraJuego()
# Postcondicion: True


# Descripcion: Funcion que llena una matriz con None
# Parametros:
#		arreglo: arreglo multidimensional que contendra puros None luego de llamar a la funcion 
def inicializarTablero(arreglo):
	try:
		# Precondicion:
		assert(type(arreglo) == list and all(type(arreglo[i]) == list for i in range(4)))
		for i in range(4):
			for j in range(4):
				arreglo[i][j] = None
	except:
		print("Verifique que el arreglo pasado por inicializarTablero() es de las dimensiones y tipos adecuados.")
# Postcondicion: all(arreglo[i][j] == None for i,j in range(4))


# Descripcion: Funcion que llena el tablero con las piezas adecuadas
# Parametros:
#		arreglo: Arreglo multidimensial que contendra las piezas en sus respectivas posiciones
#		config: Arreglo que contiene las posiciones de las piezas
def llenarTablero(arreglo, config):
	j = 0
	try:
		# Precondicion:
		assert(all(type(arreglo[i]) == list for i in range(4)) and type(config) == list)
		for i in range(len(config)):
			if len(config[i]) == 2:
				if config[i][0] == 'a':
					j = 0
				elif config[i][0] == 'b':
					j = 1
				elif config[i][0] == 'c':
					j = 2
				elif config[i][0] == 'd':
					j = 3
				if arreglo[4-int(config[i][1])][j] == None:
					arreglo[ 4-int(config[i][1]) ][ j ] = 'peon'
				else:
					pass
			else:
				if config[i][1] == 'a':
					j = 0
				elif config[i][1] == 'b':
					j = 1
				elif config[i][1] == 'c':
					j = 2
				elif config[i][1] == 'd':
					j = 3
				if arreglo[4-int(config[i][2])][j] == None:
					if config[i][0] == 'A':
						arreglo[ 4-int (config[i][2])][j] = 'alfil'
					elif config[i][0] == 'T':
						arreglo[ 4-int (config[i][2])][j] = 'torre'
					elif config[i][0] == 'C':
						arreglo[ 4-int (config[i][2])][j] = 'caballo'
					elif config[i][0] == 'D':
						arreglo[ 4-int (config[i][2])][j] = 'reina'
					elif config[i][0] == 'R':
						arreglo[ 4-int (config[i][2])][j] = 'rey'
				else:
					pass
	except AssertionError:
		print("Los arreglos pasados a la funcion llenarTablero() no son validos")
		cierraJuego()
# Postcondicion: Que el tablero tenga por lo menos una pieza


# Descripcion: Funcion que dibuja el tablero en pantalla
# Parametros:
#		arreglo: Arreglo multidimensional que contiene las piezas en sus respectivos lugares
def acomodaTablero(arreglo):
	try:
		# Precondicion:
		assert(len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		for i in range(4):
			for j in range(4):
				if arreglo[i][j] == None:
					pass
				else:
					if arreglo[i][j] == 'alfil':
						ventana.blit(alfil, (60+j*80, 85+i*80))
					elif arreglo[i][j] == 'rey':
						ventana.blit(rey, (60+j*80, 85+i*80))
					elif arreglo[i][j] == 'reina':
						ventana.blit(reina, (60+j*80, 85+i*80))
					elif arreglo[i][j] == 'torre':
						ventana.blit(torre, (60+j*80, 85+i*80))
					elif arreglo[i][j] == 'peon':
						ventana.blit(peon, (60+j*80, 85+i*80))
					else:
						ventana.blit(caballo, (60+j*80, 85+i*80))
	except:
		print("Revise que la funcion acomodaTablero() tenga el arreglo adecuado.")
		cierraJuego()
# Postcondicion: Que dibuje todas las piezas de "arreglo"


# Descripcion: Funcion que obtiene la coord numerica de la letra que paso el usuario
# Parametros:
#		coord: string de dos caracteres que contiene la informacion de las coord de las piezas
def obtieneCoordLetra(coord):
	try:
		# Precondicion:
		c = 0
		assert(len(coord) == 2 and coord[0] in "abcd" and coord[1] in "1234")
		if coord[0] == 'a':
			c = 0
		elif coord[0] == 'b':
			c = 1
		elif coord[0] == 'c':
			c = 2
		elif coord[0] == 'd':
			c = 3
		return c
	except AssertionError:
		print("obtieneCoordLetra() nada mas acepta strings de coordenadas")
		raise AssertionError
# Postcondicion: obtieneCoordLetra() == 1 or obtieneCoordLetra() == 2 or \
#					obtieneCoordLetra() == 3 or obtieneCoordLetra() == 0


# Descripcion: Fucion que detecta si hay piezas en las coordenadas indicadas por el usuario.
#			   Define si el movimiento que quiere hacer el usuario es correcto
# Parametros:
#		arreglo: Arreglo que contiene la configuracion actual del tablero
#		coord_beg, coord_end: coordenadas de inicio y fin indicadas por el usuario
def muevePieza(arreglo, coord_beg, coord_end):
	try:
		# Precondicion
		assert(len(arreglo) == 4 and (len(arreglo[i]) == 4 for i in range(4)) and coord_beg[0] in "abcd"\
		 and coord_beg[1] in "1234" and coord_end[0] in "abcd" and coord_end[1] in "1234")
		i_beg = 4 - int(coord_beg[1])
		j_beg = obtieneCoordLetra(coord_beg)
		i_end = 4 - int(coord_end[1])
		j_end = obtieneCoordLetra(coord_end)
		i = 0
		j = 0
		assert(not(i_beg == i_end and j_beg == j_end))
		pieza_1 = arreglo[i_beg][j_beg] 
		pieza_2 = arreglo[i_end][j_end]
		if arreglo[i_beg][j_beg] == None or arreglo[i_end][j_end] == None:
			raise AssertionError

		# Si la pieza escogida es un peon:
		elif arreglo[i_beg][j_beg] == 'peon':
			if (i_end == -1 + i_beg) and ((j_end == 1 + j_beg) or (j_end == j_beg-1)):
				arreglo[i_beg][j_beg] = None
				arreglo[i_end][j_end] = 'peon'
			else:
				raise AssertionError

		# Si la pieza escogida es un alfil:
		elif arreglo[i_beg][j_beg] == 'alfil':

			if j_beg < j_end:
				j = 1
			else:
				j = -1
			if i_beg < j_end:
				i = 1
			else:
				i = -1

			while (i_beg + i != i_end) and (j_beg + j != j_end) and (i + i_beg) in [0,1,2,3] and (j + j_beg) in [0,1,2,3]:
				if arreglo[i_beg + i][j_beg + j] != None:
					raise AssertionError
				i+=i
				j+=j
			else:
				arreglo[i_beg][j_beg] = None
				arreglo[i_end][j_end] = 'alfil'


		# Si la pieza escogida es una torre
		elif arreglo[i_beg][j_beg] == 'torre':

			if i_end == i_beg:
				
				if j_beg < j_end:
					j = 1
				else:
					j = -1
				i = 0

				while (j_beg + j != j_end) and (j + j_beg) in [0,1,2,3]:
					if arreglo[i_beg + i][j_beg + j] != None:
						raise AssertionError
					j += j
				else:
					arreglo[i_beg][j_beg] = None
					arreglo[i_end][j_end] = 'torre'
			
			elif j_end == j_beg:
				
				if i_beg < i_end:
					i = 1
				else:
					i = -1
				j = 0

				while (i_beg + i != i_end) and (i + i_beg) in [0,1,2,3]:
					if arreglo[i_beg + i][j_beg + j] != None:
						raise AssertionError
					i += i
				else:
					arreglo[i_beg][j_beg] = None
					arreglo[i_end][j_end] = 'torre'

			else:
				raise AssertionError


			while (i_beg + i != i_end) and (j_beg + j != j_end) and (i + i_beg) in [0,1,2,3] and (j + j_beg) in [0,1,2,3]:
				if arreglo[i_beg + i][j_beg + j] != None:
					raise AssertionError
				i += i
				j += j
			else:
				arreglo[i_beg][j_beg] = None
				arreglo[i_end][j_end] = 'torre'

		# Si la pieza escogida es un rey
		elif arreglo[i_beg][j_beg] == 'rey':
			if (((i_end == i_beg + 1) or (i_end == i_beg - 1)) and j_beg == j_end) or \
			(((i_end == i_beg + 1) or (i_end == i_beg - 1)) and ((j_end == j_beg + 1) or (j_end == j_beg - 1))) or \
			(((j_end == j_beg + 1) or (j_end == j_beg - 1)) and i_end == i_beg):
				arreglo[i_beg][j_beg] = None
				arreglo[i_end][j_end] = 'rey'
			else:
				raise AssertionError

		# Si la pieza escogida es una reina
		elif arreglo[i_beg][j_beg] == 'reina':

			if i_end == i_beg:
			
				if j_beg < j_end:
					j = 1
				else:
					j = -1
				i = 0

				while (j_beg + j != j_end) and (j + j_beg) in [0,1,2,3]:
					if arreglo[i_beg + i][j_beg + j] != None:
						raise AssertionError
					j += j
				else:
					arreglo[i_beg][j_beg] = None
					arreglo[i_end][j_end] = 'reina'
			
			elif j_end == j_beg:
				
				if i_beg < i_end:
					i = 1
				else:
					i = -1
				j = 0

				while (i_beg + i != i_end) and (i + i_beg) in [0,1,2,3]:
					if arreglo[i_beg + i][j_beg + j] != None:
						raise AssertionError
					i += i
				else:
					arreglo[i_beg][j_beg] = None
					arreglo[i_end][j_end] = 'reina'

			else:
				if j_beg < j_end:
					j = 1
				else:
					j = -1
				if i_beg < j_end:
					i = 1
				else:
					i = -1

				while (i_beg + i != i_end) and (j_beg + j != j_end) and (i + i_beg) in [0,1,2,3] and (j + j_beg) in [0,1,2,3]:
					if arreglo[i_beg + i][j_beg + j] != None:
						raise AssertionError
					i+=i
					j+=j
				else:
					arreglo[i_beg][j_beg] = None
					arreglo[i_end][j_end] = 'reina'

		# Si la pieza escogida es un caballo
		elif arreglo[i_beg][j_beg] == 'caballo':

			if (abs(i_end - i_beg )+1)*(abs(j_end - j_beg)+1) == 6:
				arreglo[i_beg][j_beg] = None
				arreglo[i_end][j_end] = 'caballo'
			else:
				raise AssertionError
		
		return pieza_1, pieza_2
	except AssertionError:
		print("Verifique que los parametros pasados sean los adecuados.")
		raise AssertionError
# Postcondicion: arreglo[i_beg][j_beg] == None and (arreglo[i_end][j_end] == 'peon' or arreglo[i_end][j_end] == 'alfil'
#				or arreglo[i_end][j_end] == 'torre' or arreglo[i_end][j_end] == 'rey' or arreglo[i_end][j_end] == 'reina'
#				or arreglo[i_end][j_end] == 'caballo')


# Descripcion: Funcion que cuenta las piezas actuales en el tablero
# Parametros: 
#		arreglo: arreglo multidimensional que contiene las piezas actuales
def contadorPiezas(arreglo):
	try:
		c = 0
		assert(len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		for i in range(4):
			for j in range(4):
				if arreglo[i][j] != None:
					c+=1
		return c
	except AssertionError:
		print("Revisa que el arreglo en contadorPiezas() sea el adecuado.")
		cierraJuego()
# Postcondicion: c<11 and c>0


# Descripcion: Funcion que hace que el usuario no escriba.
# Parametros:
#		ninguno
def noEscribe():
# Precondicion: True
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			pass
# Postcondicion: True


# Descripcion: Funcion que verifica los movimientos disponibles para el Alfil
# Parametros:
#		i,j: Posicion de la pieza en el arreglo
#		arreglo: Arreglo multidimensional que contiene las piezas del tablero
def movimientosAlfil(i, j, arreglo):
	try:
		# Precondicion:
		assert(i in [0,1,2,3] and j in [0,1,2,3] and len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		try:
			for k in range(1,4):
				if arreglo[i + k][j - k] != None:
					if j - k < 0:
						raise AssertionError
					return (True, i, j , i + k, j - k)
				else:
					continue
			else:
				raise AssertionError
		except:
			try:
				for k in range(1,4):
					if arreglo[i + k][j + k] != None:
						return (True, i, j , i + k, j + k)
					else:
						continue
				else:
					raise AssertionError
			except:
				try:
					for k in range(1,4):
						if arreglo[i - k][j - k] != None:
							if i - k < 0 or j - k < 0:
								raise AssertionError
							return (True, i, j , i - k, j - k)
						else:
							continue
					else:
						raise AssertionError
				except:
					try:
						for k in range(1,4):
							if arreglo[i - k][j + k] != None:
								if i - k < 0:
									raise AssertionError
								return (True, i, j , i - k, j + k)
							else:
								continue
						else:
							raise AssertionError
					except:
						return None
	except:
		pass
# Postcondicion: True


# Descripcion: Funcion que verifica los movimientos disponibles para la Torre
# Parametros:
#		i,j: Posicion de la pieza en el arreglo
#		arreglo: Arreglo multidimensionla que contiene las piezas del tablero
def movimientosTorre(i,j,arreglo):
	try:
		# Precondicion:
		assert(i in [0,1,2,3] and j in [0,1,2,3] and len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		try:
			for k in range(1,4):
				if arreglo[i + k][j] != None:
					return (True, i, j , i + k, j)
				else:
					continue
			else:
				raise AssertionError
		except:
			try:
				for k in range(1,4):
					if arreglo[i - k][j] != None:
						if i - k < 0:
							raise AssertionError
						return (True, i, j , i - k, j)
					else:
						continue
				else:
					raise AssertionError
			except:
				try:
					for k in range(1,4):
						if arreglo[i][j + k] != None:
							return (True, i, j , i, j + k)
						else:
							continue
					else:
						raise AssertionError
				except:
					try:
						for k in range(1,4):
							if arreglo[i][j - k] != None:
								if j - k < 0:
									raise AssertionError
								return (True, i, j , i, j - k)
							else:
								continue
						else:
							raise AssertionError
					except:
						return None
	except:
		pass
# Postcondicion: True


# Descripcion: Funcion que verifica los movimientos disponibles para el Rey
# Parametros:
#		i,j: Posicion de la pieza en el arreglo
#		arreglo: Arreglo multidimensional que contiene las piezas del tablero
def movimientosRey(i,j,arreglo):
	try:
		# Precondicion:
		assert(i in [0,1,2,3] and j in [0,1,2,3] and len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		try:
			if arreglo[i + 1][j] != None:
				return (True, i, j , i + 1, j)
			else:
				raise AssertionError
		except:
			try:
				if arreglo[i - 1][j] != None:
					if i - 1 < 0:
						raise AssertionError
					return (True, i, j , i - 1, j)
				else:
					raise AssertionError
			except:
				try:
					if arreglo[i][j + 1] != None:
						return (True, i, j , i, j + 1)
					else:
						raise AssertionError
				except:
					try:
						if arreglo[i][j - 1] != None:
							if j - 1 < 0:
								raise AssertionError
							return (True, i, j , i, j - 1)
						else:
							raise AssertionError
					except:
						try:
							if arreglo[i + 1][j + 1] != None:
								return (True, i, j , i + 1, j + 1)
							else:
								raise AssertionError
						except:
							try:
								if arreglo[i + 1][j - 1] != None:
									if i - 1 < 0:
										raise AssertionError
									return (True, i, j , i + 1, j - 1)
								else:
									raise AssertionError
							except:
								try:
									if arreglo[i - 1][j - 1] != None:
										if i - 1 < 0 or j - 1 < 0:
											raise AssertionError
										return (True, i, j , i - 1, j - 1)
									else:
										raise AssertionError
								except:
									try:
										if arreglo[i - 1][j + 1] != None:
											if i - 1 < 0:
												raise AssertionError
											return (True, i, j , i - 1, j + 1)
										else:
											raise AssertionError
									except:
										return None
	except:
		pass
# Postcondicion: True


# Descripcion: Funcion que verifica los movimientos disponibles para la Reina
# Parametros:
#		i,j: Posicion de la pieza en el arreglo
#		arreglo: Arreglo multidimensional que contiene las piezas del tablero
def movimientosReina(i,j,arreglo):
	try:
		# Precondicion:
		assert(i in [0,1,2,3] and j in [0,1,2,3] and len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		try:
			for k in range(1,4):
				if arreglo[i + k][j] != None:
					return (True, i, j , i + k, j)
				else:
					continue
			else:
				raise AssertionError
		except:
			try:
				for k in range(1,4):
					if arreglo[i - k][j] != None:
						if i - k < 0:
							raise AssertionError
						return (True, i, j , i - k, j)
					else:
						continue
				else:
					raise AssertionError
			except:
				try:
					for k in range(1,4):
						if arreglo[i][j + k] != None:
							return (True, i, j , i, j + k)
						else:
							continue
					else:
						raise AssertionError
				except:
					try:
						for k in range(1,4):
							if arreglo[i][j - k] != None:
								if j - k < 0:
									raise AssertionError
								return (True, i, j , i, j - k)
							else:
								continue
						else:
							raise AssertionError
					except:
						try:
							for k in range(1,4):
								if arreglo[i + k][j + k] != None:
									return (True, i, j , i + k, j + k)
								else:
									continue
							else:
								raise AssertionError
						except:
							try:
								for k in range(1,4):
									if arreglo[i + k][j - k] != None:
										if j - k < 0:
											raise AssertionError
										return (True, i, j , i + k, j - k)
									else:
										continue
								else:
									raise AssertionError
							except:
								try:
									for k in range(1,4):
										if arreglo[i - k][j - k] != None:
											if i - k < 0 or j - k < 0:
												raise AssertionError
											return (True, i, j , i - k, j - k)
										else:
											continue
									else:
										raise AssertionError
								except:
									try:
										for k in range(1,4):
											if arreglo[i - k][j + k] != None:
												if i - k < 0:
													raise AssertionError
												return (True, i, j , i - k, j + k)
											else:
												continue
										else:
											raise AssertionError
									except:
										return None
	except:
		pass
# Postcondicion: True


# Descripcion: Funcion que verifica los movimientos disponibles para el Peon
# Parametros:
#		i,j: Posicion de la pieza en el arreglo
#		arreglo: Arreglo multidimensional que contiene las piezas del tablero
def movimientosPeon(i, j, arreglo):
	try:
		# Precondicion:
		assert(i in [0,1,2,3] and j in [0,1,2,3] and len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		try: 
			if arreglo[i - 1][j - 1] != None:
				if i - 1 < 0 or j - 1 < 0:
					raise AssertionError
				return (True, i, j , i - 1, j - 1)
			else:
				raise AssertionError
		except:
			try:
				if arreglo[i - 1][j + 1] != None:
					if i - 1 < 0:
						raise AssertionError
					return (True, i, j , i - 1, j + 1)
				else:
					raise AssertionError
			except:
				return None
	except:
		pass
# Postcondicion: True


# Descripcion: Funcion que verifica los movimientos disponibles para el Caballo
# Paraetros:
#		i,j: Posicion de la pieza en el arreglo
#		arreglo: Arreglo multidimensional que contiene las piezas del tablero
def movimientosCaballo(i, j, arreglo):
	try:
		# Precondicion:
		assert(i in [0,1,2,3] and j in [0,1,2,3] and len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		try:
			if arreglo[i + 1][j + 2] != None:
				return (True, i, j , i + 1, j + 2)
			else:
				raise AssertionError
		except:
			try:
				if arreglo[i - 1][j + 2] != None:
					if i - 1 < 0:
						raise AssertionError
					return (True, i, j , i - 1, j + 2)
				else:
					raise AssertionError
			except:
				try:
					if arreglo[i + 1][j - 2] != None:
						if j - 2 < 0:
							raise AssertionError
						return (True, i, j , i + 1, j - 2)
					else:
						raise AssertionError
				except:
					try:
						if arreglo[i - 1][j - 2] != None:
							if i - 1 < 0 or j - 2 < 0:
								raise AssertionError
							return (True, i, j , i - 1, j - 2)
						else:
							raise AssertionError
					except:
						try:
							if arreglo[i + 2][j + 1] != None:
								return (True, i, j , i + 2, j + 1)

							else:
								raise AssertionError
						except:
							try:
								if arreglo[i + 2][j - 1]!= None:
									if j - 1 < 0:
										raise AssertionError
									return (True, i, j , i + 2, j - 1)
								else:
									raise AssertionError
							except:
								try:
									if arreglo[i - 2][j + 1] != None:
										if i - 2 < 0:
											raise AssertionError
										return (True, i, j , i - 2, j + 1)
									else:
										raise AssertionError
								except:
									try:
										if arreglo[i - 2][j - 1] != None:
											if i - 2 < 0 or j - 1 < 0:
												raise AssertionError
											return (True, i, j , i - 2, j - 1)
										else:
											raise AssertionError
									except:
										return None
	except:
		pass
# Postcondicion: True


# Descripcion: Funcion que verifica que hayan movimientos disponibles.
# Parametros:
#		arreglo: tablero actual
def movimientosDisponibles(arreglo):
	try:
		assert(contadorPiezas(arreglo) >= 2)
		chance = 0
		for i in range(4):
			for j in range(4):
				if arreglo[i][j] == 'alfil':
					chance = movimientosAlfil(i, j, arreglo)
					if chance == None:
						continue
					else:
						return chance
				elif arreglo[i][j] == 'torre':
					chance = movimientosTorre(i, j, arreglo)
					if chance == None:
						continue
					else:
						return chance
				elif arreglo[i][j] == 'rey':
					chance = movimientosRey(i, j, arreglo)
					if chance == None:
						continue
					else:
						return chance
				elif arreglo[i][j] == 'reina':
					chance = movimientosReina(i, j, arreglo)
					if chance == None:
						continue
					else:
						return chance
				elif arreglo[i][j] == 'peon':
					chance = movimientosPeon(i, j, arreglo)
					if chance == None:
						continue
					else:
						return chance
				elif arreglo[i][j] == 'caballo':
					chance = movimientosCaballo(i, j, arreglo)
					if chance == None:
						continue
					else:
						return chance
				else:
					continue
		chance = (False, 0, 0, 0, 0)
		return chance
	except:
		pass
# Postcondicion: movimientosDisponibles() in [True, False]


# Descripcion: Funcion que cambia de coordenadas numericas a alfabeticas
# Parametros:
#		x: entero a transformar
def deNumALetra(x):
	try:
		# Precondicion:
		assert(x in [0,1,2,3])
		if x == 0:
			return 'a'
		elif x == 1:
			return 'b'
		elif x == 2:
			return 'c'
		else:
			return 'd'
	except:
		print('Revise que el parametro pasado a deNumALetra(x) sea valido')
		cierraJuego()
# Postcondicion: deNumALetra(x) in ['a','b', 'c', 'd']


# Descripcion: Funcion que guarda el tablero como un string
# Parametros:
#		arreglo: arreglo multidimensional que posee las piezas en sus posiciones respectivas
def guardaTablero(arreglo):
	try:
		config = ''
		# Precondicion
		assert(len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		for i in range(4):
			for j in range(4):
				if arreglo[i][j] == 'alfil':
					config += 'A'+deNumALetra(j)+str(4-i)+'-'
				elif arreglo[i][j] == 'torre':
					config += 'T'+deNumALetra(j)+str(4-i)+'-'
				elif arreglo[i][j] == 'reina':
					config += 'D'+deNumALetra(j)+str(4-i)+'-'
				elif arreglo[i][j] == 'rey':
					config += 'R'+deNumALetra(j)+str(4-i)+'-'
				elif arreglo[i][j] == 'caballo':
					config += 'C'+deNumALetra(j)+str(4-i)+'-'
				elif arreglo[i][j] == 'peon':
					config += deNumALetra(j)+str(4-i)+'-'
		config = config.split('-')
		del(config[len(config)-1])
		config = "-".join(config)
		return config
	except:
		print('Revise que el parametro pasado a la funcion guardaTablero() sea valido.')
		cierraJuego()
# Postcondicion: True


# Descripcion: Funcion que pinta el tablero. 
# Parametros:
#		ninguno
def pintaTablero():
	# Aqui no hay que verificar nada:
	assert(True)
	for i in range(4):
		for j in range(4):
			if (i+j)%2 == 0:
				pygame.draw.rect(ventana, cafe, (i*80+50 ,j*80+75, 80, 80))
			else:
				pygame.draw.rect(ventana, marfil, (i*80+50, j*80+75, 80, 80))
# Postcondicion: True


# Descripcion: Funcion que realiza las animaciones de las piezas.
# Parametros:
#		jugada_cache: jugada que realizo el usuario. Contiene la posicion inicio y fin y las piezas involucradas
def animacionMovimientoPiezas(jugada_cache):
	try:
		assert(jugada_cache != None)
		i_beg = obtieneCoordLetra(jugada_cache[0]) * 80 + 60
		j_beg = (4-int(jugada_cache[0][1])) * 80 + 85
		i_end = obtieneCoordLetra(jugada_cache[1]) * 80 + 60
		j_end = (4-int(jugada_cache[1][1])) * 80 + 85
		x = i_beg
		y = j_beg
		c = 1

		piezas = [peon, alfil, torre, rey, reina, caballo]
		figura = 0
		figura2 = 0

		if jugada_cache[2] == 'peon':
			figura = 0
		elif jugada_cache[2] == 'alfil':
			figura = 1
		elif jugada_cache[2] == 'torre':
			figura = 2
		elif jugada_cache[2] == 'rey':
			figura = 3
		elif jugada_cache[2] == 'reina':
			figura = 4
		elif jugada_cache[2] == 'caballo':
			figura = 5

		if jugada_cache[3] == 'peon':
			figura2 = 0
		elif jugada_cache[3] == 'alfil':
			figura2 = 1
		elif jugada_cache[3] == 'torre':
			figura2 = 2
		elif jugada_cache[3] == 'rey':
			figura2 = 3
		elif jugada_cache[3] == 'reina':
			figura2 = 4
		elif jugada_cache[3] == 'caballo':
			figura2 = 5

		while x != i_end or y != j_end:
			if i_beg < i_end:
				x += 5
			elif i_beg >= i_end:
				x += -5
			x ,y = mueveRecta(x, i_beg, j_beg, i_end, j_end, c)
			pintaTablero()
			acomodaTablero(tablero_final)
			if (4-int(jugada_cache[1][1]) + obtieneCoordLetra(jugada_cache[1]))%2 == 0:
				pygame.draw.rect(ventana, cafe, (i_end - 10, j_end - 10, 80, 80))
			else:
				pygame.draw.rect(ventana, marfil, (i_end - 10, j_end - 10, 80, 80))
			ventana.blit(piezas[figura2], (i_end, j_end))
			ventana.blit(piezas[figura], (x, y))
			pygame.display.flip()
			c += 1
	except:
		print('Revise que el parametro pasado a la funcion animacionMovimientoPiezas() sea el correcto.')
		cierraJuego()
# Postcondicion: True
	

# Descripcion: Funcion que obtiene la ecuacion de una recta a partir de dos puntos. Esta devuelve el valor (x,y)
#			   dependiendo del valor de la pendiente
# Parametros:
#		x: valor que sera la primera coord del punto a averiguar
#		x_beg, y_beg: coordenadas de un punto perteneciente a la recta
#		x_end, y_end: coordenadas de otro punto perteneciente a la recta
def mueveRecta(x, x_beg, y_beg, x_end, y_end, c):
	try:
		# Precondicion:
		assert(x >= 0 and x_beg >= 0 and x_end >= 0 and y_beg >= 0 and y_end >= 0 and x in range(ancho_ventana))
		m = float(y_end - y_beg)/float(x_end - x_beg)
		return x, (m * (x - x_beg) + y_beg)
	except ZeroDivisionError:
		if y_beg < y_end:
			return x_beg, y_beg + c * 5
		else:
			return x_beg, y_beg - c * 5
	except AssertionError:
		print('Revise que la funcion mueveRecta() tenga los parametros adecuados')
		cierraJuego()
# Postcondicion: (m*(x-x_beg) + y_beg) in range(alto_ventana)


# Descripcion: Funcion que da una solucion dependiendo de la posicion de alguna pieza
# Parametros:
#		arreglo: arreglo multidimensional que posee las piezas en sus posiciones respectivas
#		pos1, pos2: caracteres que contienen la posicion de las pieza
def obtenSolucion(pos1, pos2, arreglo):
	try:
		assert(pos1 in ['a','b','c','d'] and pos2 in ['1','2','3','4'] and len(arreglo) == 4 and all(len(arreglo[i]) == 4 for i in range(4)))
		x = 4 - int(pos2)
		y = obtieneCoordLetra(pos1+pos2)
		chance = ''
		if arreglo[x][y] == None:
			return (False, 0, 0, 0, 0)
		else:
			if arreglo[x][y] == 'alfil':
				chance = movimientosAlfil(x, y, arreglo)
			elif arreglo[x][y] == 'torre':
				chance = movimientosTorre(x, y, arreglo)
			elif arreglo[x][y] == 'caballo':
				chance = movimientosCaballo(x, y, arreglo)
			elif arreglo[x][y] == 'reina':
				chance = movimientosReina(x, y, arreglo)
			elif arreglo[x][y] == 'rey':
				chance = movimientosRey(x, y, arreglo)
			elif arreglo[x][y] == 'peon':
				chance = movimientosPeon(x, y, arreglo)
		if chance == None:
			return (False, 0, 0, 0, 0)
		return chance
	except AssertionError:
		raise AssertionError


# Decripcion: Funcion que ordena los elementos de un arreglo de acuerdo a la cantidad de victorias
#      		  y el orden alfabetico del nombre de los usuarios.
# Parametros: arreglo: Arreglo a ordenar, que posee al menos dos elementos, los cuales son listas.
def bubbleSort(arreglo):
	try:
		# Precondicion:
		assert(len(arreglo)>=2)
		arreglo.sort(reverse=True)
		while not all((arreglo[i][1].upper() <= arreglo[i+1][1].upper() and arreglo[i][0]==arreglo[i+1][0]) or arreglo[i][0]!=arreglo[i+1][0] for i in range(len(arreglo)-1)):
			for i in range(len(arreglo)-1):
				if arreglo[i][0]==arreglo[i+1][0]:
					if arreglo[i][1].upper()>arreglo[i+1][1].upper():
						arreglo[i][1], arreglo[i+1][1] = arreglo[i+1][1], arreglo[i][1]
	except:
		pass
# Postcondicion: all((arreglo[i][1].upper() <= arreglo[i+1][1].upper() and arreglo[i][0]==arreglo[i+1][0]) or arreglo[i][0]!=arreglo[i+1][0] for i in range(len(arreglo)-1))


# Descripcion: Funcion principal del juego, realiza todas las acciones.
#			   Depende de las demas funciones para funcionar.
# Parametros: ninguno.
def main():
# Precondicion: True
	global nombre, ancho_ventana, alto_ventana, pantalla_principal, ingreso, pantalla_pnueva
	global pantalla_pcarga, pantalla_records, salir_juego, listo, muestra_error, cargar_disponible, records_disponible
	global tablero, n_tablero, pantalla_configuracion, pantalla_juego, tablero_final, tablero_bool
	global peon, alfil, torre, reina, rey, caballo, pantalla_mcarga, color1, color2, contador, color3, color4
	n_piezas = 0
	nombre = []
	datos = []
	n_peon = 0
	n_rey = 0
	n_caballo = 0
	n_alfil = 0
	n_reina = 0
	n_torre = 0
	jugada_cache = None
	deshacer_disponible = True
	finish = False
	minutero = 1
	segundero = 1
	minuto_ganador = 0
	segundo_ganador = 0
	minutero_pausado = 0
	segundero_pausado = 0
	primera_vez = True
	tiempo_espera = ''
	tablero_vacio = [[None for i in range(4)] for k in range(4)]
	tiempo_pausado = 0
	nueva_entrada = ''
	contador = 0
	archivo = []
	nivel = 0
	jugada = False
	paused = False
	victoria = False
	derrota = False
	contador_victorias = 0
	solucion = False
	muestra_solucion = (False, 0, 0, 0, 0)
	animacion = [False, False]
	while True:
		
		if ingreso:	# Trozo de codigo que se encarga de recibir el nombre del jugador
			# Cuando el usuario presiona enter
			if listo:
				try:
					assert(len(nombre)>=1 and (not all(i==' ' for i in nombre)))
					ingreso = False
					pantalla_principal = True
					listo = False
					tiempo = 0
				except:
					tiempo = time.time()
					while time.time()-tiempo < 2:
						ventana.fill(negro)
						cuadroCentrado(' Al parecer no ingreso ningun nombre. ', 20, ancho_ventana/2, alto_ventana/2, ventana, blanco, negro, blanco)
						pygame.display.flip()
					nombre = []
					listo = False
			else:
				# Ventana de espera por el nombre
				ventana.blit(puerta, (0,0))
				nombre, listo = escribeJugador(nombre)
				cuadroALaIzq(' Ingrese su nombre: '+ "".join(nombre),  20, 50, alto_ventana/2,\
					ventana, blanco,negro, blanco)

		# Trozo de codigo que se encarga de manejar la pantalla principal
		elif pantalla_principal:
			ventana.blit(menu1, (0,0))
			# Ventana de espera mientras el usuario no ingresa ningun dato
			if not listo:
				# Si decide salirse de la partida
				if finish:
					datos, listo = escribeJugador(datos)
					cuadroCentrado(' Seguro que desea salir?(S/N) ', 30, ancho_ventana/2, alto_ventana/2-50,\
					 ventana, negro, marfil, negro)
					cuadroCentrado("".join(datos), 30, ancho_ventana/2, alto_ventana/2, ventana, negro, \
						marfil, negro)
					if muestra_error and time.time() - tiempo < 1.5:
						cuadroCentrado(' Opcion no valida. ', 30, ancho_ventana/2, alto_ventana/2 + 50, \
							ventana, negro, marfil, marfil)			
				# Ventana menu principal
				else:
					
					# Cuadro Titulo
					cuadro_titulo = cuadroCentrado(' Solitaire Chess ', 50, ancho_ventana/2, \
						125, ventana, negro, marfil, negro)
					
					# Cuadro "Nueva Partida"
					cuadro_npartida = cuadroCentrado( ' 1 Nueva Partida ', 35, ancho_ventana/2, \
						250, ventana, negro, marfil, negro)
					
					# Cuadro "Cargar Partida"
					cuadro_cpartida = cuadroCentrado(' 2 Cargar Partida ', 35, ancho_ventana/2, \
						310, ventana, color1, color2, negro)
					
					# Cuadro "Mostrar Records"
					cuadro_records = cuadroCentrado(' 3 Mostrar Records ', 35, ancho_ventana/2, \
						370, ventana, color3, color4, negro)
					
					# Cuadro "Salir del Juego"
					cuadro_salir = cuadroCentrado( ' 4 Salir del Juego ', 35, ancho_ventana/2, \
						430, ventana, negro, marfil, negro)

					# Cuadro de ingreso de dato:
					datos, listo = escribeJugador(datos)
					cuadroCentrado(' Ingrese su opcion: ' + "".join(datos), 20, ancho_ventana/2, 500, ventana,\
					 negro, marfil, negro)


					# Cuadro de error de ingreso de datos:
					if muestra_error and time.time()-tiempo < 1.5:
						if not cargar_disponible:
							cuadroCentrado(' No hay partidas guardadas. ', 15, ancho_ventana/2, 550, \
							ventana, gris, marfil, gris)
						elif not records_disponible:
							cuadroCentrado(' No hay records registrados. ', 15, ancho_ventana/2, 550, \
							ventana, gris, marfil, gris)
						else:
							cuadroCentrado(' Por favor, ingrese una opcion valida. ', 15, ancho_ventana/2, 550, \
								ventana, gris, marfil, gris)
			else:
				try:
					assert (type(datos)==list and len(datos)==1 and ((datos[0] == '2' and cargar_disponible)\
					 or (datos[0] == '3' and records_disponible) or datos[0] in 's4SnN1'))
					if finish:
						if datos[0] in 'sS':
							cierraJuego()
						elif datos[0] in 'Nn':
							finish = False
					elif datos[0] == '1':
						pantalla_pnueva = True
						pantalla_principal = False
					elif datos[0] == '2' and cargar_disponible:
						pantalla_pcarga = True
						pantalla_principal = False
					elif datos[0] == '3' and records_disponible:
						pantalla_records = True
						pantalla_principal = False
						c = 0
						records = []
						with open('ArchivosDeTexto/Records.txt', 'r') as f:
							records = f.readlines()
						records_facil = []
						records_dificil = []
						records_mdificil = []
						for i in range(1, len(records)):
							entrada = records[i].split('\t')
							entrada[0], entrada[1] = entrada[1], entrada[0]
							if entrada[2] == 'Facil\n':
								records_facil.append(entrada)
							elif entrada[2] == 'Dificil\n':
								records_dificil.append(entrada)
							elif entrada[2] == 'Muy Dificil\n':
								records_mdificil.append(entrada)
							else:
								continue
						bubbleSort(records_facil)
						bubbleSort(records_mdificil)
						bubbleSort(records_dificil)
					elif datos[0] == '4':
						finish = True
					tiempo = 0
					muestra_error = False
					listo = False
					datos = []
				except AssertionError:
					tiempo = time.time()
					muestra_error = True
					listo = False
					datos = []

		# Trozo de codigo que se encarga de manejar la pantalla de carga de partidas
		elif pantalla_pcarga:
			ventana.blit(menu1, (0,0))
			# Mientras el usuario no presione enter:
			if not listo:
				pygame.draw.polygon(ventana, negro, ((8, 30), (32, 54), (32,42), (42, 42), (42,18), (32,18), (32, 6)))
				pygame.draw.polygon(ventana, marfil, ((10, 30), (30, 50), (30,40), (40, 40), (40,20), (30,20), (30, 10)))

				# Boton regresar:
				cuadroCentrado(' r.- Regresar ', 15, 95, 28, ventana, negro, marfil, negro)

				# Cuadro: 'Ingrese su archivo'
				cuadroCentrado(' Ingrese el nombre de su archivo ', 30, ancho_ventana/2, 150, ventana, negro, marfil, negro)
				cuadroCentrado(' en formato Partida, Fecha y Dificultad ', 30, ancho_ventana/2, 200, ventana, negro, marfil, negro)
				cuadroCentrado(' ejemplo: 5 9122016 Facil ', 20, ancho_ventana/2, 250, ventana, negro, marfil, negro)
				cuadroCentrado("".join(datos), 20, ancho_ventana/2, 300, ventana, negro, marfil, negro)
				datos, listo = escribeJugador(datos)
				if muestra_error and time.time() - tiempo < 2:
					cuadroCentrado(mensaje, 30, ancho_ventana/2, 300, ventana, negro, marfil, negro)
			
			# Cuando el usuario presiona enter:
			else:
				try:
					# Transformamos el arreglo datos en un string completo y luego lo separamos con sus espacios
					datos = "".join(datos).split(" ")
					assert(datos == ['r'] or (len(datos) == 3 and int(datos[0]) > 0 and len(datos[1]) in range(6,9) and datos[2] in ["Facil", "Dificil"]))
					
					# Si el usuario decide regresar:
					if datos == ['r']:
						pantalla_principal = True
						pantalla_pcarga = False
					# Si ingreso alguna partida:
					else:
						with open('ArchivosDeTexto/PartidasGuardadas.txt', 'r') as f:
							lista_partidas = f.readlines()
							for i in lista_partidas[1:]:
								archivo = i.split("\t")
								if int(archivo[0]) == int(datos[0]):
									if int(archivo[1]) == int(datos[1]):
										if archivo[3] == datos[2]:
											break # Cuando llega a este punto el juego detecto la partida dada por el usuario
							else:
								# Cuando revisa el archivo completo y no consigue nada, levantamos una excepcion para hacerle saber
								# que no existe dicho archivo. Estamos usando ZeroDivisionError por que queremos clasificar los errores
								raise ZeroDivisionError
						# las siguientes 4 lineas se encargan de volver a escribir el archivo sin la partida dada por el usuario
						with open('ArchivosDeTexto/PartidasGuardadas.txt', 'w') as f:
							for partida in lista_partidas:
								if "\t".join(archivo) != partida:
									f.write(partida)
						tiempo_pausado = int(archivo[5]) # Para saber en que tiempo se salvo para cargar la partida en ese tiempo exacto
						tablero = archivo[4].split("-") # Para obtener el tablero
						# Para obtener dificuldad
						if archivo[3] == 'Facil':
							nivel = 1
							minutero_pausado = (-tiempo_pausado/60 + 181)//60
							segundero_pausado = abs((tiempo_pausado/60)%60 - 60)%60
						elif archivo[3] == 'Dificil':
							nivel = 2
							minutero_pausado = (-tiempo_pausado/60+91)//60
							segundero_pausado = (abs(((tiempo_pausado)/60)%60-60)%60-30)%60
						# A partir de aqui es llenar el tablero con la configuracion guardadaa
						inicializarTablero(tablero_final)
						llenarTablero(tablero_final, tablero)
						pantalla_pcarga = False
						pantalla_juego = True
						paused = True
					muestra_error = False
					primera_vez = False
				except ZeroDivisionError:
					# Si no existe el archivo ingresado
					mensaje = ' No existe dicho archivo. '
					muestra_error = True
					tiempo = time.time()
				except AssertionError:
					# Si escribio mal:
					mensaje = ' Nomenclatura Erronea '
					muestra_error = True
					tiempo = time.time()
				datos = []
				listo = False

		# Trozo de codigo que se encarga de manejar la pantalla de mostrar records.
		elif pantalla_records:
			ventana.blit(img_records, (0,0))
			# El siguiente ciclo for tiene como uso detectar cuando se presione cualquier tecla. Cuando ese evento ocurra, se cambia
			# la pantalla de records faciles a dificiles y de dificiles a muy dificiles
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					c += 1
					if c == 3:
						pantalla_records = False
						pantalla_principal = True
			
			#ventana.fill(marron)
			pygame.draw.rect(ventana,negro, (50, 150, 500, 380))
			pygame.draw.rect(ventana, marfil, (70, 170, 460, 340))
			cuadroCentrado(' Presione cualquier tecla para continuar ', 20, ancho_ventana/2, 100, ventana, negro, marfil, negro)
			cuadroCentrado(' Posicion             Nombre            Victorias ', 20, ancho_ventana/2, 185, ventana, negro, marfil, marfil)
			
			# Mostrando los records faciles:
			if c == 0:
				# Si no hay records faciles, se aumenta en 1 el contador para que cambie a los records dificiles.
				if len(records_facil) == 0:
					c += 1
				else:
					cuadroCentrado(' Records Modo Facil ', 30, ancho_ventana/2, 50, ventana, negro, marfil, negro)
					j = 1
					for i in records_facil:
						if j == 9:
							break
						cuadroCentrado(str(j), 20, 145, 180 + (j)*35, ventana, negro, marfil, marfil)
						cuadroCentrado(i[1], 20, 300, 180 + (j)*35, ventana, negro, marfil, marfil)
						cuadroCentrado(i[0], 20, 455, 180 + (j)*35, ventana, negro, marfil, marfil)
						j += 1
			
			# Mostrando los records dificiles:
			elif c == 1:
				# Misma dinamica que en el comentario anterior al anterior
				if len(records_dificil) == 0:
					c += 1
				else:
					cuadroCentrado(' Records Modo Dificil ', 30, ancho_ventana/2, 50, ventana, negro, marfil, negro)
					j = 1
					for i in records_dificil:
						if j == 9:
							break
						cuadroCentrado(str(j), 20, 145, 180 + (j)*35, ventana, negro, marfil, marfil)
						cuadroCentrado(i[1], 20, 300, 180 + (j)*35, ventana, negro, marfil, marfil)
						cuadroCentrado(i[0], 20, 455, 180 + (j)*35, ventana, negro, marfil, marfil)
						j += 1
			
			# Mostrando los records muy dificiles:
			elif c == 2:
				# Si no hay records muy dificiles, se cambia de una vez a la pantalla principal
				if len(records_mdificil) == 0:
					pantalla_records = False
					pantalla_principal = True
				else:
					cuadroCentrado(' Records Modo Muy Dificil ', 30, ancho_ventana/2, 50, ventana, negro, marfil, negro)
					j = 1
					for i in records_mdificil:
						if j == 9:
							break
						cuadroCentrado(str(j), 20, 145, 180 + (j)*35, ventana, negro, marfil, marfil)
						cuadroCentrado(i[1], 20, 300, 180 + (j)*35, ventana, negro, marfil, marfil)
						cuadroCentrado(i[0], 20, 455, 180 + (j)*35, ventana, negro, marfil, marfil)
						j += 1

		# Trozo de codigo que se encarga de manejar la pantalla de partida nueva, eligir las dificultades, etc
		elif pantalla_pnueva:
			ventana.blit(menu2, (0,0))
			# Si el usuario no ha presionado enter:
			if not listo:
				pygame.draw.polygon(ventana, negro, ((8, 30), (32, 54), (32,42), (42, 42), (42,18), (32,18), (32, 6)))
				pygame.draw.polygon(ventana, marfil, ((10, 30), (30, 50), (30,40), (40, 40), (40,20), (30,20), (30, 10)))
				
				# Boton regresar:
				cuadro_regresar = cuadroCentrado(' r.- Regresar ', 15, 95, 28, ventana, negro, marfil, negro)
				
				# Cuadro "Elija el modo de juego:"
				cuadro_modo = cuadroCentrado(' Modos de juego: ', 40, ancho_ventana/2, 150,\
				 ventana, negro, marfil, negro)
				
				# Boton "Facil":
				cuadro_facil = cuadroCentrado(' 1.- Facil ', 40, ancho_ventana/2, alto_ventana/2-50\
					, ventana, negro, marfil, negro)
				
				# Boton "Dificil":
				cuadro_dificil = cuadroCentrado(' 2.- Dificil ', 40, ancho_ventana/2, alto_ventana/2 + 10\
					,ventana, negro , marfil, negro)

				# Boton "Muy Dificil":
				cuadro_mdificil = cuadroCentrado(' 3.- Muy Dificil ', 40, ancho_ventana/2, alto_ventana/2 +70\
					, ventana, negro, marfil,negro)
				
				# Boton "Entrenamiento"
				cuadro_entren = cuadroCentrado(' 4.- Entrenamiento ', 40, ancho_ventana/2, alto_ventana/2 +130\
					,ventana, negro, marfil, negro)

				# Cuadro de ingreso de datos:
				datos, listo = escribeJugador(datos)
				cuadroCentrado(' Ingrese su opcion: ' + "".join(datos), 20, ancho_ventana/2, 500, ventana,\
					 negro, marfil, negro)

				if muestra_error and time.time()-tiempo < 1.5:
					cuadroCentrado(' Opcion no valida. ', 20, ancho_ventana/2, 550, ventana,\
						negro, marfil, negro)
			else:
				try:
					assert(len(datos) == 1 and (datos[0] == '1' or datos[0] == '2' or datos[0] == '3' or datos[0] == '4'\
						or datos[0]=='r'))
					
					# El usuario escogio nivel facil:
					if datos[0] == '1':
						pantalla_mcarga = True
						nivel = 1
						tiempo_espera = '3:00'
					
					# El usuario escogio nivel dificil:
					elif datos[0] == '2':
						pantalla_mcarga = True
						nivel = 2
						tiempo_espera = '1:30'
					
					# El usuario escogio nivel muy dificil:
					elif datos[0] == '3':
						nivel = 3
						pantalla_juego = True
						posibles_tableros = tableros_mdificiles # Copio la lista de tableros_mdificiles
						tableros = []   # Lista de tableros que se jugaran en modo muy dificil
						for i in range(3):
							n_tablero = random.randint(0,len(posibles_tableros)-1) # obtengo un numero entero entre 0 y a longitud de la lista posibles_tableros
							tableros.append(posibles_tableros[n_tablero]) # Le agrego a tableros el elemento n_tablero de la lista posibles tableros
							del(posibles_tableros[n_tablero]) # Lo elimino para que no vuelva a aparecer despues
						inicializarTablero(tablero_final)
						llenarTablero(tablero_final, tableros[0])
						del(tableros[0])
						tiempo_espera = '2:00'
						primera_vez = True
						contador_victorias = 0
					
					# El usuario escogio regresar a la pantalla principal
					elif datos[0] == 'r':
						pantalla_principal = True
					
					# El usuario escogio el modo entrenamiento:
					elif datos[0] == '4':
						nivel = 4
						pantalla_mcarga = True
					listo = False
					pantalla_pnueva = False
					muestra_error = False
					datos = []
					jugada = False
				except AssertionError:
					muestra_error = True
					tiempo = time.time()
					listo = False
					datos = []
		
		# Trozo de codigo que se encarga de manejar 
		elif pantalla_mcarga:
			ventana.blit(menu2, (0,0))
			# Si el usuario no ha presionado enter:
			if not listo:
				pygame.draw.polygon(ventana, negro, ((8, 30), (32, 54), (32,42), (42, 42), (42,18), (32,18), (32, 6)))
				pygame.draw.polygon(ventana, marfil, ((10, 30), (30, 50), (30,40), (40, 40), (40,20), (30,20), (30, 10)))
				
				# Boton regresar:
				cuadroCentrado(' r.- Regresar ', 15, 95, 28, ventana, negro, marfil, negro)


				# Cuadro "Elija modo de carga":
				cuadroCentrado(' Elija el modo de carga: ', 40, ancho_ventana/2, 150, ventana, negro, marfil, negro)

				# Cuadro "Modo aleatorio":
				cuadroCentrado(' 1.- Modo Aleatorio ', 35, ancho_ventana/2, alto_ventana/2 - 25, ventana, negro, marfil,\
					negro)

				# Cuadro "Modo Personalizado":
				cuadroCentrado(' 2.- Modo Personalizado ', 35, ancho_ventana/2, alto_ventana/2 + 75, ventana, negro, \
					marfil, negro)

				# Cuadro de Ingreso de Datos:
				datos, listo = escribeJugador(datos)
				cuadroCentrado(' Ingrese su opcion: ' + "".join(datos), 20, ancho_ventana/2, 500, ventana,\
						 negro, marfil, negro)
				if muestra_error and time.time()-tiempo < 1.5:
					cuadroCentrado(' Opcion no valida. ', 20, ancho_ventana/2, 550, ventana,\
						negro, marfil, negro)
			else:
				try:
					assert(len(datos)==1 and (datos[0]=='r' or datos[0]=='1' or datos[0]=='2'))
					
					# Si el usuario escogio modo aleatorio:
					if datos[0]=='1':
						if nivel == 1:
							n_tablero = random.randint(0, len(tableros_faciles)-1)
							tablero = tableros_faciles[n_tablero]
						elif nivel == 2:
							n_tablero = random.randint(0, len(tableros_dificiles) - 1)
							tablero = tableros_dificiles[n_tablero]
						elif nivel == 4:
							n_tablero = random.randint(0, len(tablerosdefecto)-1)
							tablero = tablerosdefecto[n_tablero]
						inicializarTablero(tablero_final)
						llenarTablero(tablero_final, tablero)
						tablero = []
						pantalla_mcarga = False
						pantalla_juego = True
						contador = 0
						primera_vez = True
						jugada = False
						paused = False
						contador_victorias = 0

					# Si el usuario escogio el modo personalizado:
					elif datos[0]== '2':
						pantalla_configuracion = True
						pantalla_mcarga = False
						tiempo = 0
						tablero = []
					
					# Si el usuario escogio regresar al menu de escoger dificultad
					else:
						pantalla_mcarga = False
						pantalla_pnueva = True
					muestra_error = False
					datos = []
					listo = False
				except:
					tiempo = time.time()
					muestra_error = True
					datos = []
					listo = False

		# Trozo de codigo que se encargara de mostrar la pantalla de configuracion de tablero por parte del usuario
		elif pantalla_configuracion:
			ventana.blit(menu2, (0,0))
			# Si el usuario no ha presionado enter:
			if not listo:
				pygame.draw.rect(ventana, negro, (25, 50, 350, 350))
				cuadroCentrado(' Personalizacion del tablero: ', 30, ancho_ventana/2, 25, ventana, negro, marfil, negro)
				pygame.draw.rect(ventana, negro,(420, 70, 170 , 310))
				pygame.draw.rect(ventana, marfil,(430, 80, 150 , 290))
				
				# Dibujando el tablero de referencia
				for i in range(4):
					cuadroCentrado(str(4-i), 20, 37,i*75+110, ventana, blanco, negro, negro)
				cuadroCentrado('a', 20, 86, 385,ventana, blanco, negro, negro)
				cuadroCentrado('b', 20, 161, 385,ventana, blanco, negro, negro)
				cuadroCentrado('c', 20, 236, 385,ventana, blanco, negro, negro)
				cuadroCentrado('d', 20, 311, 385,ventana, blanco, negro, negro)
				for i in range(4):
					for j in range(4):
						if (i+j)%2 == 0:
							pygame.draw.rect(ventana, cafe, (i*75+50 ,j*75+75, 75, 75))
						else:
							pygame.draw.rect(ventana, marfil, (i*75+50, j*75+75, 75, 75))
				
				# Dibujando las piezas para el usuario:
				ventana.blit(torre, (208, 158))
				ventana.blit(alfil, (60, 310))
				ventana.blit(caballo, (60,80))
				ventana.blit(reina, (283, 230 ))

				# Dibujando leyenda para el usuario:
				cuadroCentrado('T: Torre', 18, 500, 100, ventana, negro, marfil, marfil)
				cuadroCentrado('A: Alfil', 18, 500, 140, ventana, negro, marfil, marfil)
				cuadroCentrado('C: Caballo', 18, 500, 180, ventana, negro, marfil, marfil)
				cuadroCentrado('R: Rey', 18, 500, 220, ventana, negro, marfil, marfil)
				cuadroCentrado('D: Reina', 18, 500, 260, ventana, negro, marfil, marfil)
				cuadroCentrado('* *: Peon', 18, 500, 300, ventana, negro, marfil, marfil)
				cuadroCentrado('r: Regresar', 18, 500, 340, ventana, negro, marfil, marfil)
				
				cuadroCentrado(' Configuracion de tablero de ejemplo: Tc3-Aa1-Ca4-Dd2 ', 20, ancho_ventana/2, 470, \
					ventana, negro, marfil, negro)
				tablero, listo = escribeJugador(tablero)
				
				# Cuadro de ingreso de datos:
				cuadroCentrado(''.join(tablero), 20, ancho_ventana/2, 550, ventana, negro, marfil, negro)
				if not muestra_error:
					cuadroCentrado(' Selecciona tu propia configuracion: ', 20, ancho_ventana/2, \
						510, ventana, negro, marfil, negro)
				else:
					cuadroCentrado(' Esa Configuracion no es valida. ', 20, ancho_ventana/2, 510, ventana,\
						negro, marfil, negro)
				if time.time()-tiempo >= 1.5:
					muestra_error = False
			else:
				try:
					tablero = ''.join(tablero)
					tablero = tablero.split("-")
					# Si el usuario decide regresar:
					if tablero == ['r']:
						raise ZeroDivisionError
					# En estos assert verifico que haya ingresado por lo menos dos fichas,
					# que hayan como maximo 2 peones, 2 alfiles, 2 torres, 2 caballos, 1 reina y un rey.
					# Tambien verifico que la sintaxis dada por el usuario sea la correcta, es decir que el 
					# alfil sea A, el rey K, etc... y que las coordenadas sean correctas. Ademas verifico si
					# hay una pieza encima de la otra, es decir, si el usuario escribio c1-c1 por ejemplo
					assert(len(tablero) >= 2 and len(tablero) <= 10  \
						and	all( (len(tablero[i]) == 2 and (tablero[i][0] in "abcd") and \
						(tablero[i][1] in "1234")) or ( len(tablero[i]) == 3 and (tablero[i][0] in "ARDTC")\
						 and (tablero[i][1] in "abcd") and (tablero[i][2] in "1234")) for i in range(len(tablero))))
					inicializarTablero(tablero_final)
					llenarTablero(tablero_final, tablero)
					for i in range(4):
						for j in range(4):
							if tablero_final[i][j] != None:
								if tablero_final[i][j] == 'alfil':
									n_alfil += 1
									# Maximo 2 alfiles
									assert(n_alfil < 3)
								elif tablero_final[i][j] == 'torre':
									# Maximo 2 torres
									n_torre += 1
									assert(n_torre < 3)
								elif tablero_final[i][j] == 'rey':
									# Maximo 1 rey
									n_rey += 1
									assert(n_rey < 2)
								elif tablero_final[i][j] == 'reina':
									# Maximo 1 reina
									n_reina += 1
									assert(n_reina < 2)
								elif tablero_final == 'caballo':
									# Maximo dos caballos
									n_caballo += 1
									assert(n_caballo < 3)
								else:
									# Maximo dos peones
									n_peon += 1
									assert(n_peon < 3)
								n_piezas += 1
					# En el siguiente assert verifico dos cosas importantes:
					# 1) Que el numero de piezas coincida con las que metio el usuario
					# 2) Que al tablero ingresado se le pueda por lo menos realizar una jugada, es decir,
					# que el tablero ingresado no sea imposible de resolver asi tal cual como nos lo ingrese el usuario
					fine = movimientosDisponibles(tablero_final)
					print(fine)
					print(tablero)
					assert(n_piezas==len(tablero) and fine[0])
					pantalla_configuracion = False
					muestra_error = False
					pantalla_juego = True
					listo = False
					contador = 0
					jugada = False
					paused = False
					tablero = []
					primera_vez = True
					n_piezas = n_alfil = n_torre = n_rey = n_reina = n_caballo = n_caballo = 0
				except ZeroDivisionError:
					pantalla_mcarga = True
					pantalla_configuracion = False
					muestra_error = False
				except AssertionError:
					tiempo = time.time()
					muestra_error = True
					tablero = []
					listo = False
					n_piezas = n_alfil = n_torre = n_rey = n_reina = n_caballo = n_caballo = 0

		#Trozo de codigo que se encarga de mostrar la pantalla de juego con todas sus funcionalidades
		elif pantalla_juego:

			# Cuando el jugador decide salir de la partida
			if finish:

				# Si el modo es muy dificil o entrenamiento, no se guardan partidas.
				if nivel in [3,4]:
					pantalla_juego = False
					pantalla_principal = True
					finish = False
				
				# Mientras no presione enter:
				elif not listo:
					ventana.blit(puerta, (0,0))
					datos, listo = escribeJugador(datos)
					cuadroCentrado(' Desea guardar la partida?(S/N) ', 30, ancho_ventana/2, alto_ventana/2-50,\
					 ventana, negro, marfil, negro)
					cuadroCentrado("".join(datos), 30, ancho_ventana/2, alto_ventana/2, ventana, negro, \
						marfil, negro)
					if muestra_error and time.time() - tiempo < 1.5:
						cuadroCentrado(' Opcion no valida. ', 30, ancho_ventana/2, alto_ventana/2 + 50, \
							ventana, negro, marfil, marfil)
				
				# Cuando decide guardar la partida:
				else:
					try:
						assert(datos[0] in "sSnN")
						if datos[0] in 'sS':
							with open('ArchivosDeTexto/PartidasGuardadas.txt', 'a+') as f:
								lista_partidas = f.readlines()[1:]
								nueva_entrada = '' # Creamos la entrada
								fecha = datetime.datetime.now()
								nueva_entrada += str(fecha.day)+str(fecha.month)+str(fecha.year)+'\t'
								nueva_entrada += str(minutero) + ':' + str(segundero) + '\t'
								if len(lista_partidas) == 0:
									nueva_entrada = '1\t' + nueva_entrada
								else:
									numero_partida = int((lista_partidas[len(lista_partidas) - 1].split('\t'))[0]) + 1
									nueva_entrada = str(numero_partida)+'\t' + nueva_entrada
								if nivel == 1:
									nueva_entrada += 'Facil\t'
								elif nivel == 2:
									nueva_entrada += 'Dificil\t'
								nueva_entrada += guardaTablero(tablero_final)+'\t'
								nueva_entrada += str(contador) + '\n'
								f.write(nueva_entrada)
							color1 = negro
							color2 = marfil
							cargar_disponible = True
							tiempo = time.time()
							nueva_entrada = nueva_entrada.split('\t')
							while time.time() - tiempo < 5:
								cuadroCentrado(' El codigo de su partida es: ', 30, ancho_ventana/2, alto_ventana/2, ventana, negro, marfil, negro)
								cuadroCentrado(' '+nueva_entrada[0]+' '+nueva_entrada[1]+' '+nueva_entrada[3]+' ',\
									30, ancho_ventana/2, alto_ventana/2 + 50, ventana, negro, marfil, negro)
								pygame.display.flip()
						pantalla_juego = False
						pantalla_principal = True
						listo = False
						finish = False
						datos = []
						primera_vez = True
						jugada_cache = None
						deshacer_disponible = False
						jugada = False
					except AssertionError:
						datos = []
						muestra_error = True
						tiempo = time.time()
						listo = False
			
			# Cuando el jugador gana.
			elif victoria:
				ventana.blit(img_victoria, (0,0))
				noEscribe()
				#pintaTablero()
				#acomodaTablero(tablero_final)
				tiempo = time.time()
				while time.time() - tiempo < 3:
					cuadroCentrado(' Ganaste! ', 30, ancho_ventana/2, alto_ventana/2, ventana, blanco, azul, blanco)
					pygame.display.flip()
				records = []
				with open('ArchivosDeTexto/Records.txt', 'r') as f:
					records = f.readlines()
				if len(records) == 1:
					if nivel == 1:
						records.append("".join(nombre) + '\t1\tFacil\n')
					elif nivel == 2:
						records.append("".join(nombre) + '\t1\tDificil\n')
					elif nivel == 3:
						records.append("".join(nombre) + '\t1\tMuy Dificil\n')
				else:
					for i in range(1, len(records)):
						entrada = records[i].split('\t')
						if entrada[0] == "".join(nombre):
							if nivel == 1 and entrada[2] == 'Facil\n':
								records.append(entrada[0] + '\t' + str(int(entrada[1]) + 1) + '\tFacil\n')
								del(records[i])
								break
							elif nivel == 2 and entrada[2] == 'Dificil\n':
								records.append(entrada[0] + '\t' + str(int(entrada[1]) + 1) + '\tDificil\n')
								del(records[i])
								break
							elif nivel == 3 and entrada[2] == 'Muy Dificil\n':
								records.append(entrada[0] + '\t' + str(int(entrada[1]) + 1) + '\tMuy Dificil\n')
								del(records[i])
								break
							else:
								continue
					else:
						if nivel == 1:
							records.append("".join(nombre) + '\t1\tFacil\n')
						elif nivel == 2:
							records.append("".join(nombre) + '\t1\tDificil\n')
						elif nivel == 3:
							records.append("".join(nombre) + '\t1\tMuy Dificil\n')

				with open('ArchivosDeTexto/Records.txt', 'w') as f:
					for line in records:
						f.write(line)

				records_disponible = True
				color3 = negro
				color4 = marfil
				pantalla_principal = True
				pantalla_juego = False
				victoria = False
				deshacer_disponible = False
				jugada_cache = None
				muestra_solucion = (False, 0, 0, 0, 0)
				solucion = False
			
			elif derrota:
				ventana.blit(img_derrota, (0,0))
				noEscribe()
				#pintaTablero()
				#acomodaTablero(tablero_final)
				tiempo = time.time()
				while time.time() - tiempo < 3:
					if not(movimientosDisponibles(tablero_final)[0]):
						cuadroCentrado(' No quedan movimientos disponibles! ', 30, ancho_ventana/2, alto_ventana/2, ventana, blanco, negro, blanco)
					elif minutero == 0 and segundero == 0:
						cuadroCentrado(' Se agoto el tiempo! ', 30, ancho_ventana/2, alto_ventana/2, ventana, blanco, negro, blanco)
					pygame.display.flip()
				tiempo = time.time()
				while time.time() - tiempo < 3:
					cuadroCentrado(' Perdiste! ', 30, ancho_ventana/2, alto_ventana/2 + 40, ventana, blanco, negro, blanco)
					pygame.display.flip()
				pantalla_juego = False
				pantalla_principal = True
				derrota = False
				deshacer_disponible = False
				jugada_cache = None
				solucion = False
				muestra_solucion = (False, 0, 0, 0, 0)
			
			else:
				ventana.blit(fondo_tablero, (0,0))
				pygame.draw.rect(ventana, negro, (25, 50, 370, 370))

				# Saludando al jugador:
				cuadroCentrado(' Partida de: '+"".join(nombre)+" ", 30, ancho_ventana/2, 25, ventana, negro, marfil, negro)

				# Dibujando el tablero:
				for i in range(4):
					cuadroCentrado(str(4-i), 20, 37,i*80+110, ventana, blanco, negro, negro)
				cuadroCentrado('a', 20, 90, 406,ventana, blanco, negro, negro)
				cuadroCentrado('b', 20, 170, 406,ventana, blanco, negro, negro)
				cuadroCentrado('c', 20, 250, 406,ventana, blanco, negro, negro)
				cuadroCentrado('d', 20, 330, 406,ventana, blanco, negro, negro)
				
				pintaTablero()

				if muestra_solucion[0]:
					pygame.draw.rect(ventana, azul, (muestra_solucion[2]*80+50, muestra_solucion[1]*80+75, 80, 80),4)
					pygame.draw.rect(ventana, azul, (muestra_solucion[4]*80+50, muestra_solucion[3]*80+75, 80, 80),4)
				
				if paused or primera_vez:
					contador = 0
					acomodaTablero(tablero_vacio)
				else:
					acomodaTablero(tablero_final)
				
				# Cuadro de dificultad y tiempo restante
				pygame.draw.rect(ventana, negro,(420, 70, 170 , 210))
				pygame.draw.rect(ventana, marfil,(430, 80, 150 , 190))
				cuadroCentrado(' Nivel: ', 20, 505, 110, ventana, negro, marfil, marfil)
				cuadroCentrado(' Tiempo: ', 20, 505, 200, ventana, negro, marfil, marfil)
				if nivel == 1:
					minutero = (-contador/FPS + 181)//60
					segundero = abs((contador/FPS)%60 - 60)%60
					cuadroCentrado(' Facil ', 30, 505, 150, ventana, negro, marfil, marfil)

					pygame.draw.rect(ventana, marron, (19, 445, 385, 100))
					# Boton de Play:
					if not jugada:
						pygame.draw.rect(ventana, cafe_os, (24, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 27, 454, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (24, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 27, 454, ventana, blanco, azul, azul)
					ventana.blit(play, (28, 457))
					
					# Boton de Pausa: 
					if not paused:
						pygame.draw.rect(ventana, cafe_os, (119, 450, 90, 90))
						cuadroALaIzq(' 2 ', 15, 122, 455, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (119, 450, 90, 90))
						cuadroALaIzq(' 2 ', 15, 122, 455, ventana, blanco, azul, azul)
					ventana.blit(pause, (123, 457))
					
					# Boton de deshacer:
					if jugada_cache == None:
						pygame.draw.rect(ventana, cafe_os, (214, 450, 90, 90))
						cuadroALaIzq(' 3 ', 15, 218, 455, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (214, 450, 90, 90))
						cuadroALaIzq(' 3 ', 15, 218, 455, ventana, blanco, azul, azul)
					ventana.blit(deshacer, (219, 457))
					
					# Boton de terminar
					pygame.draw.rect(ventana, cafe_os, (309, 450, 90, 90))
					cuadroALaIzq(' 4 ', 15, 312, 455, ventana, blanco, cafe_os, cafe_os)
					ventana.blit(terminar, (313, 457))

				elif nivel == 2:
					minutero = (-contador/FPS+91)//60
					segundero = (abs(((contador)/FPS)%60-60)%60-30)%60
					cuadroCentrado(' Dificil ', 30, 505, 150, ventana, negro, marfil, marfil)

					# Boton de Play:
					if not jugada:
						pygame.draw.rect(ventana, cafe_os, (69, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 72, 454, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (69, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 72, 454, ventana, blanco, azul, azul)
					ventana.blit(play, (73, 457))
					
					# Boton de Pausa: 
					if not paused:
						pygame.draw.rect(ventana, cafe_os, (164, 450, 90, 90))
						cuadroALaIzq(' 2 ', 15, 167, 455, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (164, 450, 90, 90))
						cuadroALaIzq(' 2 ', 15, 167, 455, ventana, blanco, azul, azul)
					ventana.blit(pause, (168, 457))
					
					# Boton de terminar:
					pygame.draw.rect(ventana, cafe_os, (259, 450, 90, 90))
					cuadroALaIzq(' 3 ', 15, 263, 455, ventana, blanco, cafe_os, cafe_os)
					ventana.blit(terminar, (264, 457))

				elif nivel == 3:
					minutero = (-contador/FPS+121)//60
					segundero = abs((contador/FPS)%60 - 60)%60
					cuadroCentrado(' Muy Dificil ', 25, 505, 150, ventana, negro, marfil, marfil)

					# Boton de Play:
					if not jugada:
						pygame.draw.rect(ventana, cafe_os, (117, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 120, 454, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (117, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 120, 454, ventana, blanco, azul, azul)
					ventana.blit(play, (121, 457))

					# Boton de terminar:
					pygame.draw.rect(ventana, cafe_os, (210, 450, 90, 90))
					cuadroALaIzq(' 2 ', 15, 214, 455, ventana, blanco, cafe_os, cafe_os)
					ventana.blit(terminar, (215, 457))
				
				elif nivel == 4:
					cuadroCentrado(' Entrenamiento ', 18, 505, 150, ventana, negro, marfil, marfil)

					# Boton de Play:
					if not jugada:
						pygame.draw.rect(ventana, cafe_os, (24, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 27, 454, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (24, 450, 90, 90))
						cuadroALaIzq(' 1 ', 15, 27, 454, ventana, blanco, azul, azul)
					ventana.blit(play, (28, 457))
					
					# Boton de Pista: 
					if solucion:
						pygame.draw.rect(ventana, azul, (119, 450, 90, 90))
						cuadroALaIzq(' 2 ', 15, 122, 455, ventana, blanco, azul, azul)
					else:
						pygame.draw.rect(ventana, cafe_os, (119, 450, 90, 90))
						cuadroALaIzq(' 2 ', 15, 122, 455, ventana, blanco, cafe_os, cafe_os)
					ventana.blit(pista, (123, 457))
					
					# Boton de deshacer:
					if jugada_cache == None:
						pygame.draw.rect(ventana, cafe_os, (214, 450, 90, 90))
						cuadroALaIzq(' 3 ', 15, 218, 455, ventana, blanco, cafe_os, cafe_os)
					else:
						pygame.draw.rect(ventana, azul, (214, 450, 90, 90))
						cuadroALaIzq(' 3 ', 15, 218, 455, ventana, blanco, azul, azul)
					ventana.blit(deshacer, (219, 457))
					
					# Boton de terminar
					pygame.draw.rect(ventana, cafe_os, (309, 450, 90, 90))
					cuadroALaIzq(' 4 ', 15, 312, 455, ventana, blanco, cafe_os, cafe_os)
					ventana.blit(terminar, (313, 457))

				# Manejando como se mostrara el tiempo
				if primera_vez:
					pygame.draw.rect(ventana, marfil, (430, 235, 150, 30))
					pygame.draw.rect(ventana, marfil, (430, 235, 150, 30))
					if nivel != 4:
						cuadroCentrado(tiempo_espera, 30, 505, 240, ventana, rojo, marfil, marfil)
					else:
						cuadroCentrado('-:--', 30, 505, 240, ventana, rojo, marfil, marfil)
				elif nivel == 4:
					cuadroCentrado('-:--', 30, 505, 240, ventana, rojo, marfil, marfil)
				elif paused:
					if segundero_pausado < 10:
						pygame.draw.rect(ventana, marfil, (430, 235, 150, 30))
						cuadroCentrado(str(minutero_pausado) + ":0" + str(segundero_pausado), 30, 505, 240, \
						ventana, rojo, marfil, marfil)
					else:
						pygame.draw.rect(ventana, marfil, (430, 235, 150, 30))
						cuadroCentrado(str(minutero_pausado) + ":" + str(segundero_pausado), 30, 505, 240, \
						ventana, rojo, marfil, marfil)
				elif segundero < 10:
					pygame.draw.rect(ventana, marfil, (430, 235, 150, 30))
					cuadroCentrado(str(minutero) + ":0" + str(segundero), 30, 505, 240, \
						ventana, rojo, marfil, marfil)
				else:
					pygame.draw.rect(ventana, marfil, (430, 235, 150, 30))
					cuadroCentrado(str(minutero) + ":" + str(segundero), 30, 505, 240, \
						ventana, rojo, marfil, marfil)

				if minutero == 0 and segundero == 0:
					derrota = True

				# Cuadro de ingreso de datos:
				pygame.draw.rect(ventana, negro, (420, 300, 170 , 200))
				pygame.draw.rect(ventana, marfil, (430, 310, 150 , 180))

				if not jugada:
					if muestra_error and time.time() - tiempo < 1:
						noEscribe()
						if not deshacer_disponible and nivel in [1, 2, 4]:
							cuadroCentrado('No se puede', 20, 505, 355, ventana, negro, marfil, marfil)
							cuadroCentrado('deshacer', 20, 505, 380, ventana, negro, marfil, marfil)
						elif not muestra_solucion[0] and nivel == 4 and solucion:
							cuadroCentrado('No hay solucion', 18, 505, 355, ventana, negro, marfil, marfil)
							cuadroCentrado('para la posicion', 18, 505, 380, ventana, negro, marfil, marfil)
							cuadroCentrado('dada', 18, 505, 405, ventana, negro, marfil, marfil)
						else:
							cuadroCentrado('Opcion', 20, 505, 355, ventana, negro, marfil, marfil)
							cuadroCentrado('erronea', 20, 505, 380, ventana, negro, marfil, marfil)
					elif not listo:
						deshacer_disponible = True
						datos, listo = escribeJugador(datos)
						if primera_vez:
							cuadroCentrado('Presione 1', 20, 505, 355, ventana, negro, marfil, marfil)
							cuadroCentrado('para empezar', 20, 505, 380, ventana, negro, marfil, marfil)
						elif paused:
							cuadroCentrado('Presione 2', 20, 505, 355, ventana, negro, marfil, marfil)
							cuadroCentrado('para continuar', 20, 505, 380, ventana, negro, marfil, marfil)
						elif solucion:
							cuadroCentrado('Ingrese la', 20, 505, 355, ventana, negro, marfil, marfil)
							cuadroCentrado('coordenada', 20, 505, 380, ventana, negro, marfil, marfil)
						else:
							cuadroCentrado(' Ingrese ', 20, 505, 355, ventana, negro, marfil, marfil)
							cuadroCentrado(' opcion: ', 20, 505, 380, ventana, negro, marfil, marfil)
						cuadroCentrado("".join(datos), 20, 505, 430, ventana, negro, marfil, marfil)
						if len(datos) > 10:
							datos = []
					else:
						try:
							assert((len(datos) == 1 and datos[0] in '1234') or (len(datos) == 2 and datos[0] \
								in 'abcd' and datos[1] in '1234'))
							if primera_vez:
								if datos[0] == '1':
									primera_vez = False
									contador = 0
								else:
									muestra_error = True
									tiempo = time.time()
							elif paused:
								if nivel in [1,2] and datos[0] == '2':
									paused = False
									contador = tiempo_pausado
								else:
									muestra_error = True
									tiempo = time.time()
							elif solucion:
								if datos[0] == '2':
									solucion = False
									muestra_solucion = (False, 0, 0, 0, 0)
								elif datos[0] in '134':
									raise AssertionError
								elif datos[0] in 'abcd' and datos[1] in '1234':
									muestra_solucion = obtenSolucion(datos[0], datos[1], tablero_final)
									if not muestra_solucion[0]:
										raise AssertionError
									else:
										pass
							elif datos[0] == '1':
								jugada = True
							
							elif datos[0] == '2':
								if nivel in [1,2]:
									if not paused:
										paused = True
										minutero_pausado = minutero
										segundero_pausado = segundero
										tiempo_pausado = contador
									else:
										paused = False
										contador = tiempo_pausado
								elif nivel == 3:
									finish = True
								elif nivel == 4:
									solucion =  True
							elif datos[0] == '3':
								if nivel in [1,4]:
									if jugada_cache == None:
										deshacer_disponible = False
										raise AssertionError
									else:
										tablero_final[4 - int(jugada_cache[0][1])][obtieneCoordLetra(jugada_cache[0])] = jugada_cache[2]
										tablero_final[4 - int(jugada_cache[1][1])][obtieneCoordLetra(jugada_cache[1])] = jugada_cache[3]
										jugada_cache = None
										deshacer_disponible = False
								elif nivel == 2:
									finish = True
								else:
									raise AssertionError

							elif datos[0] == '4':
								if nivel in [1,4]:
									finish = True
								else:
									raise AssertionError

						except AssertionError:
							muestra_error = True
							tiempo = time.time()
						listo = False
						datos = []
				else:
					if muestra_error and time.time() - tiempo < 1:
						noEscribe()
						cuadroCentrado(' Jugada ', 20, 505, 355, ventana, negro, marfil, marfil)
						cuadroCentrado(' erronea ', 20, 505, 380, ventana, negro, marfil, marfil)
					elif not listo:
						datos, listo = escribeJugador(datos)
						cuadroCentrado(' Ingrese ', 20, 505, 355, ventana, negro, marfil, marfil)
						cuadroCentrado(' jugada: ', 20, 505, 380, ventana, negro, marfil, marfil)
						cuadroCentrado("".join(datos), 20, 505, 430, ventana, negro, marfil, marfil)
					else:
						try:
							assert((len(datos) == 1 and datos[0] == '1') or (len(datos) == 5 and (datos[0] in "abcd") and (datos[3]\
							 in "abcd") and (datos[1] in "1234") and (datos[4] in "1234")))
							if datos[0] == '1':
								jugada = False
							else:
								jugada_actual = "".join(datos).split("-")
								piezas_cache1, piezas_cache2 = muevePieza(tablero_final, jugada_actual[0], jugada_actual[1])
								jugada_actual.append(piezas_cache1)
								jugada_actual.append(piezas_cache2)
								jugada_cache = jugada_actual
								deshacer_disponible = True
								solucion = False
								a = movimientosDisponibles(tablero_final)
								animacionMovimientoPiezas(jugada_cache)
								if contadorPiezas(tablero_final) == 1:
									contador_victorias += 1
									if nivel in [1, 2, 4]:
										victoria = True
									elif nivel == 3 and contador_victorias != 3:
										inicializarTablero(tablero_final)
										llenarTablero(tablero_final, tableros[0])
										del(tableros[0])
									elif nivel == 3 and contador_victorias == 3:
										victoria = True
								elif not a[0] and contadorPiezas(tablero_final) > 1:
									derrota = True
						except AssertionError:
							muestra_error = True
							tiempo = time.time()
						listo = False
						datos = []
			contador += 1
		pygame.display.update()
		fpsClock.tick(FPS)
# Postcondicion: True

if __name__=='__main__':
	main()