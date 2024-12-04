import pygame
import pytmx
import random 
from pytmx import load_pygame

import time
import math
import json

import os
import sys
from gif import GifBackground

import pygame_menu
import imageio

import asyncio




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

def generate_random_turtle(n,turtles):
   
    for _ in range(n):
        x = random.randint(-50, -10)
        y = random.randint(100, HEIGHT - 100)
        turtle = Turtle(x, y, "../assets/images/turtle_assets")
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
        fox = Fox("../assets/images/fox_assets", eggs)
        foxes.add(fox)
    return foxes

def generate_random_enemy(n,eggs):
    enemies = pygame.sprite.Group()
    for _ in range(n):
        x = WIDTH + 100
        y = random.randint(100, HEIGHT - 100)
        enemy = Enemy("../assets/images/hunter_assets",eggs)
        enemies.add(enemy)
    return enemies


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

    while running:
        surface.blit(gif_bg.get_frame(), (0, 0))
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


# Sustituye map_data y ajusta draw_map
def draw_map_from_tmx(screen, tmx_data):
    for layer in tmx_data.visible_layers:  # Iterar por las capas visibles del mapa
        if hasattr(layer, "tiles"):  # Si la capa contiene tiles
            for x, y, tile_surface in layer.tiles():  # tile_surface es la imagen del tile
                if tile_surface is not None:  # Solo dibujar tiles válidos
                    screen.blit(tile_surface, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

################### CLASES ####################

class Turtle(pygame.sprite.Sprite):
    score = 0
    def __init__(self, x, y, asset_path):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 1
        self.direccion = "walk"
        self.asset_path = asset_path

        self.attack_counter = 0
        self.is_attacked = False

        self.animaciones = {
            "idle": self.cargar_sprites("Idle.png", 4),
            "walk": self.cargar_sprites("Walk.png", 6),
            "attack": self.cargar_sprites("Attack.png", 6),
            "hurt": self.cargar_sprites("Hurt.png", 8),  # Animación de herido (2 frames)
            "death": self.cargar_sprites("Death.png", 6)
        }
        self.current_sprite = 0
        self.current_animation = self.animaciones["walk"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.is_following_player = False
        self.is_attacking = False
        self.animation_steps = 0
        self.health = 3
        self.is_dead = False
        self.last_appearance_time = time.time()

        self.is_visible=True

    def cargar_sprites(self, file_name, frames):
        """Carga los sprites desde una hoja de sprites."""
        sprites = []
        sprite_sheet = pygame.image.load(f"{self.asset_path}/{file_name}").convert_alpha()
        sprite_width = sprite_sheet.get_width() // frames
        sprite_height = sprite_sheet.get_height()

        for i in range(frames):
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)
            sprites.append(sprite)
            sprites.append(sprite)
            sprites.append(sprite)

        return sprites

    def update(self):
        """Actualiza la animación según la dirección."""
        # Control de animación para 'death' (si está muerta)
        if self.is_dead:
            self.current_animation = self.animaciones["death"]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)
            self.image = self.current_animation[self.animation_steps]
            self.rect = self.image.get_rect(center=(self.x, self.y))
       # Control de animación para 'attack'
        elif self.is_attacking:
            self.current_animation = self.animaciones["attack"]
            self.x += self.velocidad * 4  # Aumentar la velocidad de ataque
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)

            if self.animation_steps == 0:  # Cuando la animación de ataque termina
                self.is_attacking = False
                self.current_animation = self.animaciones["walk"]

        # Control de animación para 'hurt'
        elif self.is_attacked:
            self.current_animation = self.animaciones["hurt"]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)
            
            if self.animation_steps == 0:  # Cuando la animación de 'hurt' termina
                self.is_attacked = False  # Resetear el estado de ataque
                if self.health > 0:  # Solo vuelve a caminar si no está muerta
                    self.current_animation = self.animaciones["walk"]

        # Control de animación cuando sigue al jugador o está en modo "walk"
        elif self.is_following_player:
            self.current_animation = self.animaciones["walk"]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)

        else:
            self.current_animation = self.animaciones[self.direccion]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)

        # Actualizamos la imagen de la tortuga
        self.image = self.current_animation[self.animation_steps]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update_sprite(self, animation_steps, current_animation):
        """Actualizar el índice del sprite de la animación, reiniciando si es necesario."""
        animation_steps += 1
        if animation_steps >= len(current_animation):
            animation_steps = 0
            if self.is_dead:
                self.kill()
        return animation_steps

    def move(self, player):
        """Mueve la tortuga."""
        self.evaluate_limits()

        if self.is_following_player:
            if player.x > self.x:
                self.x += self.velocidad
                self.direccion = "walk"
            elif player.x < self.x:
                self.x -= self.velocidad
                self.direccion = "walk"

            if player.y > self.y:
                self.y += self.velocidad
            elif player.y < self.y:
                self.y -= self.velocidad

        elif not self.is_attacking and not self.is_dead:
            if self.direccion == "walk":
                self.x += self.velocidad
                if self.x > WIDTH:
                    self.x = random.randint(-50, -10)
                    self.y = random.randint(100, HEIGHT - 100)

            if self.x > WIDTH - 300:
                # Aumentar el puntaje si la tortuga llega al final
                Turtle.score += 1
                self.kill()
            
            
            

    def draw(self, screen):
        """Dibuja la tortuga en la pantalla."""
        screen.blit(self.image, (self.x, self.y))

    def attack(self):
        """Inicia el ataque de la tortuga.""" 
        self.animation_steps = 0       
        self.is_attacking = True

    def stop_following(self):
        """Deja de seguir al jugador y vuelve a caminar.""" 
        self.animation_steps = 0 
        self.is_following_player = False
        self.direccion = "walk"

    def start_following(self):
        """Comienza a seguir al jugador.""" 
        self.animation_steps = 0
        self.is_following_player = True

    def hurt(self):
        """Cuando la tortuga recibe daño."""   
        self.attack_counter += 1  
        self.is_attacked = True  
        if self.attack_counter >= 3:
            self.is_dead = True
            # Si la tortuga muere, restamos 1 al puntaje
            Turtle.score -= 1
        else:
            
            self.attack_steps = 0  
            self.health -= 1  # Reducir la vida de la tortuga
        
    def evaluate_limits(self):
        """Evalúa si la tortuga está dentro de los límites de la pantalla."""
        if self.y < 450 :
            if self.x > 580:
                # Eliminamos la tortuga si se sale de los límites
                Turtle.score += 1
                self.kill()
        else:
            if self.x > WIDTH - 350:
                Turtle.score += 1
                self.kill()

