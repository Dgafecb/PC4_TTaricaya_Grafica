import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla (necesaria para operaciones gráficas)
TILE_WIDTH = 32  # Cambia según el tamaño de tus tiles
TILE_HEIGHT = 32
SCALE = 2  # Para escalar los tiles y que sean más visibles
TILE_WIDTH_SCALED = TILE_WIDTH * SCALE
TILE_HEIGHT_SCALED = TILE_HEIGHT * SCALE

# Ruta del tileset
TILESET_PATH = "../assets/images/escenes/gentle forest v01.png"  # Cambia la ruta según tu proyecto

# Inicializa una ventana temporal para cargar el tileset
screen = pygame.display.set_mode((1, 1))

# Cargar tileset
tileset = pygame.image.load(TILESET_PATH).convert_alpha()
tileset_width, tileset_height = tileset.get_size()

# Calcular dimensiones de la ventana
WINDOW_WIDTH = tileset_width * SCALE
WINDOW_HEIGHT = tileset_height * SCALE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Inicializa la ventana con el tamaño correcto
pygame.display.set_caption("Visualizador de Tileset")

# Función para dividir el tileset en tiles individuales
def load_tileset(tileset, tile_width, tile_height, scale=None):
    tiles = []
    tileset_width, tileset_height = tileset.get_size()

    for row in range(0, tileset_height, tile_height):
        for col in range(0, tileset_width, tile_width):
            tile = tileset.subsurface((col, row, tile_width, tile_height))
            if scale:
                tile = pygame.transform.scale(tile, (tile_width * scale, tile_height * scale))
            tiles.append(tile)
    return tiles

# Dividir el tileset
tiles = load_tileset(tileset, TILE_WIDTH, TILE_HEIGHT, SCALE)

# Función para dibujar los tiles con índices
def draw_tileset_with_indices(screen, tiles, tile_width, tile_height):
    font = pygame.font.SysFont("Arial", 16)  # Fuente para los índices
    for index, tile in enumerate(tiles):
        # Calcular la posición en la cuadrícula
        col = index % (WINDOW_WIDTH // tile_width)
        row = index // (WINDOW_WIDTH // tile_width)
        x = col * tile_width
        y = row * tile_height

        # Dibujar el tile
        screen.blit(tile, (x, y))

        # Dibujar el índice
        text = font.render(str(index), True, (255, 255, 255))
        screen.blit(text, (x + 5, y + 5))  # Posición del texto dentro del tile

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el tileset con índices
    screen.fill((0, 0, 0))  # Fondo negro
    draw_tileset_with_indices(screen, tiles, TILE_WIDTH_SCALED, TILE_HEIGHT_SCALED)
    pygame.display.flip()

pygame.quit()
sys.exit()
