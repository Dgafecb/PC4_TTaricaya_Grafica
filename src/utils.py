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


def load_story_from_json(filename, story_type="story"):
    with open(filename, "r") as file:
        data = json.load(file)
    
    # Verifica si el tipo de historia es válido y lo carga
    if story_type in data:
        return data[story_type]
    else:
        raise ValueError(f"Tipo de historia '{story_type}' no encontrado en el archivo JSON.")


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


def draw_powerup_info(screen, powerup_active, time_left_powerup):
    font = pygame.font.Font(None, 24)  # Tamaño de fuente para el tiempo
    small_font = pygame.font.Font(None, 20)  # Fuente más pequeña para la descripción corta
    
    # Colores
    white = (255, 255, 255)
    green = (0, 255, 0)
    black = (0, 0, 0)
    
    # Diccionario de imágenes y descripciones
    powerup_path = {
        "speed": {"image": "../assets/images/power_upps/crystal_01.png", "desc": "Boosts speed"},
        "invisible_turtle_follower": {"image": "../assets/images/power_upps/potion_01.png", "desc": "Invisible follower"},
        "turtle_speed": {"image": "../assets/images/power_upps/herb_02.png", "desc": "Increases turtle speed"}
    }
    
    if powerup_active:
        # Obtener la descripción y la imagen del powerup
        powerup_info = powerup_path.get(powerup_active, {"image": None, "desc": "Unknown Power"})
        powerup_text = powerup_info["desc"]
        powerup_image_path = powerup_info["image"]
        powerup_image = pygame.image.load(powerup_image_path).convert_alpha()
        time_left_powerup /= 1000  # Convertir a segundos
        # redodear superiormente
        time_left_powerup = round(time_left_powerup + 0.5)
        time_text = f"Time Left: {int(time_left_powerup)}s"
        
        # Renderizar los textos
        powerup_render = small_font.render(powerup_text, True, white)
        time_render = font.render(time_text, True, white)
        
        # Ajustar tamaño de la imagen
        powerup_image = pygame.transform.scale(powerup_image, (40, 40))  # Tamaño fijo de la imagen
        
        # Ajuste de tamaño de la caja
        box_width = 220
        box_height = 120
        
        # Dibujar fondo para el cuadro
        pygame.draw.rect(screen, black, (WIDTH - box_width - 10, 10, box_width, box_height))  # Fondo
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - box_width - 10, 10, box_width, box_height), 4)  # Borde
        
        # Centrar la imagen y los textos dentro del cuadro
        image_x = WIDTH - box_width + (box_width - 40) // 2  # Centrar imagen
        image_y = 20  # Posición vertical de la imagen
        
        powerup_text_x = WIDTH - box_width + (box_width - powerup_render.get_width()) // 2  # Centrar texto de descripción
        powerup_text_y = image_y + 45  # Colocar debajo de la imagen
        
        time_text_x = WIDTH - box_width + (box_width - time_render.get_width()) // 2  # Centrar tiempo
        time_text_y = powerup_text_y + 30  # Colocar debajo de la descripción
        
        # Dibujar la imagen, la descripción y el tiempo restante
        screen.blit(powerup_image, (image_x, image_y))  # Dibujar imagen
        screen.blit(powerup_render, (powerup_text_x, powerup_text_y))  # Dibujar descripción
        screen.blit(time_render, (time_text_x, time_text_y))  # Dibujar tiempo restante
        
    else:
        # Si no hay power-up activo, no mostrar nada
        return
    
def draw_instructions(screen, instructions):
    font = pygame.font.Font(None, 24)  # Tamaño de fuente para las instrucciones
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    # Ajuste de tamaño de la caja
    box_width = 220
    box_height = 120
    
    # Ubicar el cuadro en la esquina superior derecha
    x = WIDTH - box_width - 10
    y = 10

    # Dibujar fondo para el cuadro
    pygame.draw.rect(screen, black, (x, y, box_width, box_height))  # Fondo
    pygame.draw.rect(screen, white, (x, y, box_width, box_height), 4)  # Borde

    # Dibujar las instrucciones
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, white)
        text_x = x + (box_width - text.get_width()) // 2
        text_y = y + 10 + i * 30
        screen.blit(text, (text_x, text_y))