class Fox(pygame.sprite.Sprite):
    def __init__(self, asset_path, eggs_group):
        super().__init__()
        self.respawn()
        self.velocidad = 2
        self.direccion = "walk_left"  # Camina hacia la izquierda por defecto
        self.asset_path = asset_path
        self.eggs_group = eggs_group

        # Cargar las animaciones
        self.animaciones = {
            "idle_left": self.cargar_sprites("GandalfHardcore doggy sheet 2.png", 0),
            "idle_right": self.cargar_sprites_inv("GandalfHardcore doggy sheet 2.png", 0),
            "walk_right": self.cargar_sprites("GandalfHardcore doggy sheet 2.png", 1),
            "walk_left": self.cargar_sprites_inv("GandalfHardcore doggy sheet 2.png", 1),
            "attack": self.cargar_sprites("GandalfHardcore doggy sheet 2.png", 1),
        }

        self.current_sprite = 0
        self.current_animation = self.animaciones["walk_left"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Estado del zorro
        self.is_attacking = False
        self.attack_steps = 0
        self.target_egg = None
        self.attack_cooldown = 0
        self.attack_count = 0
        self.escapando = False

    def cargar_sprites(self, image_path, fila):
        sprites = []
        sprite_sheet = pygame.image.load(os.path.join(self.asset_path, image_path)).convert_alpha()
        sprite_width = sprite_sheet.get_width() // 6
        sprite_height = sprite_sheet.get_height() // 2

        for i in range(6):
            rect = pygame.Rect(i * sprite_width, fila * sprite_height, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)

        return sprites

    def cargar_sprites_inv(self, image_path, fila):
        sprites = []
        sprite_sheet = pygame.image.load(os.path.join(self.asset_path, image_path)).convert_alpha()
        sprite_width = sprite_sheet.get_width() // 6
        sprite_height = sprite_sheet.get_height() // 2

        for i in range(6):
            rect = pygame.Rect(i * sprite_width, fila * sprite_height, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprite_invertido = pygame.transform.flip(sprite, True, False)
            sprites.append(sprite_invertido)

        return sprites

    def update(self):
        """Actualiza la animación y la lógica del zorro."""
        self.find_closest_egg()
        if self.escapando:
            self.target_egg = None
            self.is_attacking = False
            self.current_animation = self.animaciones["walk_right"]
            self.direccion = "walk_right"
            self.attack_cooldown = 120
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Control de animación y ataque
        if self.is_attacking and self.attack_cooldown == 0:
            self.current_animation = self.animaciones["attack"]
            self.attack_steps += 1
            if self.attack_steps >= len(self.current_animation):
                if self.target_egg:
                    self.target_egg.break_egg()

                self.attack_steps = 0
                self.attack_count += 1
                self.attack_cooldown = 90

                if self.attack_count >= 3:
                    self.attack_count = 0
                    self.attack_cooldown = 120
                    self.is_attacking = False
                    self.current_animation = self.animaciones["walk_left"]
                    self.direccion = "walk_left"
        else:
            if not self.is_attacking:
                # Cambio de animación dependiendo de la dirección
                if self.direccion == "walk_left":
                    self.current_animation = self.animaciones["walk_left"]
                else:
                    self.current_animation = self.animaciones["walk_right"]

        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            self.current_sprite = 0

        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        """Mueve el zorro hacia el huevo más cercano o camina por su cuenta."""
        if self.target_egg:
            if self.target_egg.x > self.x:
                self.x += self.velocidad
                self.direccion = "walk_right"
            elif self.target_egg.x < self.x:
                self.x -= self.velocidad
                self.direccion = "walk_left"    

            if self.target_egg.y > self.y:
                self.y += self.velocidad
            elif self.target_egg.y < self.y:
                self.y -= self.velocidad
        else:
            if self.direccion == "walk_left":
                self.x -= self.velocidad
                if self.x < 0:  # Cuando el zorro llegue al borde izquierdo, reinicia
                    self.respawn()
                    self.escapando = False
            else:
                self.x += self.velocidad
                if self.x > WIDTH -100 :  # Cuando el zorro llegue al borde derecho, reinicia
                    self.respawn()
                    self.escapando = False
        
        # Si esta escapando, se mueve al punto de escape 700,200
        if self.escapando:
            if self.x < 700:
                self.x += self.velocidad
            if self.y < 200:
                self.y += self.velocidad
            if self.x > 700:
                self.x -= self.velocidad
            if self.y > 200:
                self.y -= self.velocidad


    def attack(self):
        """Inicia el ataque del zorro si no está en cooldown."""        
        if self.attack_cooldown == 0:  
            self.is_attacking = True

    def stop_attack(self):
        """Detiene el ataque."""        
        self.is_attacking = False

    def find_closest_egg(self):
        """Encuentra el huevo más cercano para atacar."""
        closest_egg = None
        min_distance = float('inf')

        for egg in self.eggs_group:
            distance = pygame.math.Vector2(self.x - egg.x, self.y - egg.y).length()
            if distance < min_distance and distance < 100 and egg.is_visible:
                min_distance = distance
                closest_egg = egg

        self.target_egg = closest_egg

    def draw(self, screen):
        """Dibuja el zorro en la pantalla."""
        screen.blit(self.image, (self.x, self.y))
    def huir(self):
        self.escapando = True

    def respawn(self):
        self.x = random.choice(range(690, 711, 20))  # Posición x dentro del rango del arbusto
        self.y = random.choice(range(60, 390, 30))
        self.direccion = "walk_left"



class DialogueBox:
    def __init__(self, letters_path, position, text_speed=2, box_width=700, box_height=120, letter_size=(16, 16),color_fondo = '#071821'):
        """
        Inicializa el cuadro de diálogo.
        :param letters_path: Carpeta donde están las imágenes de letras.
        :param position: Posición del cuadro de diálogo (x, y).
        :param text_speed: Velocidad de animación del texto.
        :param box_width: Ancho del cuadro de diálogo.
        :param box_height: Alto del cuadro de diálogo.
        :param letter_size: Tamaño de cada letra (ancho, alto).
        """
        self.letters_path = letters_path
        self.position = position
        self.text_speed = text_speed
        self.box_width = box_width
        self.box_height = box_height
        self.letter_width, self.letter_height = letter_size
        self.text = ""
        self.visible_text = ""
        self.current_index = 0
        self.is_visible = False
        self.font = pygame.font.SysFont("arial", 18)  # Fuente para el texto simple de las instrucciones
        self.color_fondo = color_fondo
        # Diccionario para caracteres especiales (botones específicos)
        self.special_characters = {
            'A': "../assets/images/botones_assets/boton_A.png",
            'B': "../assets/images/botones_assets/boton_B.png"
        }
    def change_position(self,new_position):
        self.position =  new_position
    def set_text(self, text):
        """
        Establece el texto para mostrar y reinicia el progreso.
        """
        self.text = text
        self.visible_text = " " * len(text)  # Llena el cuadro con espacios al inicio
        self.current_index = 0
        self.is_visible = True
    def set_color_fondo(self,color_fondo):
        self.color_fondo = color_fondo

    def hide(self):
        """Oculta el cuadro de diálogo."""
        self.is_visible = False

    def update(self):
        """
        Actualiza el texto animado, mostrando caracteres gradualmente.
        """
        if self.is_visible and self.current_index < len(self.text):
            self.current_index += self.text_speed
            # Reemplaza gradualmente los espacios con las letras reales
            self.visible_text = self.text[:int(self.current_index)] + " " * (len(self.text) - int(self.current_index))

    def draw(self, screen, color_fondo = '#071821', color_letra='#e4fccc'):
        """
        Dibuja el cuadro de diálogo y el texto.
        """
        if self.is_visible:
            # Dibuja el rectángulo del cuadro de diálogo
            pygame.draw.rect(
                screen, 
                color_fondo,  # Color del cuadro # 346c54 (letra dia) - # #e4fccc (fondo dia)
                (self.position[0], self.position[1], self.box_width, self.box_height)
            )
            pygame.draw.rect(
                screen, 
                (200, 200, 200),  # Color del borde (gris claro)
                (self.position[0], self.position[1], self.box_width, self.box_height), 
                3  # Grosor del borde
            )

            # Calcular espacio disponible para el texto (considerando las instrucciones)
            instructions_height = 30  # Altura para las instrucciones
            available_height = self.box_height - instructions_height  # Espacio para el texto
            max_line_width = self.box_width - 40  # Ancho máximo para una línea de texto

            # Variables para el dibujo de texto
            x, y = self.position[0] + 20, self.position[1] + 20  # Posición inicial
            line_width = 0  # Ancho de la línea actual

            words = self.visible_text.split(" ")  # Dividir el texto en palabras
            for word in words:
                word_width = 0
                # Calcular el ancho de la palabra
                for char in word:
                    try:
                        # Cargar la imagen correspondiente al carácter
                        char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                        char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))
                        word_width += char_image.get_width()  # Sumar el ancho de cada carácter
                    except FileNotFoundError:
                        print(f"Advertencia: Imagen no encontrada para '{char}'")

                # Verificar si la palabra cabe en la línea
                if line_width + word_width <= max_line_width:
                    # Si cabe, agregar la palabra a la línea actual
                    for char in word:
                        try:
                            # Cargar la imagen correspondiente al carácter
                            char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                            char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))

                            # Dibuja el carácter en la pantalla
                            screen.blit(char_image, (x, y))

                            # Actualiza la posición en X y el ancho de la línea
                            x += self.letter_width
                            line_width += self.letter_width
                        except FileNotFoundError:
                            print(f"Advertencia: Imagen no encontrada para '{char}'")

                    # Agregar un espacio entre las palabras
                    x += self.letter_width  # Ajuste de espacio entre palabras
                    line_width += self.letter_width  # Ajuste del ancho de la línea
                else:
                    # Si no cabe, pasa a la siguiente línea
                    x = self.position[0] + 20  # Reiniciar la posición X
                    y += self.letter_height + 5  # Saltar a la siguiente línea
                    line_width = 0  # Reiniciar el ancho de la línea

                    # Asegurarnos de que la palabra cabe en la nueva línea
                    if y + self.letter_height + instructions_height > self.position[1] + self.box_height:
                        break  # Si no cabe más texto, no dibujar nada más

                    # Dibuja la palabra en la nueva línea
                    for char in word:
                        try:
                            # Cargar la imagen correspondiente al carácter
                            char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                            char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))

                            # Dibuja el carácter en la pantalla
                            screen.blit(char_image, (x, y))

                            # Actualiza la posición en X y el ancho de la línea
                            x += self.letter_width
                            line_width += self.letter_width
                        except FileNotFoundError:
                            print(f"Advertencia: Imagen no encontrada para '{char}'")

                    # Después de escribir la palabra, agregamos un espacio
                    x += self.letter_width  # Para dejar un espacio después de la palabra
                    line_width += self.letter_width  # Ajustar el ancho de la línea después del espacio

            # Dibuja las instrucciones debajo del texto
            instructions = "Presiona: (ESPACIO) para terminar   (Q) para continuar"
            instructions_surface = self.font.render(instructions, True, color_letra)  # Texto blanco
            screen.blit(instructions_surface, (self.position[0] + 20, self.position[1] + self.box_height - instructions_height))

    def draw_menu(self, screen, color_fondo = '#e4fccc', color_letra='#346c54'):
        """
        Dibuja el cuadro de diálogo y el texto.
        """
        if self.is_visible:
            # Dibuja el rectángulo del cuadro de diálogo
            pygame.draw.rect(
                screen, 
                color_fondo,  # Color del cuadro # 346c54 (letra dia) - # #e4fccc (fondo dia)
                (self.position[0], self.position[1], self.box_width, self.box_height)
            )
            pygame.draw.rect(
                screen, 
                (200,200,200),  # Color del borde (gris claro)
                (self.position[0], self.position[1], self.box_width, self.box_height), 
                3  # Grosor del borde
            )

            # Calcular espacio disponible para el texto (considerando las instrucciones)
            instructions_height = 30  # Altura para las instrucciones
            available_height = self.box_height - instructions_height  # Espacio para el texto
            max_line_width = self.box_width - 40  # Ancho máximo para una línea de texto

            # Variables para el dibujo de texto
            x, y = self.position[0] + 20, self.position[1] + 20  # Posición inicial
            line_width = 0  # Ancho de la línea actual

            words = self.visible_text.split(" ")  # Dividir el texto en palabras
            for word in words:
                word_width = 0
                # Calcular el ancho de la palabra
                for char in word:
                    try:
                        # Cargar la imagen correspondiente al carácter
                        char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                        char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))
                        word_width += char_image.get_width()  # Sumar el ancho de cada carácter
                    except FileNotFoundError:
                        print(f"Advertencia: Imagen no encontrada para '{char}'")

                # Verificar si la palabra cabe en la línea
                if line_width + word_width <= max_line_width:
                    # Si cabe, agregar la palabra a la línea actual
                    for char in word:
                        try:
                            # Cargar la imagen correspondiente al carácter
                            char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                            char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))

                            # Dibuja el carácter en la pantalla
                            screen.blit(char_image, (x, y))

                            # Actualiza la posición en X y el ancho de la línea
                            x += self.letter_width
                            line_width += self.letter_width
                        except FileNotFoundError:
                            print(f"Advertencia: Imagen no encontrada para '{char}'")

                    # Agregar un espacio entre las palabras
                    x += self.letter_width  # Ajuste de espacio entre palabras
                    line_width += self.letter_width  # Ajuste del ancho de la línea
                else:
                    # Si no cabe, pasa a la siguiente línea
                    x = self.position[0] + 20  # Reiniciar la posición X
                    y += self.letter_height + 5  # Saltar a la siguiente línea
                    line_width = 0  # Reiniciar el ancho de la línea

                    # Asegurarnos de que la palabra cabe en la nueva línea
                    if y + self.letter_height + instructions_height > self.position[1] + self.box_height:
                        break  # Si no cabe más texto, no dibujar nada más

                    # Dibuja la palabra en la nueva línea
                    for char in word:
                        try:
                            # Cargar la imagen correspondiente al carácter
                            char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                            char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))

                            # Dibuja el carácter en la pantalla
                            screen.blit(char_image, (x, y))

                            # Actualiza la posición en X y el ancho de la línea
                            x += self.letter_width
                            line_width += self.letter_width
                        except FileNotFoundError:
                            print(f"Advertencia: Imagen no encontrada para '{char}'")

                    # Después de escribir la palabra, agregamos un espacio
                    x += self.letter_width  # Para dejar un espacio después de la palabra
                    line_width += self.letter_width  # Ajustar el ancho de la línea después del espacio

    def draw_image(self, screen, color_letra='#e4fccc'):
        if self.is_visible:
            # Dibujar el fondo del cuadro
            
            pygame.draw.rect(
                screen,
                self.color_fondo,
                (self.position[0], self.position[1], self.box_width, self.box_height)
            )
            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (self.position[0], self.position[1], self.box_width, self.box_height),
                3
            )

            # Coordenadas iniciales
            x, y = self.position[0] + 20, self.position[1] + 20
            max_x = self.position[0] + self.box_width - 20  # Límite derecho del cuadro

            for char in self.visible_text:
                if x + self.letter_width > max_x:  # Comprobar si excede el límite
                    x = self.position[0] + 20  # Reiniciar la posición x al inicio
                    y += self.letter_height  # Mover hacia abajo

                    # Si excede la altura del cuadro, detener (o manejar de otra forma)
                    if y + self.letter_height > self.position[1] + self.box_height:
                        print("Advertencia: Texto excede la altura del cuadro.")
                        break

                if char in self.special_characters:
                    # Dibujar la imagen especial para 'A' o 'B'
                    try:
                        char_image = pygame.image.load(self.special_characters[char])
                        char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))
                        screen.blit(char_image, (x, y))
                        x += self.letter_width
                    except FileNotFoundError:
                        print(f"Advertencia: Imagen no encontrada para '{char}'")
                else:
                    # Dibujar el texto normal
                    try:
                        char_image_path = f"{self.letters_path}/{ord(char)}.png"
                        char_image = pygame.image.load(char_image_path)
                        char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))
                        screen.blit(char_image, (x, y))
                        x += self.letter_width
                    except FileNotFoundError:
                        print(f"Advertencia: Imagen no encontrada para '{char}'")



