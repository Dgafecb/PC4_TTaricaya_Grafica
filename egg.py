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

