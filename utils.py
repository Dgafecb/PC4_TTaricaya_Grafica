import json
import random
from player import Player
from turtles import Turtle
from zorro import Fox
from enemy import Enemy
#from gif import GifBackground
from dialogue import DialogueBox
import sys
import pygame
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
        "speed": {"image": "./assets/images/power_upps/crystal_01.png", "desc": "Boosts speed"},
        "invisible_turtle_follower": {"image": "./assets/images/power_upps/potion_01.png", "desc": "Invisible follower"},
        "turtle_speed": {"image": "./assets/images/power_upps/herb_02.png", "desc": "Increases turtle speed"}
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

def generate_random_turtle(n,turtles):
   
    for _ in range(n):
        x = random.randint(-50, -10)
        y = random.randint(100, HEIGHT - 100)
        turtle = Turtle(x, y, "./assets/images/turtle_assets")
        turtles.add(turtle)


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


# Función para generar zorros aleatorios
def generate_random_fox(n,eggs):
    foxes = pygame.sprite.Group()
    for _ in range(n):
        # A la derecha
        x = WIDTH + 100

        y = random.randint(100, HEIGHT - 100)
        fox = Fox("./assets/images/fox_assets", eggs)
        foxes.add(fox)
    return foxes

def generate_random_enemy(n,eggs):
    enemies = pygame.sprite.Group()
    for _ in range(n):
        x = WIDTH + 100
        y = random.randint(100, HEIGHT - 100)
        enemy = Enemy("./assets/images/hunter_assets",eggs)
        enemies.add(enemy)
    return enemies

# Codigo de menu


lg_bg = '#e4fccc'
dg_bg = '#071821'

#gif_bg = GifBackground("./video.gif", (WIDTH, HEIGHT))

def set_color(texto, color, font_size=30):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(texto, True, color)
    return text_surface


def start_game(surface, dict_estado_actual):
    pygame.mixer.music.stop()
    
    dict_estado_actual["estado_actual"] = 0
    #print("El estado ha cambiado",dict_estado_actual)
    

def handle_events(event, back_button_rect):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if back_button_rect.collidepoint(event.pos):
            return True
    return False

def instructions_menu_loop(surface, dialogue_boxes, back_button_rect, back_button_color):
    clock = pygame.time.Clock()
    running = True

    path_image = "./assets/images/fondo.png"
    image = pygame.image.load(path_image).convert_alpha()
    while running:
        surface.blit(image, (0, 0))
        # Dibujar cuadros de diálogo
        for box in dialogue_boxes:
            box.draw_image(surface, color_letra=(200, 200, 200))
            box.update()

        # Dibuja el botón "Volver"
        pygame.draw.rect(surface, back_button_color, back_button_rect)
        font = pygame.font.SysFont('arial', 24)
        text = font.render("Volver", True, (0, 0, 0))
        surface.blit(text, (back_button_rect.x + 10, back_button_rect.y + 5))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif handle_events(event, back_button_rect):  # Usar la función de eventos separada
                #print("Botón 'Volver' presionado")
                running = False  # Salir del menú de instrucciones

        pygame.display.flip()
        clock.tick(60)