import pygame
import random
import time

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image_normal, image_pressed, sound_file, scale_factor=1.5): # scale_factor permite escalar el size del sprite del boton
        super().__init__()
        self.x = x
        self.y = y
        self.scale_factor = scale_factor

        # Carga y escala las imágenes
        self.image_normal = pygame.image.load(image_normal).convert_alpha()
        self.image_pressed = pygame.image.load(image_pressed).convert_alpha()
        self.image_normal = pygame.transform.scale(
            self.image_normal,
            (
                int(self.image_normal.get_width() * self.scale_factor),
                int(self.image_normal.get_height() * self.scale_factor),
            )
        )
        self.image_pressed = pygame.transform.scale(
            self.image_pressed,
            (
                int(self.image_pressed.get_width() * self.scale_factor),
                int(self.image_pressed.get_height() * self.scale_factor),
            )
        )

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False
        self.pressed_time = None  # Momento en que el botón fue presionado

        # Carga el sonido
        self.sound = pygame.mixer.Sound(sound_file)

    def check_collision(self, player):
        """Verifica la colisión con el player y presiona el botón si colisiona."""
        if self.rect.colliderect(player.rect):
            if not self.is_pressed:
                self.sound.play()
                self.image = self.image_pressed
                self.is_pressed = True
                self.pressed_time = time.time()  # Marca el momento en que fue presionado
        else:
            if not self.is_pressed:  # Solo cambia a normal si no está en estado presionado
                self.image = self.image_normal

    def update(self):
        """Actualiza el estado del botón."""
        if self.is_pressed and self.pressed_time:
            elapsed_time = time.time() - self.pressed_time
            if elapsed_time >= 4:  # AQUI SE MODIFICA EL TIEMPO QUE ESPERA ANTES DE CAMBIAR DE LUGAR
                self.change_position()
                self.image = self.image_normal
                self.is_pressed = False
                self.pressed_time = None

    def change_position(self):
        """Cambia la posición del botón a un lugar aleatorio en la pantalla."""
        width, height = 520, 600
        new_x = random.randint(0, width - self.rect.width)
        new_y = random.randint(80, height - self.rect.height)
        self.rect.topleft = (new_x, new_y)
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        """Dibuja el botón en la pantalla."""
        screen.blit(self.image, (self.x, self.y))


