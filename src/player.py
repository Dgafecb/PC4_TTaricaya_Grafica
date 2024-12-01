import pygame
import pytmx
import xml.etree.ElementTree as ET
from map_reader import load_map, get_tile_value_at_position
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path, map_file, ids_colisionables, layer):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 5
        self.direccion = "down"
        self.asset_path = asset_path
        self.map = pytmx.load_pygame(map_file)  # Cargar el mapa de Tiled
        self.ids_colisionables = ids_colisionables  # Lista de IDs colisionables
        self.layer = layer
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

    def get_tile(self, row, col):
        """Obtiene el tile en la posición (row, col) del mapa."""
        return self.map.get_tile_gid(col // 32, row // 32, 0)  # Dividir por 32 para ajustar a los tiles

    def show_gidCSV(self, row, col):
        """Muestra el GID de la celda en la posición (row, col) del mapa."""
        gid = get_tile_value_at_position(self.map, row, col)
        print(f"GID en ({row}, {col}): {gid}")


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

    def es_colisionable(self, x, y):
        """Verifica si el tile en la posición (x, y) es colisionable."""
        tile_gid = self.map.get_tile_gid(x, y, 0)  # Capa 0, puedes cambiar el índice si es necesario
        
        if tile_gid in self.ids_colisionables:
            print("BLOQUE COLISIONABLE")  # Imprimir en consola para ver si está funcionando
            return True
        return False

    def move(self, keys):
        """Mueve al jugador y cambia la animación según la dirección."""
        nueva_x, nueva_y = self.x, self.y  # Variables para la nueva posición

        if keys[pygame.K_DOWN]:
            nueva_y += self.velocidad
        elif keys[pygame.K_UP]:
            nueva_y -= self.velocidad
        elif keys[pygame.K_LEFT]:
            nueva_x -= self.velocidad
        elif keys[pygame.K_RIGHT]:
            nueva_x += self.velocidad

        # Obtener las coordenadas del tile (dividiendo por el tamaño del tile, en este caso 32)
        tile_x = nueva_x // 32
        tile_y = nueva_y // 32

        # Mostrar el GID del tile en la nueva posición
        self.show_gidCSV(tile_y, tile_x)

        # Verificar si la nueva posición es colisionable
        if not self.es_colisionable(nueva_x // 32, nueva_y // 32):  # Dividir por 32 para ajustar a los tiles
            self.x = nueva_x
            self.y = nueva_y

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
        """Dibuja al jugador en la pantalla."""
        pantalla.blit(self.image, (self.x, self.y))
