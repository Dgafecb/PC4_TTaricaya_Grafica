import pygame
import pytmx
from settings import WIDTH, HEIGHT, FPS
from player import Player
from utils import load_tileset, draw_map
from dialogue import DialogueBox  # Importa el cuadro de diálogo
from pytmx import load_pygame
from utils import load_story_from_json
from turtles import Turtle
import random
from crab import Crab  # Importa la clase Crab
from utils import  draw_score
import time
from power import Power  # Importa la clase Power
from utils import  draw_powerup_info
from zorro import Fox
from egg import Egg
import math
import json
from utils import mostrar_letrero_personalizado
from buttons import Button
from enemy import Enemy
from utils import draw_image, draw_map_from_tmx, check_collision,check_collision_power
from utils import init_objects
from utils import generate_random_turtle,generate_random_fox,generate_random_enemy
from settings import WIDTH, HEIGHT, FPS
import os
import sys
from gif import GifBackground
import subprocess
import pygame_menu


from utils import *
from dialogue import DialogueBox
import asyncio

# Inicializa el mixer de Pygame
pygame.mixer.init()

path_musica_dia = '../assets/sounds/platformer_level03_loop.ogg'
path_musica_noche = '../assets/sounds/fantasy Dragon.ogg'
path_musica_menu = '../assets/sounds/arcade.ogg'

# Cargar la música
#pygame.mixer.music.load(path_musica_menu)  # Ruta a tu archivo de música

#pygame.mixer.music.set_volume(0.5)  # Establece el volumen (opcional)

path_nido ='../assets/images/ui/frames/nido.png'

# Inicialización
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PC4: Guardianes de las Taricayas")
clock = pygame.time.Clock()

# Cargar un mapa con Tiled
tmx_map_dia = load_pygame("../MapaDia.tmx")
mapa_noche = pygame.image.load("../MapaNoche.png").convert_alpha()
# Escala la imagen al tamaño de la pantalla
mapa_noche = pygame.transform.scale(mapa_noche, screen.get_size())

# Instancia del narrador
narrador_assets_path = "../assets/images/narrator_assets/Amazon.png"
narrador_sprite = pygame.image.load(narrador_assets_path).convert_alpha()
narrador_sprite = pygame.transform.scale(narrador_sprite,(200,200))

# Posicion del narrador
narrador_sprite_x = 50 + 700 // 2 - narrador_sprite.get_width() // 2  # Basado en las dimensiones del cuadro de diálogo
narrador_sprite_y = 450 - narrador_sprite.get_height() - 10  # 10 píxeles encima del cuadro

# Crear el cuadro de diálogo de narrativa inicial
dialogue_box = DialogueBox(
    letters_path="../assets/images/ui/ascii_noche/",
    position=(50, 450),
    text_speed=0.5,
    box_width=700,
    box_height=120,
    letter_size=(16, 16)
)
story = load_story_from_json('../history.json')
story_noche = load_story_from_json("../history.json", "story_noche")
story_dia = load_story_from_json("../history.json", "story_dia")

# Inicialización de los objetos del juego
turtles,powerups,foxes,eggs,enemies = init_objects()

# Lista de cangrejos
crabs = pygame.sprite.Group()
for _ in range(4):  # Por ejemplo, 3 cangrejos
    crab_asset_path = "../assets/images/crab_assets"
    crab = Crab(crab_asset_path, turtles)
    crabs.add(crab)
              

# Agrega una variable para saber si el jugador está siguiendo una tortuga
following_turtle = None

# Creamos una lista de packs
egg_packs = {}

# Función para generar huevos en un patrón circular
def generate_pack_egg(x, y, n):
    """Genera un pack de huevos en una posición (x, y) en un patrón circular"""
    radio = 25  # Ajusta este valor dependiendo de qué tan dispersos quieres los huevos
    angulo_incremento = 2 * math.pi / n  # Para distribuir los huevos de manera equidistante
    
    # Lista de los objetos egg
    lista_egg = []  
   
    for i in range(n):
        # Calcular el ángulo para cada huevo
        angulo = angulo_incremento * i
        # Calcular la nueva posición para cada huevo en el círculo
        egg_x = x + math.cos(angulo) * radio
        egg_y = y + math.sin(angulo) * radio
        
        # Crear el huevo en la nueva posición calculada
        egg = Egg(egg_x, egg_y, "../assets/images/egg_assets",enemies)
        eggs.add(egg)  # Agregar el huevo al grupo de sprites
        lista_egg.append(egg)  # Agregar el huevo a la lista de huevos
    # Agregamos la lista de huevos a la lista de packs
    egg_packs[(x, y)] = lista_egg


