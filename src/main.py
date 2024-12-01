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

#MUSICA
# Inicializa el mixer de Pygame
pygame.mixer.init()

# Cargar la música
pygame.mixer.music.load("../assets/sounds/platformer_level03_loop.ogg")  # Ruta a tu archivo de música
pygame.mixer.music.set_volume(0.5)  # Establece el volumen (opcional)

# Sustituye map_data y ajusta draw_map
def draw_map_from_tmx(screen, tmx_data):
    for layer in tmx_data.visible_layers:  # Iterar por las capas visibles del mapa
        if hasattr(layer, "tiles"):  # Si la capa contiene tiles
            for x, y, tile_surface in layer.tiles():  # tile_surface es la imagen del tile
                if tile_surface is not None:  # Solo dibujar tiles válidos
                    screen.blit(tile_surface, (x * tmx_data.tilewidth, y * tmx_data.tileheight))



# Inicialización
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PC4: Guardianes de las Taricayas")
clock = pygame.time.Clock()

# Cargar un mapa con Tiled
tmx_map = load_pygame("../MapaDia.tmx")


# Instancia del narrador
narrador_assets_path = "../assets/images/narrator_assets/Amazon.png"
narrador_sprite = pygame.image.load(narrador_assets_path).convert_alpha()
narrador_sprite = pygame.transform.scale(narrador_sprite,(200,200))

# Posicion del narrador
narrador_sprite_x = 50 + 700 // 2 - narrador_sprite.get_width() // 2  # Basado en las dimensiones del cuadro de diálogo
narrador_sprite_y = 450 - narrador_sprite.get_height() - 10  # 10 píxeles encima del cuadro

# Instancia del jugador
player_assets_path = "../assets/images/player_assets"
player = Player(WIDTH // 2, HEIGHT // 2, player_assets_path, "../MapaDia.tmx")

# Crear el cuadro de diálogo dinámico
dialogue_box = DialogueBox(
    letters_path="../assets/images/ui/ascii",
    position=(50, 450),
    text_speed=0.5,
    box_width=700,
    box_height=120,
    letter_size=(16, 16)
)

story = load_story_from_json('../history.json')


# Tortugas: generadas aleatoriamente
turtles = pygame.sprite.Group()

# En el ciclo principal:
powerups = pygame.sprite.Group()  # Grupo de power-ups

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
        x = random.randint(200, WIDTH-200)  # Evita las zonas del mar
        y = random.randint(200, HEIGHT-200)
        
        powerup = Power(x, y, "../assets/images/power_upps")
        powerups.add(powerup)


# Añadir las tortugas al grupo al inicio
generate_random_turtle(12)  # Iniciar con una tortuga

# Añadir los power-ups al grupo al inicio
generate_random_powerup(3)  # Iniciar con 3 power-ups


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
            powerup.apply_ability(player)
            return powerup
    return None



# Variables globales para el puntaje y tiempo
score = 0
start_time = None
time_left = 60  # 60 segundos para completar la misión



def main():
    global following_turtle, score, time_left, start_time  # Usamos la variable global para modificarla dentro del ciclo principal

    # Reproducir música (en loop infinito)
    pygame.mixer.music.play(loops=-1, start=0.0)  # loops=-1 para repetir la música infinitamente

    running = True
    in_story = True  # Variable para controlar si estamos en la narrativa inicial
    current_story_index = 0  # Variable local para manejar el índice de la narrativa
    dialogue_box.set_text(story[current_story_index])  # Establecer el primer texto

    # Variables para controlar el tiempo y la aparición de tortugas
    last_turtle_spawn_time = 0  # Tiempo de la última aparición de tortuga
    turtle_spawn_interval = 3000  # Intervalo en milisegundos (3 segundos)
    
    max_turtles = 25  # Máximo número de tortugas en pantalla

    start_time = None  # Inicia el cronómetro después de la historia
    game_duration = 60  # Duración del juego en segundos
    x_, y_ = 0, 0  # Inicializar las variables x_ y y_

    #Intervalo de los power-ups
    power_interval = 3000  # Tiempo de la última aparición de power-up
    last_powerup_spawn_time = 0  # Intervalo en milisegundos (3 segundos)

    # Variable para controlar el intervalo de activación de la habilidad de atraer tortugas
    last_attract_time = 0  # Inicializamos la variable que controla el tiempo de activación de la habilidad
    attract_interval = 5000  # Intervalo en milisegundos (5 segundos) para la habilidad de atraer tortugas

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if in_story:
                    if event.key == pygame.K_q:  # Avanza la narrativa con la tecla Q
                        if current_story_index < len(story) - 1:
                            current_story_index += 1
                            dialogue_box.set_text(story[current_story_index])
                        else:
                            in_story = False  # Termina la narrativa
                            dialogue_box.hide()
                            start_time = time.time()  # Inicia el cronómetro después de la historia
                    elif event.key == pygame.K_SPACE:  # Salta la narrativa
                        dialogue_box.hide()
                        in_story = False
                        start_time = time.time()  # Inicia el cronómetro después de la historia

                # Interacción con las tortugas cuando no estamos en la narrativa
                if not in_story and event.key == pygame.K_a:
                    following_turtles = check_collision(player, turtles)
                    if following_turtles:
                        for turtle in following_turtles:
                            if not turtle.is_following_player:
                                turtle.is_following_player = True  # Comienza a seguir al jugador
                            else:
                                turtle.stop_following()  # Deja de seguir al jugador

                if not in_story and event.key == pygame.K_s:
                    following_turtles = check_collision(player, turtles)
                    if following_turtles:
                        for turtle in following_turtles:
                            turtle.attack()  # Las tortugas atacan
                            turtle.is_following_player = False  # Dejan de seguir al jugador
                    following_turtle = None  # Reseteamos la variable

        # Lógica para generar tortugas a intervalos regulares
        current_time = pygame.time.get_ticks()  # Obtiene el tiempo transcurrido desde que se inició el juego

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

        if not in_story:
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
                    print("Colisión con tortuga")
                    crab.attack()
                else:
                    crab.stop_attack()
                crab.move()
                crab.update()

            
            # Verificar colisiones con el power app
            powerup = check_collision_power(player, powerups)
            if powerup:
                print("Colisión con power-up")
                powerup.apply_ability(player)
                # Eliminar el power-up si fue recogido
                powerups.remove(powerup)
            
            # Si el jugador puede atraer tortugas, atraerlas pero solo una vez por intervalo
            if player.can_get_turtles and current_time - last_attract_time > attract_interval:
                player.attract_turtles(turtles)
                player.can_get_turtles = False
                last_attract_time = current_time  # Actualizar el tiempo de la última vez que se activó la habilidad
            
            if player.can_speed_turtle_up:
                player.speed_up_turtles(turtles)
            
        # Dibujar todo
        screen.fill((0, 0, 0))

        draw_map_from_tmx(screen, tmx_map)
        player.draw(screen)

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

        # Dibujar el cuadro de diálogo si está activo
        dialogue_box.update()
        dialogue_box.draw(screen)
    
        # Dibujar el score y el tiempo
        if start_time:
            time_left = max(0, game_duration - int(time.time() - start_time))

        score = Turtle.score
        draw_score(screen, score, time_left)

        if start_time and time_left <= 0:
            running = False  # Terminar el juego después de 60 segundos

        if in_story:
            screen.blit(narrador_sprite, (narrador_sprite_x, narrador_sprite_y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
