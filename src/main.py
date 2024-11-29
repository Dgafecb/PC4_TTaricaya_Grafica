import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from utils import load_tileset, draw_map
from dialogue import DialogueBox  # Importa el cuadro de diálogo
from pytmx import load_pygame
from utils import load_story_from_json
from turtles import Turtle
import random

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

# Lista de tortugas
turtles = pygame.sprite.Group()

# Generar tortugas aleatorias
for _ in range(5):
    turtle = Turtle(random.randint(-50, -10), random.randint(100, HEIGHT - 100), "../assets/images/turtle_assets")
    turtles.add(turtle)

# Agrega una variable para saber si el jugador está siguiendo una tortuga
following_turtle = None

def check_collision(player, turtles):
    """Verifica si el jugador está colisionando con alguna tortuga."""
    for turtle in turtles:
        # Verificamos si el jugador colisiona con la tortuga y a apretado la tecla A
        if player.rect.colliderect(turtle.rect):
            return turtle
    return None

def main():
    global following_turtle  # Usamos la variable global para modificarla dentro del ciclo principal

    # Reproducir música (en loop infinito)
    pygame.mixer.music.play(loops=-1, start=0.0)  # loops=-1 para repetir la música infinitamente

    running = True
    in_story = True  # Variable para controlar si estamos en la narrativa inicial
    current_story_index = 0  # Variable local para manejar el índice de la narrativa
    dialogue_box.set_text(story[current_story_index])  # Establecer el primer texto

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
                    elif event.key == pygame.K_SPACE:  # Salta la narrativa
                        dialogue_box.hide()
                        in_story = False

                # Interacción con las tortugas cuando no estamos en la narrativa
                if not in_story and event.key == pygame.K_a:
                    if following_turtle:
                        following_turtle.is_following_player = False                        
                        following_turtle = None
                    else:
                        following_turtle = check_collision(player, turtles)
                        if following_turtle:
                            following_turtle.is_following_player = True
                if not in_story and event.key == pygame.K_s:
                    if following_turtle:
                        following_turtle.attack()
                        following_turtle.stop_following()
                        following_turtle = None
                


        if not in_story:
            keys = pygame.key.get_pressed()

            # Mover al jugador
            player.move(keys)

            # Mover las tortugas
            for turtle in turtles:
                turtle.move(player)
                turtle.update()

        # Dibujar todo
        screen.fill((0, 0, 0))

        draw_map_from_tmx(screen, tmx_map)
        player.draw(screen)

        # Dibujar tortugas
        for turtle in turtles:
            turtle.draw(screen)

        # Dibujar el cuadro de diálogo si está activo
        dialogue_box.update()
        dialogue_box.draw(screen)
        # Dibujar el narrador encima del cuadro de diálogo
        if in_story:
            screen.blit(narrador_sprite, (narrador_sprite_x, narrador_sprite_y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
