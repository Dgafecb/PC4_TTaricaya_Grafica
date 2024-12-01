import pygame
import json
from settings import WIDTH, HEIGHT

def load_image(path, scale=None):
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

def load_tileset(image_path, tile_width, tile_height, scale=None):
    """Divide el tileset en tiles individuales y los escala si es necesario."""
    tiles = []
    tileset = pygame.image.load(image_path).convert_alpha()
    tileset_width, tileset_height = tileset.get_size()

    for row in range(0, tileset_height, tile_height):
        for col in range(0, tileset_width, tile_width):
            tile = tileset.subsurface((col, row, tile_width, tile_height))
            if scale:
                tile = pygame.transform.scale(tile, (scale[0], scale[1]))
            tiles.append(tile)

    return tiles


# Función para dibujar el mapa
def draw_map(screen, map_data, tiles, tile_width, tile_height):
    """Dibuja el mapa en la pantalla directamente con índices."""
    for row_index, row in enumerate(map_data):
        for col_index, tile_index in enumerate(row):
            if tile_index >= 0:  # Evitar índices negativos (espacios vacíos)
                x = col_index * tile_width
                y = row_index * tile_height
                screen.blit(tiles[tile_index], (x, y))


def load_story_from_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data["story"]  # Devuelve la lista de textos


# Función para dibujar el puntaje y el cronómetro
def draw_score(screen, score, time_left):
    font = pygame.font.Font(None, 36)  # Asegúrate de que la fuente esté correctamente cargada
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = font.render(f"Time: {time_left}s", True, (255, 255, 255))

    # Dibujar un cuadro de fondo para el puntaje
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, 250, 60))  # Fondo con espacio para puntaje y tiempo
    pygame.draw.rect(screen, (255, 255, 255), (10, 10, 250, 60), 2)  # Borde del cuadro

    # Dibujar el puntaje y el tiempo dentro del cuadro
    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (20, 40))


# Función para iniciar el temporizador (devuelve el tiempo actual en milisegundos)
def start_timer():
    return pygame.time.get_ticks()

def load_sprite(image_path, width=None, height=None):
    """
    Carga un sprite de una imagen y opcionalmente la escala a un tamaño específico.
    
    :param image_path: Ruta al archivo de imagen.
    :param width: Ancho deseado para la imagen (opcional).
    :param height: Alto deseado para la imagen (opcional).
    :return: El sprite cargado (y escalado si se especifica).
    """
    # Cargar la imagen
    sprite = pygame.image.load(image_path).convert_alpha()
    
    # Si se proporcionan ancho y alto, escalamos la imagen
    if width and height:
        sprite = pygame.transform.scale(sprite, (width, height))
    
    return sprite



# Función para dibujar la información del poder activo
def draw_powerup_info(screen, powerup_active, elapsed_time):
    font = pygame.font.Font(None, 36)  # Mantener el tamaño de la fuente original
    
    # Colores para diferentes estados del poder
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)

    # Determinar el texto y el color según el poder activo
    if powerup_active:
        # Determinar el texto basado en el poder activo
        if powerup_active == 'speed':
            powerup_text = "Speed Boost"
            color = green
        elif powerup_active == 'invisible_turtle_follower':
            powerup_text = "Invisible Turtle Follower"
            color = green
        elif powerup_active == 'turtle_speed':
            powerup_text = "Turtle Speed Up"
            color = green
        else:
            powerup_text = "Unknown Power"
            color = red
        
        # Calcular el tiempo restante (en segundos)
        time_remaining = max(0, 5 - (elapsed_time / 1000))  # 5 segundos de duración (ajusta según lo que necesites)
        time_text = f"Time Left: {int(time_remaining)}s"  # Convertir a un número entero para la visualización
        
        # Renderizar el texto del poder activo y el tiempo restante
        powerup_render = font.render(powerup_text, True, white)
        time_render = font.render(time_text, True, white)
        
        # Calcular el ancho del texto para ajustar el fondo
        powerup_width = powerup_render.get_width() + 20  # Añadir margen para el texto
        time_width = time_render.get_width() + 20
        box_width = max(powerup_width, time_width)  # Tomar el mayor de los dos anchos para el cuadro
        
        # Dibujar fondo para el texto (ajustar el tamaño del cuadro según el texto)
        pygame.draw.rect(screen, black, (WIDTH - box_width - 10, 10, box_width + 20, 120))  # Cuadro de fondo ajustado
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - box_width - 10, 10, box_width + 20, 120), 4)  # Borde del cuadro
        
        # Dibujar los textos en la pantalla
        screen.blit(powerup_render, (WIDTH - box_width, 20))  # Dibujar el nombre del poder
        screen.blit(time_render, (WIDTH - box_width, 60))  # Dibujar el tiempo restante
        
    else:
        # Si no hay power-up activo, no mostrar nada
        return


