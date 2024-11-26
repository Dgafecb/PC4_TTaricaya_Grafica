import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from utils import load_tileset, draw_map
from dialogue import DialogueBox  # Importa el cuadro de diálogo

# Inicialización
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PC4: Guardianes de las Taricayas")
clock = pygame.time.Clock()

# Cargar tilesets
tileset_path_main = "../assets/images/escenes/gentle forest v01.png"
tileset_path_walls = "../assets/images/escenes/gentle tree wall.png"

# Cargar tiles sin escalado
tiles_main = load_tileset(tileset_path_main, 32, 32)  # Carga en tamaño original (32x32)
tiles_walls = load_tileset(tileset_path_walls, 32, 32)

# Combinar todos los tiles en una lista
tiles = tiles_main + tiles_walls

# Crear un mapa directamente con índices de tiles
map_data = [
    [0, 1, 41, 41, 41, 0, 1, 41, 41, 41],  # Índices para tierra y agua
    [64, 64, 42, 0, 0, 64, 64, 42, 0, 0],  # Paredes de árboles del tileset walls
    [16, 17, 17, 17, 65, 16, 17, 17, 17, 65],  # Mezcla de troncos y paredes
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],         # Piso normal
    [12, 0, 1, 12, 12, 12, 0, 1, 12, 12],   # Elementos adicionales
]

# Instancia del jugador
player_assets_path = "../assets/images/player_assets"
player = Player(WIDTH // 2, HEIGHT // 2, player_assets_path)

# Crear el cuadro de diálogo dinámico
dialogue_box = DialogueBox(
    letters_path="../assets/images/ui/ascii",
    position=(50, 450),
    text_speed=0.5,
    box_width=700,
    box_height=120,
    letter_size=(16, 16)  # Cambia el tamaño de las letras si es necesario
)

# Narrativa inicial del juego
story = [
    "Bienvenido a la Reserva Nacional Pacaya-Samiria.",
    "Eres un guardián encargado de proteger las taricayas.",
    "Debes evitar a los depredadores y asegurar la supervivencia."
]


def main():
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

        # Movimiento del jugador solo si la narrativa inicial terminó
        if not in_story:
            keys = pygame.key.get_pressed()
            player.move(keys)

        # Dibujar todo
        screen.fill((0, 0, 0))
        draw_map(screen, map_data, tiles, 32, 32)  # Usa el tamaño original (32x32)
        player.draw(screen)

        # Dibujar el cuadro de diálogo si está activo
        dialogue_box.update()
        dialogue_box.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
