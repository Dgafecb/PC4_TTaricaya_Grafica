import pygame
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
#MUSICA
# Inicializa el mixer de Pygame
pygame.mixer.init()


path_musica_dia = '../assets/sounds/platformer_level03_loop.ogg'
path_musica_noche = '../assets/sounds/fantasy Dragon.ogg'

# Cargar la música
pygame.mixer.music.load(path_musica_noche)  # Ruta a tu archivo de música
pygame.mixer.music.set_volume(0.5)  # Establece el volumen (opcional)

# Inicialización
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PC4: Guardianes de las Taricayas")
clock = pygame.time.Clock()

# CArgar un mapa con Tiled de dia
tmx_map_dia = load_pygame("../MapaDia.tmx")
mapa_dia = pygame.image.load("../MapaDia.png").convert_alpha()
# Cargar un mapa con Tiled de noche
tmx_map_noche = load_pygame("../MapaNoche.tmx")
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
    letters_path="../assets/images/ui/ascii",
    position=(50, 450),
    text_speed=0.5,
    box_width=700,
    box_height=120,
    letter_size=(16, 16)
)
story = load_story_from_json('../history.json')
story_noche = load_story_from_json("../history.json", "story_noche")
story_dia = load_story_from_json("../history.json", "story_dia")

# Tortugas: generadas aleatoriamente
turtles = pygame.sprite.Group()

# En el ciclo principal:
powerups = pygame.sprite.Group()  # Grupo de power-ups

# Zorros: generados aleatoriamente
foxes = pygame.sprite.Group()

# Huevos: generados aleatoriamente
eggs = pygame.sprite.Group()

# Función para crear tortugas aleatorias
def generate_random_turtle(n):
    for _ in range(n):
        x = random.randint(-50, -10)
        y = random.randint(100, HEIGHT - 100)
        turtle = Turtle(x, y, "../assets/images/turtle_assets")
        turtles.add(turtle)

# Función para generar power-ups aleatorios en posiciones válidas
def generate_random_powerup(n):
    for _ in range(n):
        # Generar una posición aleatoria en el rango que no esté en el mar (a la izquierda)
        x = random.randint(100, WIDTH-500)  # Evita las zonas del mar
        y = random.randint(100, HEIGHT-200)
        
        powerup = Power(x, y, "../assets/images/power_upps")
        powerups.add(powerup)

# Función para generar zorros aleatorios
def generate_random_fox(n):
    for _ in range(n):
        # A la derecha
        x = WIDTH + 100

        y = random.randint(100, HEIGHT - 100)
        fox = Fox("../assets/images/fox_assets", eggs)
        foxes.add(fox)
# Lista para almacenar las posiciones de los huevos generados
egg_positions_individual = []  # Almacena las posiciones de los huevos generados

# Añadir las tortugas al grupo al inicio
generate_random_turtle(12)  # Iniciar con una tortuga




# Lista de cangrejos
crabs = pygame.sprite.Group()
for _ in range(4):  # Por ejemplo, 3 cangrejos
    crab_asset_path = "../assets/images/crab_assets"
    crab = Crab(crab_asset_path, turtles)
    crabs.add(crab)
              

# Agrega una variable para saber si el jugador está siguiendo una tortuga
following_turtle = None

def check_collision(player, turtles):
    """Verifica si el jugador está colisionando con alguna tortuga y retorna todas las que están colisionando."""
    following_turtles = []  # Lista de tortugas que están colisionando con el jugador
    for turtle in turtles:
        if player.rect.colliderect(turtle.rect):  # Verificamos si el jugador está colisionando con la tortuga
            following_turtles.append(turtle)
    return following_turtles


def check_collision_power(player, powerups):
    """Verifica si el jugador está colisionando con algún power-up."""
    for powerup in powerups:
        if player.rect.colliderect(powerup.rect):
            return powerup
    return None

# Creamos una lista de packs
egg_packs = {}

# Función para generar huevos en un patrón circular
def generate_pack_egg(x, y, n):
    """Genera un pack de huevos en una posición (x, y) en un patrón circular"""
    radio = 30  # Ajusta este valor dependiendo de qué tan dispersos quieres los huevos
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
        egg = Egg(egg_x, egg_y, "../assets/images/egg_assets")
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
        if distancia <= 30:  # Si está dentro del radio del pack (ajustar el radio según sea necesario)
            print(f"Eliminando huevos en el pack en ({pack_x}, {pack_y})")
            remove_eggs_in_pack(pack_x, pack_y)  # Eliminar los huevos del pack
            break
    else:
        # Si no hay un pack en esta posición y no hemos alcanzado el máximo de 5
        if len(egg_packs) < max_egg_packs:
            print("Creando un nuevo pack de huevos")
            generate_pack_egg(x, y, 5)  # Crear un nuevo pack de huevos
        
# Variables globales
max_egg_packs = 5  # Número máximo de packs de huevos generados


# Variables globales para el puntaje y tiempo
score = 0
start_time = None
start_time_dia = None
start_time_noche =None
time_left = 60  # 60 segundos para completar la misión

