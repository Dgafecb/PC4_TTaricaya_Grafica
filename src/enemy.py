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
                    print(f"El enemigo ha tomado un huevo. Total: {len(self.eggs_taken)}")
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
