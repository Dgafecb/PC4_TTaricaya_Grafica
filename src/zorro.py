import pygame
import os
import random
from settings import WIDTH, HEIGHT

class Fox(pygame.sprite.Sprite):
    def __init__(self, asset_path, eggs_group):
        super().__init__()
        self.x = random.choice([WIDTH / 2, WIDTH])
        self.y = random.randint(100, HEIGHT - 100)
        self.velocidad = 2
        self.direccion = "walk_left"  # Camina hacia la izquierda por defecto
        self.asset_path = asset_path
        self.eggs_group = eggs_group

        # Cargar las animaciones
        self.animaciones = {
            "idle": self.cargar_sprites("GandalfHardcore doggy sheet 2.png", 0),  # Primer fila de la imagen
            "idle_left": self.cargar_sprites_inv("GandalfHardcore doggy sheet 2.png", 0),  # Invertir la misma animación para idle
            "walk_left": self.cargar_sprites("GandalfHardcore doggy sheet 2.png", 1),  # Segunda fila de la imagen
            "walk_right": self.cargar_sprites_inv("GandalfHardcore doggy sheet 2.png", 1),  # Segunda fila invertida para caminar a la derecha
            "attack": self.cargar_sprites("GandalfHardcore doggy sheet 2.png", 1),  # Usamos la misma animación para el ataque por ahora
        }

        self.current_sprite = 0
        self.current_animation = self.animaciones["walk_left"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Estado del zorro
        self.is_attacking = False
        self.attack_steps = 0
        self.target_egg = None
        self.attack_cooldown = 0  # Cooldown de ataque
        self.attack_count = 0  # Contador de ataques realizados

    def cargar_sprites(self, image_path, fila):
        """Corta la imagen principal en frames individuales para las animaciones."""
        sprites = []
        # Cargar la imagen completa
        sprite_sheet = pygame.image.load(os.path.join(self.asset_path, image_path)).convert_alpha()

        # Asumimos que la imagen tiene 2 filas y 6 columnas (12 frames en total)
        # Las dimensiones de cada sprite
        sprite_width = sprite_sheet.get_width() // 6  # Divide la imagen en 6 partes (columnas)
        sprite_height = sprite_sheet.get_height() // 2  # Divide la imagen en 2 partes (filas)

        # Recortar los frames de la fila indicada
        for i in range(6):  # Hay 6 frames por fila
            # Recortar la imagen para obtener el sprite individual
            rect = pygame.Rect(i * sprite_width, fila * sprite_height, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)

        return sprites

    def cargar_sprites_inv(self, image_path, fila):
        """Corta la imagen principal en frames individuales para las animaciones y las invierte."""
        sprites = []
        # Cargar la imagen completa
        sprite_sheet = pygame.image.load(os.path.join(self.asset_path, image_path)).convert_alpha()

        # Asumimos que la imagen tiene 2 filas y 6 columnas (12 frames en total)
        # Las dimensiones de cada sprite
        sprite_width = sprite_sheet.get_width() // 6  # Divide la imagen en 6 partes (columnas)
        sprite_height = sprite_sheet.get_height() // 2  # Divide la imagen en 2 partes (filas)

        # Recortar los frames de la fila indicada
        for i in range(6):  # Hay 6 frames por fila
            # Recortar la imagen para obtener el sprite individual
            rect = pygame.Rect(i * sprite_width, fila * sprite_height, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            # Invertir el sprite
            sprite_invertido = pygame.transform.flip(sprite, True, False)
            sprites.append(sprite_invertido)

        return sprites

    def update(self):
        """Actualiza la animación y la lógica del zorro."""
        self.find_closest_egg()

        # Control de cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1  # Reducir el cooldown
        
        if self.is_attacking and self.attack_cooldown == 0:
            self.current_animation = self.animaciones["attack"]
            self.attack_steps += 1
            if self.attack_steps >= len(self.current_animation):
                # Llama al método de eliminar huevo
                if self.target_egg:
                    self.target_egg.remove()  # Eliminar el huevo atacado

                self.attack_steps = 0
                self.attack_count += 1
                self.attack_cooldown = 90  # Establece el tiempo de cooldown
                
                if self.attack_count >= 3:  # Limitar a 3 ataques antes de establecer cooldown
                    self.attack_count = 0
                    self.attack_cooldown = 120  # Establecer cooldown más largo después de 3 ataques
                    self.is_attacking = False
                    self.current_animation = self.animaciones["walk_left"]
        else:
            if not self.is_attacking:
                if self.direccion == "walk_left":
                    self.current_animation = self.animaciones["walk_left"]
                else:
                    self.current_animation = self.animaciones["walk_right"]

        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            self.current_sprite = 0

        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Mover hacia la izquierda o derecha
        if self.target_egg:
            if self.target_egg.x < self.x:
                self.x -= self.velocidad
                self.direccion = "walk_left"
            elif self.target_egg.x > self.x:
                self.x += self.velocidad
                self.direccion = "walk_right"

            if self.target_egg.y > self.y:
                self.y += self.velocidad
            elif self.target_egg.y < self.y:
                self.y -= self.velocidad
        else:
            if self.direccion == "walk_left":
                self.x -= self.velocidad
                if self.x < 0:  # Cuando el zorro llegue al borde izquierdo, reinicia
                    self.x = WIDTH
            else:
                self.x += self.velocidad
                if self.x > WIDTH:  # Cuando el zorro llegue al borde derecho, reinicia
                    self.x = 0

    def attack(self):
        """Inicia el ataque del zorro si no está en cooldown."""        
        if self.attack_cooldown == 0:  # Solo atacar si no hay cooldown
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
            # Verificar si el huevo está lo suficientemente cerca
            if distance < min_distance and distance < 100:
                min_distance = distance
                closest_egg = egg

        self.target_egg = closest_egg

    def draw(self, screen):
        """Dibuja el zorro en la pantalla."""
        screen.blit(self.image, (self.x, self.y))
