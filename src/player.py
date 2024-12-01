import pygame
import pytmx

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path, map_file):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 5
        self.direccion = "down"
        self.asset_path = asset_path
        self.map = pytmx.load_pygame(map_file)  # Cargar el mapa de Tiled

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