# Función para eliminar los huevos de un pack específico
def remove_eggs_in_pack(pack_x, pack_y):
    """Elimina los huevos correspondientes a un pack en la posición (pack_x, pack_y)"""
    # Obtener la lista de huevos del pack
    lista_egg = egg_packs[(pack_x, pack_y)]

    # Eliminar cada huevo de la lista de sprites
    for e in lista_egg:
        e.kill()  # Elimina el huevo del grupo de sprites

    # Eliminar la entrada del pack en el diccionario
    del egg_packs[(pack_x, pack_y)]


# Función para crear o eliminar un pack de huevos
def create_or_remove_egg_pack(x, y):
    """Crea o elimina un pack de huevos en la posición especificada."""
  
    # Verificar si el clic está dentro de un pack existente
    for (pack_x, pack_y), list_packs in egg_packs.items():
        # Verificar si el clic está dentro del radio del pack
        distancia = math.sqrt((x - pack_x) ** 2 + (y - pack_y) ** 2)
        if distancia < 25:  # Si está dentro del radio del pack (ajustar el radio según sea necesario)
            #print(f"Eliminando huevos en el pack en ({pack_x}, {pack_y})")
            remove_eggs_in_pack(pack_x, pack_y)  # Eliminar los huevos del pack
            break
    else:
        # Si no hay un pack en esta posición y no hemos alcanzado el máximo de 5
        if len(egg_packs) < max_egg_packs:
            #print("Creando un nuevo pack de huevos")
            generate_pack_egg(x, y, 5)  # Crear un nuevo pack de huevos
        
# Variables globales
max_egg_packs = 5  # Número máximo de packs de huevos generados


# Variables globales para el puntaje y tiempo
score = 0
start_time = None
start_time_dia = None
start_time_noche =None
time_left = 60  # 60 segundos para completar la misión
# Instancia de los botones
#Botones
boton_sirena = Button(100, 100, '../assets/images/botones_assets/boton_A.png',
                       '../assets/images/botones_assets/boton_A_presionado.png',
                       '../assets/sounds/effects/policia/police_2.wav')
boton_perros = Button(200, 200,  '../assets/images/botones_assets/boton_B.png',
                       '../assets/images/botones_assets/boton_B_presionado.png',
                       '../assets/sounds/effects/perros/dog_barking.wav')