import pygame
import random
import os
from settings import WIDTH, HEIGHT

class Crab(pygame.sprite.Sprite):
    def __init__(self, asset_path, turtles_group):
        super().__init__()
        self.x = random.choice([WIDTH/2, WIDTH-100])
        self.y = random.randint(100, HEIGHT - 100)
        self.velocidad = 1
        self.direccion = "walk"
        self.asset_path = asset_path
        self.turtles_group = turtles_group

        # Cargar las animaciones
        self.animaciones = {
            "idle": self.cargar_sprites("Idle", 5),
            "walk": self.cargar_sprites("Moving", 4),
            "attack": self.cargar_sprites("Attack", 4),
        }
        self.current_sprite = 0
        self.current_animation = self.animaciones["walk"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Estado del cangrejo
        self.is_attacking = False
        self.attack_steps = 0
        self.target_turtle = None
        self.attack_cooldown = 0  # Cooldown de ataque
        self.attack_count = 0  # Contador de ataques realizados

    def cargar_sprites(self, folder, frames):
        """Carga los sprites desde una carpeta para una animación dada."""
        sprites = []
        for i in range(1, frames + 1):
            base_path = os.path.join(self.asset_path, folder)
            if folder == "Attack":
                sprite_path = os.path.join(base_path, f"Crab_Attack{i}.png")
            elif folder == "Idle":
                sprite_path = os.path.join(base_path, f"Crab{i}.png")
            else:
                sprite_path = os.path.join(base_path, f"CrabMoving{i}.png")
            
            try:
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprites.append(sprite)
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo {sprite_path}")
        
        return sprites

    def update(self):
        """Actualiza la animación y la lógica del cangrejo."""
        self.find_closest_turtle()
        #print(self.target_turtle)

        
        # Control de cooldown de ataque
        if self.attack_cooldown > 0 :
            self.attack_cooldown -= 1  # Reducir el cooldown
         

        if self.is_attacking and self.attack_cooldown == 0:
            #print("Attacking")
            self.current_animation = self.animaciones["attack"]
            self.attack_steps += 1
            if self.attack_steps >= len(self.current_animation):
                #print("Attack done")
                # Llama al método hurt de la tortuga atacada
                if self.target_turtle:
                    self.target_turtle.hurt()

                self.attack_steps = 0
                self.attack_count += 1
                self.attack_cooldown = 90  # Establece el tiempo de cooldown
                
                if self.attack_count >= 3:  # Limitar a 3 ataques antes de establecer cooldown
                    self.attack_count = 0
                    self.attack_cooldown = 120  # Establecer cooldown más largo después de 3 ataques
                    self.is_attacking = False
                    self.current_animation = self.animaciones["walk"]
        else:
            if not self.is_attacking:
                self.current_animation = self.animaciones["walk"]

        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            self.current_sprite = 0

        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Mover hacia la tortuga más cercana si existe un objetivo
        if self.target_turtle:
            if self.target_turtle.x > self.x:
                self.x += self.velocidad
            elif self.target_turtle.x < self.x:
                self.x -= self.velocidad

            if self.target_turtle.y > self.y:
                self.y += self.velocidad
            elif self.target_turtle.y < self.y:
                self.y -= self.velocidad

    def move(self):
        """Mueve el cangrejo hacia la tortuga más cercana o camina por su cuenta."""
 
        if self.target_turtle:
            #print("atacando")
            if self.target_turtle.x > self.x:
                
                self.x += self.velocidad
            elif self.target_turtle.x < self.x:
                self.x -= self.velocidad

            if self.target_turtle.y > self.y:
                self.y += self.velocidad
            elif self.target_turtle.y < self.y:
                self.y -= self.velocidad

        else:
            if self.direccion == "walk":
                self.y += self.velocidad
                if self.y > HEIGHT or self.y < 0:
                    self.y = random.choice([0, HEIGHT])
                    self.x = random.randint(0, WIDTH)

    def attack(self):
        """Inicia el ataque del cangrejo si no está en cooldown."""        
        if self.attack_cooldown == 0:  # Solo atacar si no hay cooldown
            self.is_attacking = True
            

    def stop_attack(self):
        """Detiene el ataque."""        
        self.is_attacking = False

    def find_closest_turtle(self):
        """Encuentra la tortuga más cercana para atacar."""
        closest_turtle = None
        min_distance = float('inf')
       
        for turtle in self.turtles_group:

            distance = pygame.math.Vector2(self.x - turtle.x, self.y - turtle.y).length()
 
            # Verificar si la tortuga es la más cercana y está a menos de 100 píxeles y sea visible
            if distance < min_distance and distance < 100 and turtle.is_visible:

                min_distance = distance
                closest_turtle = turtle

        self.target_turtle = closest_turtle

    def draw(self, screen):
        """Dibuja el cangrejo en la pantalla."""
        screen.blit(self.image, (self.x, self.y))

import pygame
import random
import time
from settings import HEIGHT, WIDTH

class Egg(pygame.sprite.Sprite):
    score = 25
    
    def __init__(self, x, y, asset_path, enemies_group):
        super().__init__()
        self.x = x
        self.y = y
        self.asset_path = asset_path
        self.enemies_group = enemies_group  # Grupo de enemigos
        self.enemy = None  # Inicialmente no hay enemigo asignado
        self.is_broken = False
        self.is_rolling = False
        self.is_visible = True

        # Si ha sido tomado por el player
        self.is_taken_player = False
        self.player = None

    
        # Cargar las animaciones
        self.animaciones = {
            "idle": self.cargar_sprites("egg-idle.png", 6),      # Estado Idle (6 frames)
            "breaking": self.cargar_sprites("egg-breaking.png", 12),  # Estado Breaking (12 frames)
            "rolling": self.cargar_sprites("egg-rolling.png", 4),    # Estado Rolling (4 frames)
        }

        self.current_sprite = 0
        self.current_animation = self.animaciones["idle"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def cargar_sprites(self, file_name, frames):
        """Divide la imagen en múltiples cuadros."""
        sprites = []
        sprite_sheet = pygame.image.load(f"{self.asset_path}/{file_name}").convert_alpha()
        sprite_width = sprite_sheet.get_width() // frames
        sprite_height = sprite_sheet.get_height()
        for i in range(frames):
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)
        return sprites

    def update(self):
        """Actualiza la animación y la lógica del huevo."""

        if self.is_broken:
            self.current_animation = self.animaciones["breaking"]
        elif self.is_rolling:
            self.current_animation = self.animaciones["rolling"]
        elif self.is_taken_player:
            self.follow_player(self.player)
            self.current_animation = self.animaciones["idle"]
        else:
            self.current_animation = self.animaciones["idle"]

        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            if self.is_broken:  # El huevo roto mantiene el último frame
                self.current_sprite = len(self.current_animation) - 1
                Egg.score -= 1
                self.kill()  # Eliminar el huevo roto
            elif self.is_rolling:  # El huevo en rolling hace un loop
                self.current_sprite = 0
            else:  # Idle también hace un loop
                self.current_sprite = 0

        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

       
    def break_egg(self):
        """Rompe el huevo cuando es atacado por el zorro."""
        if not self.is_broken:
            self.is_broken = True
            self.is_rolling = False  # Dejar de rodar si se rompe

    def roll(self):
        """Hace que el huevo ruede (solo si no está roto)."""
        if not self.is_broken:
            self.is_rolling = True

    def stop_rolling(self):
        """Detiene el movimiento de rodar."""
        self.is_rolling = False

    def draw(self, screen):
        """Dibuja el huevo en la pantalla."""
        if self.is_visible:
            screen.blit(self.image, (self.x, self.y))

    def take_egg(self, enemy):
        """El huevo es tomado por el jugador."""
        #print("Huevo tomado")
        self.is_visible = False  # Hacerlo invisible
        self.enemy = enemy

    def drop_egg(self):
        """Cuando el enemigo huye, hace caer los huevos desde su posición."""
        #print("Huevo soltado")
        if self.enemy:
            self.is_visible = True  # Hacer visible el huevo
            # Puedes establecer aquí la posición del enemigo
            self.x = self.enemy.x - random.randint(0, 50)
            self.y = self.enemy.y - random.randint(0, 50)
            #print(f"Posición del huevo: {self.x}, {self.y}")
    
    def follow_player(self,player):
        """Huevo sigue al jugador."""
        if self.is_taken_player and self.player:
            self.x = player.x
            self.y = player.y + 10

    def stop_following_player(self):
        """Deja de seguir al jugador."""
        self.is_taken_player = False

import pygame
import os
import random
from settings import WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_path, eggs_group):
        super().__init__()
        self.respawn()
        self.velocidad = 2
        self.direccion = "running_right"  # Se mueve hacia derecha
        self.asset_path = asset_path
        self.eggs_group = eggs_group
        self.eggs_taken = []

        # Cargar las animaciones
        self.animaciones = {
            "attack": self.cargar_sprites("attack.png", 9),
            "iddle_witharm_right": self.cargar_sprites("iddle_witharm.png", 4),
            "iddle_witharm_left": self.cargar_sprites_inv("iddle_witharm.png", 4),
            "running_right": self.cargar_sprites("running.png", 7),
            "running_left": self.cargar_sprites_inv("running.png", 7),
            "running_witharm_right": self.cargar_sprites("running_witharm.png", 7),
            "running_witharm_left": self.cargar_sprites_inv("running_witharm.png", 7),
        }

        self.current_sprite = 0
        self.current_animation = self.animaciones["running_left"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Estado del enemigo
        self.is_attacking = False
        self.attack_steps = 0
        self.target_egg = None
        self.attack_cooldown = 0
        self.attack_count = 0
        self.escapando = False
        


    def cargar_sprites(self, image_path, num_frames):
        sprites = []
        sprite_sheet = pygame.image.load(os.path.join(self.asset_path, image_path)).convert_alpha()
        sprite_width = sprite_sheet.get_width() // num_frames  # 6 columnas en total
        sprite_height = sprite_sheet.get_height()  # Solo una fila

        for i in range(num_frames):
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)

        return sprites

    def cargar_sprites_inv(self, image_path, num_frames):
        sprites = []
        sprite_sheet = pygame.image.load(os.path.join(self.asset_path, image_path)).convert_alpha()
        sprite_width = sprite_sheet.get_width() // num_frames  # 6 columnas en total
        sprite_height = sprite_sheet.get_height()  # Solo una fila

        for i in range(num_frames):
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprite_invertido = pygame.transform.flip(sprite, True, False)
            sprites.append(sprite_invertido)

        return sprites

    def update(self):
        """Actualiza la animación y la lógica del enemigo."""
        self.find_closest_egg()
        if self.escapando:
            if self.eggs_taken:
                for egg in self.eggs_taken:
                    egg.is_in_enemy_collection = False
                    egg.drop_egg()
                self.eggs_taken = []


            self.target_egg = None
            self.is_attacking = False
            self.current_animation = self.animaciones["running_left"]
            self.direccion = "running_left"
            self.attack_cooldown = 120
            # Ajustar la velocidad para que el enemigo huya más rápido
            self.velocidad = 3
            
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Control de animación y ataque
        if self.is_attacking and self.attack_cooldown == 0 :
            self.current_animation = self.animaciones["attack"]
            self.attack_steps += 1
            if self.attack_steps >= len(self.current_animation):
                if self.target_egg:
                    self.target_egg.take_egg(self)  # Pasar el objeto enemigo a la función take_egg
                    self.eggs_taken.append(self.target_egg)
                    #print(f"El enemigo ha tomado un huevo. Total: {len(self.eggs_taken)}")
                    self.target_egg = None

                self.attack_steps = 0
                self.attack_count += 1
                self.attack_cooldown = 90

                if self.attack_count >= 3:
                    self.attack_count = 0
                    self.attack_cooldown = 120
                    self.is_attacking = False
                    self.current_animation = self.animaciones["running_left"]
                    self.direccion = "running_left"
        else:
            if not self.is_attacking:
                # Cambio de animación dependiendo de la dirección
                if self.direccion == "running_left":
                    self.current_animation = self.animaciones["running_left"]
                elif self.direccion == "running_right":
                    self.current_animation = self.animaciones["running_right"]
                elif self.direccion == "running_witharm_left":
                    self.current_animation = self.animaciones["running_witharm_left"]
                elif self.direccion == "running_witharm_right":
                    self.current_animation = self.animaciones["running_witharm_right"]
                elif self.direccion == "iddle_witharm_left":
                    self.current_animation = self.animaciones["iddle_witharm_left"]
                elif self.direccion == "iddle_witharm_right":
                    self.current_animation = self.animaciones["iddle_witharm_right"]

        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            self.current_sprite = 0

        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        """Mueve el enemigo hacia el huevo más cercano o camina por su cuenta."""
        self.evaluate_limit()
        if self.target_egg:
            if self.target_egg.x > self.x:
                self.x += self.velocidad
                self.direccion = "running_right"
            elif self.target_egg.x < self.x:
                self.x -= self.velocidad
                self.direccion = "running_left"    

            if self.target_egg.y > self.y:
                self.y += self.velocidad
            elif self.target_egg.y < self.y:
                self.y -= self.velocidad
        else:
            if self.direccion == "running_left":
                self.x -= self.velocidad
                if self.x < -self.rect.width:  # Cuando el enemigo salga del borde izquierdo, no reaparece inmediatamente
                    self.direccion = "running_right"
                    self.respawn()

            elif self.direccion == "running_right":
                self.x += self.velocidad
                if self.x > WIDTH-100:  # Cuando el enemigo llegue al borde derecho, reinicia
                    self.respawn()
                    

    def attack(self):
        """Inicia el ataque del enemigo si no está en cooldown."""        
        if self.attack_cooldown == 0:  
            self.is_attacking = True

    def stop_attack(self):
        """Detiene el ataque."""        
        self.is_attacking = False

    def find_closest_egg(self):
        """Encuentra el huevo más cercano para atacar."""
        closest_egg = None
        min_distance = float('inf')

        for egg in self.eggs_group:
            distance = pygame.math.Vector2(self.x - egg.x, self.y - egg.y).length()
            if distance < min_distance and distance < 100 and egg.is_visible:
                min_distance = distance
                closest_egg = egg

        self.target_egg = closest_egg

    def draw(self, screen):
        """Dibuja el enemigo en la pantalla."""
        screen.blit(self.image, (self.x, self.y))

    def huir(self):
        """Enemigo huye cuando se activa el estado de escape."""
        self.escapando = True
    
    def check_collision_egg(self):
        """Verifica si el enemigo colisiona con algun huevo"""
        if not self.escapando:
            for egg in self.eggs_group:
                if self.rect.colliderect(egg.rect) and egg.is_visible:
                    self.attack()
                    self.target_egg = egg
                    break
    
    def respawn(self):
        self.x = random.randint(-250,-50) # Aparece en la zona izquierda (primer cuarto del ancho)
        self.y = random.randint(HEIGHT // 2, HEIGHT)
        self.velocidad = 2
        self.direccion = "running_right"  # Se mueve hacia la derecha
        self.escapando = False
    
    def evaluate_limit(self):
        if self.x > WIDTH - 350:
            # Cambiar la dirección si llega al borde derecho
            self.direccion = "running_left"


def load_and_save_tiles(image_path, tile_width, tile_height, output_folder, scale=None):
    """Divide el tileset en tiles individuales y los guarda en una carpeta."""
    # Inicializar pygame y el display para poder usar convert_alpha()
    pygame.init()
    pygame.display.set_mode((1, 1))  # No es necesario mostrar la ventana, solo inicializarla

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tileset = pygame.image.load(image_path).convert_alpha()
    tileset_width, tileset_height = tileset.get_size()
    tile_count = 0

    for row in range(0, tileset_height, tile_height):
        for col in range(0, tileset_width, tile_width):
            tile = tileset.subsurface((col, row, tile_width, tile_height))
            if scale:
                tile = pygame.transform.scale(tile, (scale[0], scale[1]))

            # Guardar el tile en la carpeta de salida
            tile_filename = os.path.join(output_folder, f"tile_{tile_count}.png")
            pygame.image.save(tile, tile_filename)
            tile_count += 1

    #print(f"Se han guardado {tile_count} tiles en '{output_folder}'.")

# Ejemplo de uso:
load_and_save_tiles("../assets/images/escenes/gentle forest v03.png", 32, 32, "../assets/images/ui/frames/", scale=(64, 64))


class GifBackground:
    def __init__(self, gif_path, screen_size):
        self.reader = imageio.get_reader(gif_path)
        self.screen_size = screen_size
        self.frame_count = len(self.reader)
        self.current_frame = 0

    def get_frame(self):
        frame = self.reader.get_data(self.current_frame)
        self.current_frame = (self.current_frame + 1) % self.frame_count
        surf = pygame.image.fromstring(frame.tobytes(), frame.shape[1::-1], 'RGB')
        return pygame.transform.scale(surf, self.screen_size)



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path, map_file, turtles_group, crap_group):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 5
        self.direccion = "down"
        self.asset_path = asset_path
        self.map = pytmx.load_pygame(map_file)  # Cargar el mapa de Tiled
        # Atributo que indica si el jugador ha recogido un power-up
        self.has_power = False
        # Tiempo de duración del power-up
        self.power_duration = 0
        
        self.turtles_group = turtles_group
        self.crap_group = crap_group

        
        self.can_put_invisible = False
        self.can_speed_turtle_up = False

        # Cargar las animaciones
        self.animaciones = {
            "down": self.cargar_sprites("walk_down.png", 8),
            "up": self.cargar_sprites("walk_up.png", 8),
            "left": self.cargar_sprites("walk_left_up.png", 8),
            "right": self.cargar_sprites("walk_right_up.png", 8),
        }
        self.current_sprite = 0
        self.current_animation = self.animaciones["down"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.player_sprites_powers = None

    def cargar_sprites(self, file_name, frames):
        """Divide la imagen en múltiples cuadros."""
        sprites = []
        sprite_sheet = pygame.image.load(f"{self.asset_path}/{file_name}").convert_alpha()
        sprite_width = sprite_sheet.get_width() // frames
        sprite_height = sprite_sheet.get_height()
        for i in range(frames):
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)
        return sprites

    def move(self, keys):
        """Mueve al jugador y cambia la animación según la dirección."""
        if self.can_put_invisible:
            self.invisibility_turtle()
        else:
            # Restablecer la visibilidad de las tortugas
            for turtle in self.turtles_group:
                if turtle.is_following_player:
                    turtle.is_visible = True

        if self.can_speed_turtle_up:
            self.speed_up_turtles()
        else:
            # Restablecer la velocidad de las tortugas
            for turtle in self.turtles_group:
                if turtle.is_following_player:
                    turtle.velocidad = 1
        

        if keys[pygame.K_DOWN]:
            self.y += self.velocidad
            self.direccion = "down"
        elif keys[pygame.K_UP]:
            self.y -= self.velocidad
            self.direccion = "up"
        elif keys[pygame.K_LEFT]:
            self.x -= self.velocidad
            self.direccion = "left"
        elif keys[pygame.K_RIGHT]:
            self.x += self.velocidad
            self.direccion = "right"
        else:
            self.direccion = None

        self.update_animation()

        # Control del tiempo de duración del power-up
        if self.has_power:
            self.power_duration += 1
            if self.power_duration >= 200:
                
                self.has_power = False
                self.power_duration = 0

                # Restablecer las habilidades del jugador
                self.can_get_turtles = False
                self.can_speed_turtle_up = False
                self.velocidad = 5
            
            # Agregar una animacion del personaje con el power-up , efecto de apagado
            self.apply_power_effect()
        

    def update_animation(self):
        """Actualiza la animación según la dirección."""
        if self.direccion:
            self.current_animation = self.animaciones[self.direccion]
            self.current_sprite += 1
            if self.current_sprite >= len(self.current_animation):
                self.current_sprite = 0
            self.image = self.current_animation[self.current_sprite]
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, pantalla):
        pantalla.blit(self.image, (self.x, self.y))
    
    def apply_power_effect(self):
        """Aplica un efecto visual durante el power-up (cambio de color y vibración)."""
        # Cambio de color (usando RGB)
        if self.power_duration % 2 == 0:  # Cambiar cada pocos ciclos
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            self.image.fill((r, g, b), special_flags=pygame.BLEND_RGB_MULT)

        # Efecto de vibración (pequeños desplazamientos aleatorios)
        if self.power_duration % 5 == 0:
            self.rect.x += random.randint(-2, 2)  # Desplazamiento horizontal
            self.rect.y += random.randint(-2, 2)  # Desplazamiento vertical

        # Agregar opacidad (parpadeo)
        if self.power_duration % 20 == 0:
            alpha = random.randint(180, 255)
            self.image.set_alpha(alpha)

    # Creamos habilidades ocultas para el jugador

    # Las tortugas se vuelven invisibles si lo estan siguiendo
    def invisibility_turtle(self):
        for turtle in self.turtles_group:
            if turtle.is_following_player:
                turtle.is_visible = False
    
    # Aumentar la velocidad de las tortugas que lo siguen
    def speed_up_turtles(self):
        for turtle in self.turtles_group:
            if turtle.is_following_player:
                turtle.velocidad = 3
    
