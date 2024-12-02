import pygame
import os

class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path):
        super().__init__()
        self.x = x
        self.y = y
        self.asset_path = asset_path
        self.is_broken = False
        self.is_rolling = False

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
            sprites.append(sprite)
           
        return sprites

    def update(self):
        """Actualiza la animación y la lógica del huevo."""
        if self.is_broken:
            print("Huevo roto")
            self.current_animation = self.animaciones["breaking"]
        elif self.is_rolling:
            self.current_animation = self.animaciones["rolling"]
        else:
            self.current_animation = self.animaciones["idle"]

        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            if self.is_broken:  # El huevo roto mantiene el último frame
                self.current_sprite = len(self.current_animation) - 1
                # Eliminar el huevo roto
                self.kill()
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
        screen.blit(self.image, (self.x, self.y))