# Instancia del jugador
player_assets_path = "../assets/images/player_assets"
player = Player(WIDTH // 2, HEIGHT // 2, player_assets_path, "../MapaDia.tmx", turtles, crabs)
 # estados del juego
ESTADOS = {"narrativa_inicio":0,"narrativa_noche":1, "juego_noche":2, "narrativa_dia":3, "juego_dia":4,"puntaje_noche":5,"puntaje_noche_transicion":6,"puntaje_noche_terminado":7,"puntaje_final_transicion":8,"puntaje_final":9,"menu":10}
# estado actual del juego

#estado_actual = ESTADOS["narrativa_inicio"]# 0 
estado_actual = ESTADOS["menu"] # 10
TEMP = {"estado_actual":10}

gif_bg = GifBackground("../video.gif", (WIDTH, HEIGHT))




if estado_actual == ESTADOS["menu"]:
    # Reproducir música (en loop infinito)
    pygame.mixer.music.load(path_musica_menu)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
        

running = True
in_story = True  # Variable para controlar si estamos en la narrativa inicial
current_story_index = 0  # Variable local para manejar el índice de la narrativa
dialogue_box.set_text(story[current_story_index])  # Establecer el primer texto
current_story_index_noche = 0
current_story_index_dia = 0
# Variables para controlar el tiempo y la aparición de tortugas
last_turtle_spawn_time = 0  # Tiempo de la última aparición de tortuga
turtle_spawn_interval = 3000  # Intervalo en milisegundos (3 segundos)

max_turtles = 25  # Máximo número de tortugas en pantalla
start_time = None
start_time_noche = None # Inicia el cronometro despues de la narrativa de noche
start_time_dia = None  # Inicia el cronómetro después de la historia
game_duration = 60  # Duración del juego en segundos
noche_duration = 60 # Duracion de la noche
dia_duration = 60 # Duracion del dia
x_, y_ = 0, 0  # Inicializar las variables x_ y y_

# Intervalo de los power-ups
power_interval = 2000  # Tiempo de la última aparición de power-up
last_powerup_spawn_time = 0  # Intervalo en milisegundos (2 segundos)

# Variables para los poderes
powerup_active = None  # Power-up activo (puede ser 'speed', 'attract', etc.)
powerup_start_time = 0  # Tiempo de inicio del power-up
powerup_duration = 5000  # Duración de 5 segundos para cada power-up
powerup_cooldowns = {'speed': 0, 'invisible_turtle_follower': 0, 'turtle_speed': 0}  # Cooldowns de los poderes
time_left_powerup = 0  # Tiempo restante del power-up activo

color_fondo = '#071821'
color_letra = '#e4fccc'
dialogue_box.letters_path = "../assets/images/ui/ascii_noche/"
# Añadir las tortugas al grupo al inicio
generate_random_turtle(12,turtles)  # Iniciar con una tortuga

'''
Integracion de menu

'''
# Colores de dia
lg_bg = '#e4fccc'
dg_bg = '#071821'

lg_font = '#e4fccc'
theme = pygame_menu.themes.THEME_DARK.copy()
theme.background_color = (0, 0, 0, 0)
theme.button_font_color = lg_bg

menu = pygame_menu.Menu('         Taricaya: Guardian del Amazonas        ', WIDTH, HEIGHT, theme=theme)
# Ajustar la creación de botones
menu.add.button('Empezar Juego', lambda: start_game(screen,TEMP))
menu.add.button('Ver Instrucciones', lambda: create_instructions_menu(screen))
menu.add.button('Salir', pygame_menu.events.EXIT)
current_menu = menu

while running:

    
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            
            if estado_actual in [ESTADOS["narrativa_inicio"]]: # Refactorizo historia para verificar que esta en la narrativa inicial
                if event.key == pygame.K_q:  # Avanza la narrativa con la tecla Q
                    if current_story_index < len(story) - 1:
                        current_story_index += 1
                        dialogue_box.set_text(story[current_story_index])
                    else:
                        #in_story = False  # Refactorizo el fin de la narrativa inicial
                        estado_actual = ESTADOS["narrativa_noche"] #Para que pueda iniciar la narrativa del juego de noche
                        #dialogue_box.hide()
                        #inicia el dialogo de noche
                        dialogue_box.set_text(story_noche[current_story_index_noche])
                        
                elif event.key == pygame.K_SPACE:  # Salta la narrativa
                    #dialogue_box.hide()
                    #in_story = False
                    estado_actual = ESTADOS["narrativa_noche"] #Para que pueda iniciar la narrativa del juego de noche
                    #inicia el dialogo de noche
                    dialogue_box.set_text(story_noche[current_story_index_noche])
            # Avanzar dialogo de narrativa noche
            elif estado_actual in [ESTADOS["narrativa_noche"]]: 
                if event.key == pygame.K_q:  # Avanza la narrativa con la tecla Q
                    if current_story_index_noche < len(story_noche) - 1:
                        current_story_index_noche += 1
                        dialogue_box.set_text(story_noche[current_story_index_noche])
                    else:
                        
                        estado_actual = ESTADOS["juego_noche"] #Para que pueda iniciar el juego de noche
                        dialogue_box.hide()
                        
                        
                        
                elif event.key == pygame.K_SPACE:  # Salta la narrativa
                    dialogue_box.hide()

                    estado_actual = ESTADOS["juego_noche"] #Para que pueda iniciar el juego de noche
                    #start_time_noche = time.time()
            # Avanzar dialogos narrativa de dia
            elif estado_actual in [ESTADOS["narrativa_dia"]]: 
                if event.key == pygame.K_q:  # Avanza la narrativa con la tecla Q
                    if current_story_index_dia < len(story_dia) - 1:
                        current_story_index_dia += 1
                        dialogue_box.set_text(story_dia[current_story_index_dia])
                    else:
                        estado_actual = ESTADOS["juego_dia"] #Para que pueda iniciar el juego de noche
                        dialogue_box.hide()
                        start_time_dia = time.time()
                        # Cambiar el dialogo de dia
                        # 346c54 (letra dia) - # #e4fccc (fondo dia)
                        # Ubicar al player en el centro
                        player.x = WIDTH // 2
                        player.y = HEIGHT // 2
                        
                        
                elif event.key == pygame.K_SPACE:  # Salta la narrativa
                    dialogue_box.hide()
                    #in_story = False
                    estado_actual = ESTADOS["juego_dia"] #Para que pueda iniciar el juego de noche
                    start_time_dia = time.time()
                    player.x = WIDTH // 2
                    player.y = HEIGHT // 2
            # TRANSICION DEL PUNTAJE FINAL DE NOCHE
            elif estado_actual in [ESTADOS["puntaje_noche_transicion"]]: 
                if event.key == pygame.K_q or event.key == pygame.K_SPACE: # Presiona Q para dejar de mostrar puntaje y empezar la narrativa de dia
                    estado_actual = ESTADOS["puntaje_noche_terminado"]
                    dialogue_box.change_position((50,450))
            # PRESIONAR Q PARA EMPEZAR DE NUEVO
            elif estado_actual in [ESTADOS["puntaje_final_transicion"]]:
                if event.key == pygame.K_q:
                    # REINICIAR TODAS LAS VARIABLES
                    

                    estado_actual = ESTADOS["narrativa_inicio"]
                    score = 0
                    start_time = None
                    start_time_dia = None
                    start_time_noche =None
                    time_left = 60  # 60 segundos para completar la misión
                    current_story_index = 0
                    dialogue_box.change_position((50,450))
                    dialogue_box.set_text(story[current_story_index])
                    following_turtle = None
                    #egg_positions_individual = []

                    egg_packs= {}
                    #print(egg_packs)
                    for egg in eggs:
                        egg.kill()
                    for fox in foxes:
                        fox.kill()
                    for enemy in enemies:
                        enemy.kill()          
                    for turtle in turtles:
                        turtle.kill()  

                    Egg.score = 25
                    Turtle.score = 0

                    
                    
                if event.key == pygame.K_SPACE:
                    # Termina el juego si apreta espacio
                    running =  False
            if estado_actual in [ESTADOS["juego_noche"]]:
                if event.key == pygame.K_a:
                    #print("Presionando la tecla A")
                    #print(egg_packs)

                    # Verificar si ha colisionado con un huevo
                    for egg in eggs:
                        if player.rect.colliderect(egg.rect) and egg.is_taken_player == False:
                            #print("Huevo tomado")
                            egg.is_taken_player = True
                            egg.player = player
                            # Hemos encontrado al huevo, verificamos si este huevo pertenece a un pack
                            for (x_nido, y_nido), lista_egg in egg_packs.items():
                                if egg in lista_egg:
                                    #print(f"El huevo pertenece al pack en ({x_nido}, {y_nido})")
                                    # Eliminamos el huevo del pack
                                    lista_egg.remove(egg)
                                    break
                            break
                    
                elif event.key == pygame.K_s:
                    # Soltamos el huevo
                    #print("Presionando la tecla S")
                    for egg in eggs:
                        if egg.is_taken_player:
                            #print("Huevo soltado")
                            egg.stop_following_player()
                            # Hemos encontrado al huevo, verificamos si la posicion del huevo esta en el radio del nido del algun pack
                            for (x_nido, y_nido), lista_egg in egg_packs.items():
                                distancia = math.sqrt((egg.x - x_nido) ** 2 + (egg.y - y_nido) ** 2)
                                if distancia < 25:  # Si está dentro del radio del pack (ajustar el radio según sea necesario)
                                    #print(f"El huevo pertenece al pack en ({x_nido}, {y_nido})")
                                    
                                    # Agregamos el huevo al pack
                                    lista_egg.append(egg)

                                    # Calculamos la posición del huevo en el pack
                                    radio = 25  # Ajusta este valor dependiendo de qué tan dispersos quieres los huevos
                                    angulo_incremento = 2 * math.pi / max_egg_packs  # Para distribuir los huevos de manera equidistante
                                    
                                    # Calculamos el ángulo de la posición del huevo en el pack
                                    index = len(lista_egg) # El índice del huevo que acaba de ser agregado
                                    angulo = angulo_incremento * index  # Calculamos el ángulo correspondiente al huevo recién agregado
                                    
                                    x_nuevo = x_nido + math.cos(angulo) * radio
                                    y_nuevo = y_nido + math.sin(angulo) * radio
                                    egg.x = x_nuevo
                                    egg.y = y_nuevo

                                    break
                            break
        
            # Interacción con las tortugas cuando no estamos en la narrativa
            
            if estado_actual in [ESTADOS["juego_dia"]] and event.key == pygame.K_a: # R2
                following_turtles = check_collision(player, turtles)
                if following_turtles:
                    for turtle in following_turtles:
                        if not turtle.is_following_player:
                            turtle.is_following_player = True  # Comienza a seguir al jugador
                        else:
                            turtle.stop_following()  # Deja de seguir al jugador
                            turtle.is_visible = True

            # Atacar cuando apreta la tecla s
            #if not in_story and event.key == pygame.K_s:
            if estado_actual in [ESTADOS["juego_dia"]] and event.key == pygame.K_s: # R3
                for turtle in turtles:
                    if player.rect.colliderect(turtle.rect) & turtle.is_following_player:
                        turtle.attack()
                        turtle.is_following_player = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado_actual in [ESTADOS["juego_noche"]] and not start_time_noche:
                x_, y_ = event.pos
                #print(f"Click en {x_}, {y_}")
                create_or_remove_egg_pack(x_, y_)
        '''
        if event.type == pygame.KEYDOWN: #SOLO
            if event.key ==pygame.K_n:   # PARA
                start_time = time.time()  # Inicia el cronómetro después de la historia
                estado_actual = 4        # PRUEBAS
                start_time_dia = time.time()  # Inicia el cronómetro del dia luego que termine 
        if event.type == pygame.KEYDOWN: #SOLO
            if event.key ==pygame.K_m:   # PARA
                estado_actual = 3        # PRUEBAS
        '''

    
        
    # Generamos power-ups aleatorios despues de la historia y una sola vez
    # Manejo de los power-ups y cooldowns
    current_time = pygame.time.get_ticks()
    
    # Revisar si el jugador ha recogido un power-up solo si no hay un power-up activo
    #if not powerup_active and not in_story: 
    if not powerup_active and estado_actual in [ESTADOS["juego_dia"]]: #  R4
        powerup = check_collision_power(player, powerups)
        if powerup:
            # Activar el poder correspondiente si no está en cooldown
            if powerup.type == 'speed' and powerup_cooldowns['speed'] == 0:
                #print("Activando velocidad")
                player.velocidad = 9
                powerup_active = 'speed'
                powerup_start_time = current_time
                powerup_cooldowns['speed'] = 5000
            elif powerup.type == 'invisible_turtle_follower' and powerup_cooldowns['invisible_turtle_follower'] == 0:
                #print("Activando invisibilidad de tortugas")
                player.can_put_invisible = True
                powerup_active = 'invisible_turtle_follower'
                powerup_start_time = current_time
                powerup_cooldowns['invisible_turtle_follower'] = 5000
            elif powerup.type == 'turtle_speed' and powerup_cooldowns['turtle_speed'] == 0:
                #print("Activando velocidad de tortugas")
                player.can_speed_turtle_up = True
                powerup_active = 'turtle_speed'
                powerup_start_time = current_time
                powerup_cooldowns['turtle_speed'] = 5000
            
            powerup.apply_ability(player)

    # Mostrar el tiempo del power-up activo
    if powerup_active:
        time_left_powerup = max(0, powerup_duration - (current_time - powerup_start_time))  # Asegurarse de que el tiempo no sea negativo

        if time_left_powerup <= 0:  # Desactivar poder cuando haya pasado el tiempo
            powerup_active = None
            player.velocidad = 5  # Restablecer velocidad a su valor original
            player.can_put_invisible= False
            player.can_speed_turtle_up = False

            # Restablecer el cooldown del poder
            
            powerup_cooldowns['speed'] = 0
            powerup_cooldowns['invisible_turtle_follower'] = 0
            powerup_cooldowns['turtle_speed'] = 0
    
    # Lógica para power-ups 
    if current_time - last_powerup_spawn_time > power_interval and len(powerups) < 3:
        # Crear un nuevo power-up en una posición aleatoria
        new_powerup = Power(random.randint(100, WIDTH-200), random.randint(100, HEIGHT), "../assets/images/power_upps")
        powerups.add(new_powerup)
        last_powerup_spawn_time = current_time  # Actualizar el tiempo del ultimo power-up creado

    # Aparecer nuevas tortugas a intervalos regulares
    if current_time - last_turtle_spawn_time > turtle_spawn_interval and len(turtles) < max_turtles:
        # Crear una nueva tortuga en una posición aleatoria
        new_turtle = Turtle(random.randint(-50, -10), random.randint(100, HEIGHT - 100), "../assets/images/turtle_assets")
        turtles.add(new_turtle)
        last_turtle_spawn_time = current_time  # Actualizar el tiempo de la última tortuga creada

    #if not in_story:
    if estado_actual in [ESTADOS["juego_dia"]]:
        keys = pygame.key.get_pressed()

        # Mover al jugador
        player.move(keys)

        # Mover las tortugas
        for turtle in turtles:
            turtle.move(player)
            turtle.update()
        
        # Lógica de movimiento de los cangrejos
        for crab in crabs:
            crab.find_closest_turtle()
        
            # Atacamos cuando hay una tortuga objetivo y colisionemos con ella
            if crab.target_turtle and crab.rect.colliderect(crab.target_turtle.rect):
                #print("Colisión con tortuga")
                crab.attack()
            else:
                crab.stop_attack()

            crab.move()
            crab.update()

    # Dibujar todo
    screen.fill((0, 0, 0))
    if estado_actual in [ESTADOS["narrativa_dia"],ESTADOS["juego_dia"],ESTADOS["puntaje_final"],ESTADOS["puntaje_final_transicion"]]:
        draw_map_from_tmx(screen, tmx_map_dia) #Dibujamos el mapa de dia
    elif estado_actual in [ESTADOS["narrativa_inicio"],ESTADOS["narrativa_noche"],ESTADOS["juego_noche"],ESTADOS["puntaje_noche"],ESTADOS["puntaje_noche_transicion"]]:
        screen.blit(mapa_noche,(0,0)) # Dibujamos el mapa de noche
    # Dibujamos el tiempo restante del powerup

    if estado_actual in [ESTADOS["juego_noche"]]:
        #rint(f"linea 576 egg: {egg_packs}")
        if len(egg_packs.keys()) == max_egg_packs and not start_time_noche:
            #print("Has alcanzado el máximo de packs de huevos")
            start_time_noche = time.time()
            foxes = generate_random_fox(2,eggs)  # Iniciar con un zorro

            # Generar enemigos
            enemies = generate_random_enemy(2,eggs)

            
        else:
            # Dibujamos un letrero para indicar que se pueden crear packs de huevos
            if not start_time_noche:
                mostrar_letrero_personalizado(screen,len(egg_packs.keys()), max_egg_packs)
            pass

        # Verificamos que el zorro este cerca a un huevo
        for fox in foxes:
            for egg in eggs:
                if fox.rect.colliderect(egg.rect):
                    fox.attack()


        keys = pygame.key.get_pressed()

        # Mover al jugador
        player.move(keys)
        player.draw(screen)

        if egg_packs:
            # Dibujamos el nido
            for (x_nido,y_nido) in egg_packs.keys():
                draw_image(screen, path_nido, x_nido, y_nido)
        

        # Dibujamos los huevos
        for egg in eggs:
            if egg.is_visible:
                egg.update()
                egg.draw(screen)
        

        
        boton_perros.check_collision(player)
        boton_sirena.check_collision(player)
        boton_perros.update()
        boton_sirena.update()
        boton_perros.draw(screen)
        boton_sirena.draw(screen)

        # Verificamos colosiones con los enemigos
        for enemy in enemies:
            enemy.check_collision_egg()
        
        # Dibujamos los zorros
        for fox in foxes:
            if boton_perros.is_pressed: # Si el boton fue presionado haremos que los zorros huyan
                fox.huir()
            fox.move()
            fox.update()
            fox.draw(screen)
        
        # Dibujamos los enemigos
        for enemy in enemies:
            if boton_sirena.is_pressed:
                enemy.huir()
            enemy.move()
            enemy.update()
            enemy.draw(screen)

    if estado_actual in [ESTADOS["narrativa_dia"],ESTADOS["juego_dia"]]:
        # Dibujar tortugas
        for turtle in turtles:
            turtle.draw(screen)
        
        # Dibujar cangrejos
        for crab in crabs:
            crab.draw(screen)

        # Dibujar power-ups
        for powerup in powerups:
            powerup.update()
            powerup.draw(screen)
        

        player.draw(screen)

    # Dibujar el cuadro de diálogo si está activo
    
    dialogue_box.update()
    dialogue_box.draw(screen,color_fondo=color_fondo, color_letra=color_letra)
    

    
    # Dibujar el score y el tiempo 
    if start_time_noche:
        time_left = max(0, game_duration - int(time.time() - start_time_noche))
        if estado_actual == ESTADOS["narrativa_dia"]:
            time_left = 60
    if start_time_dia:
        time_left = max(0, game_duration - int(time.time() - start_time_dia))
    
    if estado_actual == ESTADOS["juego_noche"]:
        score = Egg.score
    elif estado_actual == ESTADOS["juego_dia"]:
        score = Turtle.score

    if estado_actual in [ESTADOS["juego_noche"],ESTADOS["narrativa_noche"],ESTADOS["narrativa_inicio"]]:
        path_three = '../assets/images/ui/frames/arbol.png'
        for j in range(690,711,20):
            for i in range(60, 390, 30):
                draw_image(screen, path_three,j,i)
    elif estado_actual == ESTADOS["puntaje_noche"]:
        # Muestra el cuadro de dialogo de noche
        dialogue_box.change_position((50,250))
        dialogue_box.set_text(f"Puntaje obtenido en nivel 1: {score}          Presiona Q para empezar el nivel 2")
        estado_actual = ESTADOS["puntaje_noche_transicion"]
    elif estado_actual == ESTADOS["puntaje_final"]:
        dialogue_box.change_position((50,250))
        score_total = Egg.score+Turtle.score
        dialogue_box.set_text(f"Puntaje total obtenido: {score_total}          Presiona Q para jugar de nuevo")
        estado_actual = ESTADOS["puntaje_final_transicion"]
    # Eliminamos el cuadro de score de la esquina superior cuando mostremos los puntajes finales de noche y final
    if estado_actual not in [ESTADOS["puntaje_noche"],ESTADOS["puntaje_noche_transicion"],ESTADOS["puntaje_final"],ESTADOS["puntaje_final_transicion"]]:
        draw_score(screen, score, time_left)
    # Dibujamos el tiempo restante del powerup
    draw_powerup_info(screen, powerup_active, time_left_powerup)  # Información del poder activo
    #if in_story:
    if estado_actual in [ESTADOS["narrativa_inicio"],ESTADOS["narrativa_dia"],ESTADOS["narrativa_noche"]]:
        screen.blit(narrador_sprite, (narrador_sprite_x, narrador_sprite_y))
    
    if start_time_noche and time_left <=0 and estado_actual == ESTADOS["puntaje_noche_terminado"]:
        estado_actual = ESTADOS["narrativa_dia"]
        color_fondo = '#e4fccc'
        color_letra = '#346c54'
        dialogue_box.letters_path = "../assets/images/ui/ascii/"

        # Cambiar la música cuando se inicia el juego de día
        pygame.mixer.music.stop()  # Detener la música actual
        pygame.mixer.music.load(path_musica_dia)  # Cargar la música de día
        pygame.mixer.music.play(loops=-1, start=0.0)  # Reproducir en bucle
        
        dialogue_box.set_text(story_dia[current_story_index_dia])
        
    if start_time_dia and start_time_noche and time_left<=0 and estado_actual != ESTADOS["puntaje_final_transicion"]:
        #running= False
        # MOSTRAR PUNTAJE FINAL AQUI
        estado_actual = ESTADOS["puntaje_final"]
        
    elif start_time_noche and time_left<=0 and estado_actual == ESTADOS["juego_noche"]:
        estado_actual = ESTADOS["puntaje_noche"]
    
    if estado_actual in [ESTADOS["menu"]]:
        screen.blit(gif_bg.get_frame(), (0, 0))  # Renderizar el fondo GIF
    
        #menu.mainloop(screen)
        current_menu.update(events)
        current_menu.draw(screen)
        #current_menu.mainloop(surface=screen)
        pygame.display.flip()
        clock.tick(60)
        estado_actual = TEMP["estado_actual"]
        #print("Estado actual",estado_actual)

        if estado_actual == 0:
            pygame.mixer.music.load(path_musica_noche)  # Ruta a tu archivo de música
            pygame.mixer.music.set_volume(0.5)  # Establece el volumen (opcional)
            pygame.mixer.music.play(loops=-1, start=0.0)
            pass
    
    
    pygame.display.flip()

            

