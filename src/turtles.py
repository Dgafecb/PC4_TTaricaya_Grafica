import random
import pygame
from settings import WIDTH, HEIGHT

class Turtle(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 1  # Velocidad de la tortuga
        self.direccion = "walk"  # Estado inicial: camina hacia la derecha
        self.asset_path = asset_path

        # Cargar las animaciones
        self.animaciones = {
            "idle": self.cargar_sprites("Idle.png", 4),  # 4 frames para Idle
            "walk": self.cargar_sprites("Walk.png", 6),  # 6 frames para caminar
            "attack": self.cargar_sprites("Attack.png", 6),  # 6 frames para atacar
            "hurt": self.cargar_sprites("Hurt.png", 2),  # 2 frames para herido
            "death": self.cargar_sprites("Death.png", 6)  # 6 frames para muerte
        }
        self.current_sprite = 0
        self.current_animation = self.animaciones["walk"]  # Inicialmente camina
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Estado de la tortuga
        self.is_following_player = False  # Si la tortuga sigue al jugador
        self.is_attacking = False  # Si la tortuga está atacando
        self.attack_steps = 0  # Para controlar cuántos pasos da la tortuga durante el ataque

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

        return sprites

    def update(self):
        """Actualiza la animación según la dirección."""
        if self.is_attacking:
            self.current_animation = self.animaciones["attack"]
            self.attack_steps += 1
            # Avanza brutalmente hacia adelante durante el ataque
            self.x += self.velocidad * 10
            if self.attack_steps >= len(self.current_animation):
                # Después de completar la animación de ataque, vuelve a caminar
                self.is_attacking = False
                self.attack_steps = 0
                self.current_animation = self.animaciones["walk"]
        else:
            self.current_animation = self.animaciones[self.direccion]


        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            self.current_sprite = 0

        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self, player):
        """Mueve la tortuga."""
        if self.is_following_player:
            # La tortuga sigue al jugador
            if player.x > self.x:
                self.x += self.velocidad
                self.direccion = "walk"  # Asegura que la tortuga se mueva hacia la derecha
            elif player.x < self.x:
                self.x -= self.velocidad
                self.direccion = "walk"  # Asegura que la tortuga se mueva hacia la izquierda

            # Opcional: puedes agregar lógica para que la tortuga también siga al jugador verticalmente si es necesario
            if player.y > self.y:
                self.y += self.velocidad
            elif player.y < self.y:
                self.y -= self.velocidad
        elif not self.is_attacking:
            # La tortuga se mueve normalmente en su dirección predeterminada
            if self.direccion == "walk":
                self.x += self.velocidad
                if self.x > WIDTH:  # Si la tortuga sale de la pantalla por la derecha, se vuelve a generar al azar.
                    self.x = random.randint(-50, -10)
                    self.y = random.randint(100, HEIGHT - 100)

    def draw(self, screen):
        """Dibuja la tortuga en la pantalla."""
        screen.blit(self.image, (self.x, self.y))

    def attack(self):
        """Inicia el ataque de la tortuga."""        
        self.is_attacking = True  # Comienza la animación de ataque

    def stop_following(self):
        """Deja de seguir al jugador y vuelve a caminar."""
        self.is_following_player = False
        self.direccion = "walk"

    def start_following(self):
        """Comienza a seguir al jugador."""
        self.is_following_player = True