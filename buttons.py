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