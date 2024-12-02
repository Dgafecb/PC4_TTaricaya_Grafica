import pygame
import random
import time

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image_normal, image_pressed, sound_file, scale_factor=1.5): # scale_factor permite escalar el tamaño de los sprites x1.5 default
        super().__init__()  # Inicializa la clase base Sprite
        self.x = x
        self.y = y
        self.scale_factor = scale_factor  # Factor de escalado

        # Carga y escala las imágenes
        self.image_normal = pygame.image.load(image_normal).convert_alpha()
        self.image_pressed = pygame.image.load(image_pressed).convert_alpha()
        
        # Incrementar el tamaño de las imágenes
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
        
        self.image = self.image_normal  # Imagen por defecto
        self.rect = self.image.get_rect(topleft=(x, y))  # Posición inicial del botón
        self.is_pressed = False  # Estado de si el botón está presionado
        
        # Carga el sonido
        self.sound = pygame.mixer.Sound(sound_file)
        self.sound_channel = None  # Para rastrear el canal donde se reproduce el sonido
        self.start_time = None  # Para controlar cuándo comenzó el sonido

    def check_collision(self, player):
        """Verifica la colisión con el player y presiona el botón si colisiona."""
        if self.rect.colliderect(player.rect):
            if not self.is_pressed:  # Solo ejecuta acciones si no estaba presionado
                self.sound_channel = self.sound.play()
                self.start_time = time.time()  # Marca el tiempo en que comienza el sonido
                self.image = self.image_pressed  # Cambia a la imagen presionada
                self.is_pressed = True  # Marca el botón como presionado
                self.change_position()  # Cambia la posición del botón
        else:
            self.image = self.image_normal  # Cambia de vuelta a la imagen normal
            self.is_pressed = False  # Marca el botón como no presionado

    def update(self):
        """Actualiza el estado del botón, incluyendo detener el sonido si ha pasado tiempo."""
        if self.sound_channel and self.start_time:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 5:  # Detiene el sonido después de 5 segundos
                self.sound_channel.stop()
                self.start_time = None  # Resetea el temporizador

    def change_position(self):
        """Cambia la posición del botón a un lugar aleatorio en la pantalla."""
        width, height = 520, 600  # Dimensiones del área de movimiento del botón
        new_x = random.randint(0, width - self.rect.width)
        new_y = random.randint(80, height - self.rect.height)
        self.rect.topleft = (new_x, new_y)
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        """Dibuja el botón en la pantalla."""
        screen.blit(self.image, (self.x, self.y))


"""
#Antes de main
from buttons import Button
boton_sirena = Button(100, 100, '../assets/images/botones_assets/boton_A.png',
                       '../assets/images/botones_assets/boton_A_presionado.png',
                       '../assets/sounds/effects/policia/police_2.wav')
boton_perros = Button(200, 200,  '../assets/images/botones_assets/boton_B.png',
                       '../assets/images/botones_assets/boton_B_presionado.png',
                       '../assets/sounds/effects/perros/dog_barking.wav')
# Junto a los update
boton_perros.check_collision(player)
boton_sirena.check_collision(player)
# Dentro del dibujo completo/luego del blit del mapa
boton_perros.draw(screen)
boton_sirena.draw(screen)
"""