class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path):
        super().__init__()
        self.x = x
        self.y = y
        self.asset_path = asset_path  # Carpeta base de recursos
        self.frames, self.type = self.load_animations()  # Cargar las animaciones según el tipo
        self.current_sprite = 0
        self.image = self.frames[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.duration = 5000  # Duración del power-up (en frames)
        self.collected = False  # Variable para saber si el power-up fue recogido

    def load_animations(self):
        """Carga las animaciones del power-up según su tipo."""
        # Definir las rutas de los tipos de power-up
        power_up_types = {
            "speed": ["crystal_01.png", "crystal_02.png", "crystal_03.png"],
            "turtle_speed": ["herb_02.png", "herb_03.png"],
            "invisible_turtle_follower": ["potion_01.png", "potion_02.png", "potion_03.png", "potion_04.png"]
        }

        # Seleccionamos un tipo de power-up aleatorio
        selected_type = random.choice(list(power_up_types.keys()))
        frames = []
        
        # Cargar las imágenes de ese tipo
        for image_name in power_up_types[selected_type]:
            image_path = f"{self.asset_path}/{image_name}"
            frames.append(pygame.image.load(image_path).convert_alpha())

        return frames, selected_type  # Retornar las imágenes y el tipo de power-up

    def update(self):
        """Actualiza la animación del power-up."""
        if self.collected:
            return  # Si el power-up ya fue recogido, no actualiza más

        # Eliminar el power-up después de que haya pasado su duración
        if self.duration > 0:
            self.duration -= 1
        if self.duration < 20:
            # Generar un efecto de desaparición
            self.image.set_alpha(self.duration * 10)
        if self.duration == 0:
            self.kill()  # Si el power-up no se recogió, se elimina por tiempo

        # Actualizar la animación
        self.current_sprite += 1
        if self.current_sprite >= len(self.frames):
            self.current_sprite = 0
        self.image = self.frames[self.current_sprite]

    def apply_ability(self, player):
        """Aplica la habilidad al jugador."""
        if self.collected:
            return  # Si el power-up ya fue recogido, no aplicar la habilidad de nuevo

        # Aplicar la habilidad según el tipo de power-up
        if self.type == "invisible_turtle_follower":
            player.can_put_invisible = True
        elif self.type == "turtle_speed":
            player.can_speed_turtle_up = True
        elif self.type == "speed":
            player.speed = 12  # Ajustar la velocidad del jugador

        # Marcar como recogido y eliminarlo después de aplicar la habilidad
        self.collected = True
        self.kill()

    # Dibuja el power-up en la pantalla
    def draw(self, screen):
        if not self.collected:  # Solo dibujar si no fue recogido
            screen.blit(self.image, self.rect)

# settings
# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600
FPS = 48

# Rutas de archivos
ASSET_DIR = "assets/"
IMAGE_DIR = ASSET_DIR + "images/"
SOUND_DIR = ASSET_DIR + "sounds/"
FONT_DIR = ASSET_DIR + "fonts/"

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Codigo de menu

lg_bg = '#e4fccc'
dg_bg = '#071821'

gif_bg = GifBackground("../video.gif", (WIDTH, HEIGHT))


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


async def main():
    global following_turtle, score, time_left, start_time,start_time_dia,estado_actual, start_time_noche # Usamos la variable global para modificarla dentro del ciclo principal
    global foxes,enemies,eggs,crabs,egg_packs,player,boton_perros,boton_sirena,dialogue_box,turtles,powerups,tmx_map_dia,mapa_noche
    
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
                        global egg_packs
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

                        
                        main()
                        
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
        await asyncio.sleep(0)

    await asyncio.sleep(0)
              

asyncio.run(main())