# Instancia del jugador
player_assets_path = "../assets/images/player_assets"
player = Player(WIDTH // 2, HEIGHT // 2, player_assets_path, "../MapaDia.tmx", turtles, crabs)
 # estados del juego
ESTADOS = {"narrativa_inicio":0,"narrativa_noche":1, "juego_noche":2, "narrativa_dia":3, "juego_dia":4}
# estado actual del juego
estado_actual = ESTADOS["narrativa_inicio"]# 0 
def main():
    global following_turtle, score, time_left, start_time,start_time_dia,estado_actual, start_time_noche  # Usamos la variable global para modificarla dentro del ciclo principal
   
    
    # Reproducir música (en loop infinito)
    pygame.mixer.music.play(loops=-1, start=0.0)  # loops=-1 para repetir la música infinitamente

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

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
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
                            
                            
                    elif event.key == pygame.K_SPACE:  # Salta la narrativa
                        dialogue_box.hide()
                        #in_story = False
                        estado_actual = ESTADOS["juego_dia"] #Para que pueda iniciar el juego de noche
                        start_time_dia = time.time()
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
                    print(f"Click en {x_}, {y_}")
                    create_or_remove_egg_pack(x_, y_)
         
            if event.type == pygame.KEYDOWN: #SOLO
                if event.key ==pygame.K_n:   # PARA
                    start_time = time.time()  # Inicia el cronómetro después de la historia
                    estado_actual = 4        # PRUEBAS
                    start_time_dia = time.time()  # Inicia el cronómetro del dia luego que termine 
            if event.type == pygame.KEYDOWN: #SOLO
                if event.key ==pygame.K_m:   # PARA
                    estado_actual = 3        # PRUEBAS
                    
      
      
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
                    print("Activando velocidad")
                    player.velocidad = 10
                    powerup_active = 'speed'
                    powerup_start_time = current_time
                    powerup_cooldowns['speed'] = 5000
                elif powerup.type == 'invisible_turtle_follower' and powerup_cooldowns['invisible_turtle_follower'] == 0:
                    print("Activando invisibilidad de tortugas")
                    player.can_put_invisible = True
                    powerup_active = 'invisible_turtle_follower'
                    powerup_start_time = current_time
                    powerup_cooldowns['invisible_turtle_follower'] = 5000
                elif powerup.type == 'turtle_speed' and powerup_cooldowns['turtle_speed'] == 0:
                    print("Activando velocidad de tortugas")
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
        if estado_actual in [ESTADOS["narrativa_dia"],ESTADOS["juego_dia"]]:
            draw_map_from_tmx(screen, tmx_map_dia) #Dibujamos el mapa de dia
        elif estado_actual in [ESTADOS["narrativa_inicio"],ESTADOS["narrativa_noche"],ESTADOS["juego_noche"]]:
            screen.blit(mapa_noche,(0,0)) # Dibujamos el mapa de noche
        # Dibujamos el tiempo restante del powerup

        if estado_actual in [ESTADOS["juego_noche"]]:
            if len(egg_packs.keys()) == max_egg_packs and not start_time_noche:
                print("Has alcanzado el máximo de packs de huevos")
                start_time_noche = time.time()
                generate_random_fox(2)  # Iniciar con un zorro

            # Verificamos que el zorro este cerca a un huevo
            for fox in foxes:
                for egg in eggs:
                    if fox.rect.colliderect(egg.rect):
                        print("Zorro colisionando con huevo")
                        fox.attack()


            # Dibujamos los huevos
            for egg in eggs:
                egg.update()
                egg.draw(screen)

            # Dibujamos los zorros
            for fox in foxes:
                fox.move()
                fox.update()
                fox.draw(screen)

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
        dialogue_box.draw(screen)
        
        # Dibujar el score y el tiempo
        
        if start_time_noche:
            time_left = max(0, game_duration - int(time.time() - start_time_noche))
            if estado_actual == ESTADOS["narrativa_dia"]:
                time_left = 60
        if start_time_dia:
            time_left = max(0, game_duration - int(time.time() - start_time_dia))
        

        score = Turtle.score
        draw_score(screen, score, time_left)
        # Dibujamos el tiempo restante del powerup
        draw_powerup_info(screen, powerup_active, time_left_powerup)  # Información del poder activo
        #if in_story:
        if estado_actual in [ESTADOS["narrativa_inicio"],ESTADOS["narrativa_dia"],ESTADOS["narrativa_noche"]]:
            screen.blit(narrador_sprite, (narrador_sprite_x, narrador_sprite_y))
        
        if start_time_noche and time_left <=0:
            estado_actual = ESTADOS["narrativa_dia"]

            # Cambiar la música cuando se inicia el juego de día
            pygame.mixer.music.stop()  # Detener la música actual
            pygame.mixer.music.load(path_musica_dia)  # Cargar la música de día
            pygame.mixer.music.play(loops=-1, start=0.0)  # Reproducir en bucle
            
            dialogue_box.set_text(story_dia[current_story_index_dia])
            if start_time_dia:
                running= False
                # MOSTRAR PUNTAJE FINAL AQUI
        pygame.display.flip()
              

if __name__ == "__main__":
    main()