# Función para crear el menú de instrucciones
def create_instructions_menu(surface):
    # Crear cuadros de diálogo para las instrucciones
    dialogue_boxes = []

    box_width, box_height = 700, 100
    text_speed = 2
    letter_size = (16, 16)
    letters_path_day = "../assets/images/ui/ascii"  # Cambia a la ruta de tus letras
    letters_path_night = "../assets/images/ui/ascii_noche"  # Cambia a la ruta de tus letras

    # Crear los cuadros de diálogo
    dialogue_boxes.append(DialogueBox(letters_path_day, (50, 30), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text('Usa las flechas del teclado para moverte por el mapa.')
    dialogue_boxes[-1].set_color_fondo((224,248,207))

    dialogue_boxes.append(DialogueBox(letters_path_day, (50, 130), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text('a. De dia: Usa A para guiar a las tortugas y S para darles un empujon.')
    dialogue_boxes[-1].set_color_fondo((224,248,207))

    dialogue_boxes.append(DialogueBox(letters_path_day, (50, 230), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text('Recoge los potenciadores y descubre su efecto.')
    dialogue_boxes[-1].set_color_fondo((224,248,207))

    dialogue_boxes.append(DialogueBox(letters_path_night, (50, 330), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text('b. De noche: Presiona los botones para ahuyentar depredadores.')
    dialogue_boxes[-1].set_color_fondo((7,24,33))
    
    dialogue_boxes.append(DialogueBox(letters_path_night, (50, 430), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text('Presiona A para espantar cazadores, presiona B para espantar a los lobos.')
    dialogue_boxes[-1].set_color_fondo((7,24,33))

    
    # Botón para volver al menú principal
    back_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 40)
    back_button_color = (100, 200, 100)

    # Llamamos al loop de instrucciones
    instructions_menu_loop(surface, dialogue_boxes, back_button_rect, back_button_color)

def go_back_to_main_menu(menu):
    global current_menu
    current_menu = menu

def switch_menu(new_menu):
    global current_menu
    current_menu = new_menu


import sys

# Configuración global
WIDTH, HEIGHT = 800, 600
lg_bg = '#e4fccc'  # Color claro para los botones
dg_bg = '#071821'  # Color oscuro para los botones
button_hover = '#5a6e70'  # Color al pasar el ratón sobre el botón

# Instrucciones del juego
instrucciones_texto = [
    "Nivel 1 : ",
    "Elige los nidos de las tortugas a tu cargo. (CLICK)",
    "  (A) : Agarrar un huevo.",
    "  (S) : Soltar el huevo.",
    "Nivel 2 : ",
    "Ayuda a las tortugas a cruzar el río",
    "  (A) : Atraes la tortuga que chocas.",
    "  (A + S) : Empujas la tortuga que esta cerca",
    "Puedes recoger habilidades que te ayudarán en el juego",
]

instruction = False
dic_i = {'intruction':False}
# Función para dibujar el menú
def dibujar_menu(surface, TEMP, clock,events):
    # Cargar la imagen de fondo
    global instruction

    fondo_menu_path = './assets/images/fondo.png'
    image = pygame.image.load(fondo_menu_path)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))  # Ajustar tamaño de la imagen al tamaño de la pantalla
    surface.blit(image, (0, 0))  # Dibujar fondo en la superficie

    # Dimensiones de los botones
    button_width, button_height = 300, 50
    start_game_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height))
    instructions_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height))
    exit_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, button_height))

    # Dibujar botones
    pygame.draw.rect(surface, dg_bg, start_game_rect)
    pygame.draw.rect(surface, dg_bg, instructions_rect)
    pygame.draw.rect(surface, dg_bg, exit_rect)

    font = pygame.font.SysFont('arial', 30)
    start_text = font.render('Empezar Juego', True, lg_bg)
    instructions_text = font.render('Ver Instrucciones', True, lg_bg)
    exit_text = font.render('Salir', True, lg_bg)

    surface.blit(start_text, (start_game_rect.x + (button_width - start_text.get_width()) // 2, start_game_rect.y + (button_height - start_text.get_height()) // 2))
    surface.blit(instructions_text, (instructions_rect.x + (button_width - instructions_text.get_width()) // 2, instructions_rect.y + (button_height - instructions_text.get_height()) // 2))
    surface.blit(exit_text, (exit_rect.x + (button_width - exit_text.get_width()) // 2, exit_rect.y + (button_height - exit_text.get_height()) // 2))

    

    # Manejar los eventos de clic
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Clic en el botón "Empezar Juego"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_game_rect.collidepoint(event.pos):
                TEMP["estado_actual"] = 0  # Cambiar el estado a "juego"
                
        # Clic en el botón "Ver Instrucciones"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if instructions_rect.collidepoint(event.pos):
                instruction = True
                dic_i["intruction"] = True

        # Clic en el botón "Salir"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
    
    if instruction:
        mostrar_instrucciones(surface, clock,dic_i,events)
        instruction = dic_i["intruction"]

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

# Función para mostrar el cuadro de instrucciones
def mostrar_instrucciones(surface, clock, dict_inst,events):
    # Rectángulo para el cuadro de instrucciones
    instructions_box_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
    pygame.draw.rect(surface, (0, 0, 0, 150), instructions_box_rect)  # Fondo semitransparente

    # Dibujar el texto de instrucciones
    font = pygame.font.SysFont('arial', 24)
    y_offset = 120
    for line in instrucciones_texto:
        line_text = font.render(line, True, lg_bg)
        surface.blit(line_text, (instructions_box_rect.x + 20, y_offset))
        y_offset += 40

    # Botón de cierre (X)
    close_button_rect = pygame.Rect(instructions_box_rect.x + instructions_box_rect.width - 50, instructions_box_rect.y - 30, 30, 30)
    pygame.draw.rect(surface, (255, 0, 0), close_button_rect)  # Botón de cierre rojo
    close_text = font.render('X', True, (255, 255, 255))
    surface.blit(close_text, (close_button_rect.x + 8, close_button_rect.y + 5))  # Posicionar la "X"

    # Manejar eventos del botón de cierre
    for event in events :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if close_button_rect.collidepoint(event.pos):
                #print("Cerrar")
                #print(dict_inst)
                dict_inst["intruction"] = False
                return  # Cerrar el cuadro de instrucciones

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)