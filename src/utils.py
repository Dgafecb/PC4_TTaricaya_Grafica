from libraries import *

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

def mostrar_letrero_personalizado(screen, current_egg_packs, max_egg_packs):
    # Crear la fuente internamente dentro de la función
    font = pygame.font.SysFont('Arial', 20)
    
    # Establecer el mensaje dependiendo de la cantidad de packs
    if current_egg_packs < max_egg_packs:
        mensaje = f"Puedes ingresar huevos (click). Packs actuales: {current_egg_packs}/{max_egg_packs}"
    else:
        mensaje = f"¡Has alcanzado el máximo de packs de huevos!"
    
    # Colores personalizables
    color_texto = (255, 255, 255)  # Blanco para el texto
    color_fondo = (0, 0, 0)  # Fondo negro
    color_borde = (255, 165, 0)  # Borde naranja (puedes cambiar a cualquier color que te guste)
    
    # Tamaño y márgenes del cuadro de texto
    margen = 15
    texto = font.render(mensaje, True, color_texto)
    texto_rect = texto.get_rect(center=(screen.get_width() // 2, 100 ))

    # Crear el fondo del letrero (con bordes redondeados)
    cuadro_rect = texto_rect.inflate(margen, margen)
    
    # Fondo con borde
    pygame.draw.rect(screen, color_borde, cuadro_rect, border_radius=15)
    pygame.draw.rect(screen, color_fondo, texto_rect.inflate(margen, margen), border_radius=15)

    # Dibujar el texto en el centro del letrero
    screen.blit(texto, texto_rect)


def draw_image(screen, image_path, x, y, scale=None):
    """
    Dibuja una imagen en la pantalla en las coordenadas (x, y).
    
    :param screen: La superficie en la que se dibujará la imagen.
    :param image_path: Ruta al archivo de imagen.
    :param x: Coordenada X donde se dibujará la imagen.
    :param y: Coordenada Y donde se dibujará la imagen.
    :param scale: (Opcional) Una tupla con las nuevas dimensiones (ancho, alto) para redimensionar la imagen.
    """
    # Cargar la imagen
    image = load_image(image_path, scale)
    
    # Dibujar la imagen en las coordenadas especificadas
    screen.blit(image, (x, y))


# Funcion agregada para imprimir texto letra por letra
def imprimir_letras(surface, texto, color, x, y, font, interval=30):
    """
    Función para mostrar texto letra por letra con un intervalo entre cada letra.
    :param surface: superficie en la que se dibujará el texto.
    :param texto: texto que se va a mostrar.
    :param color: color del texto.
    :param x: posición en x donde se dibuja el texto.
    :param y: posición en y donde se dibuja el texto.
    :param font: fuente del texto.
    :param interval: intervalo entre cada letra en milisegundos.
    """
    for i in range(len(texto)):
        text_surface = font.render(texto[:i+1], True, color)
        surface.blit(text_surface, (x, y))
        pygame.display.update()
        pygame.time.wait(interval)

# Sustituye map_data y ajusta draw_map
def draw_map_from_tmx(screen, tmx_data):
    for layer in tmx_data.visible_layers:  # Iterar por las capas visibles del mapa
        if hasattr(layer, "tiles"):  # Si la capa contiene tiles
            for x, y, tile_surface in layer.tiles():  # tile_surface es la imagen del tile
                if tile_surface is not None:  # Solo dibujar tiles válidos
                    screen.blit(tile_surface, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

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

def init_objects():
    turtles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    foxes = pygame.sprite.Group()
    eggs = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    return turtles, powerups, foxes, eggs, enemies

def generate_random_turtle(n):
    turtles = pygame.sprite.Group()
    for _ in range(n):
        x = random.randint(-50, -10)
        y = random.randint(100, HEIGHT - 100)
        turtle = Turtle(x, y, "../assets/images/turtle_assets")
        turtles.add(turtle)
    return turtles

# Función para generar power-ups aleatorios en posiciones válidas
def generate_random_powerup(n):
    powerups = pygame.sprite.Group()
    for _ in range(n):
        # Generar una posición aleatoria en el rango que no esté en el mar (a la izquierda)
        x = random.randint(100, WIDTH-500)  # Evita las zonas del mar
        y = random.randint(100, HEIGHT-200)
        
        powerup = Power(x, y, "../assets/images/power_upps")
        powerups.add(powerup)
    return powerups