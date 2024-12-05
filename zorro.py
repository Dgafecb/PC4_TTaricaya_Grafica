import pygame
import os
import random
from settings import WIDTH, HEIGHT

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
            "idle_left": self.cargar_sprites("GandalfHardcore fox.png", 0),
            "idle_right": self.cargar_sprites_inv("GandalfHardcore fox.png", 0),
            "walk_right": self.cargar_sprites("GandalfHardcore fox.png", 1),
            "walk_left": self.cargar_sprites_inv("GandalfHardcore fox.png", 1),
            "attack": self.cargar_sprites("GandalfHardcore fox.png", 1),
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

