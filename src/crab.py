import pygame
import random
import os
from settings import WIDTH, HEIGHT

class Crab(pygame.sprite.Sprite):
    def __init__(self, asset_path, turtles_group):
        super().__init__()
        self.x = random.choice([WIDTH/2, WIDTH])
        self.y = random.randint(100, HEIGHT - 100)
        self.velocidad = 1
        self.direccion = "walk"
        self.asset_path = asset_path
        self.turtles_group = turtles_group

        # Cargar las animaciones
        self.animaciones = {
            "idle": self.cargar_sprites("Idle", 5),
            "walk": self.cargar_sprites("Moving", 4),
            "attack": self.cargar_sprites("Attack", 4),
        }
        self.current_sprite = 0
        self.current_animation = self.animaciones["walk"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Estado del cangrejo
        self.is_attacking = False
        self.attack_steps = 0
        self.target_turtle = None
        self.attack_cooldown = 0  # Cooldown de ataque
        self.attack_count = 0  # Contador de ataques realizados

    def cargar_sprites(self, folder, frames):
        """Carga los sprites desde una carpeta para una animación dada."""
        sprites = []
        for i in range(1, frames + 1):
            base_path = os.path.join(self.asset_path, folder)
            if folder == "Attack":
                sprite_path = os.path.join(base_path, f"Crab_Attack{i}.png")
            elif folder == "Idle":
                sprite_path = os.path.join(base_path, f"Crab{i}.png")
            else:
                sprite_path = os.path.join(base_path, f"CrabMoving{i}.png")
            
            try:
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprites.append(sprite)
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo {sprite_path}")
        
        return sprites

    def update(self):
        """Actualiza la animación y la lógica del cangrejo."""
        self.find_closest_turtle()

        
        # Control de cooldown de ataque
        if self.attack_cooldown > 0 :
            self.attack_cooldown -= 1  # Reducir el cooldown
         

        if self.is_attacking and self.attack_cooldown == 0:
            print("Attacking")
            self.current_animation = self.animaciones["attack"]
            self.attack_steps += 1
            if self.attack_steps >= len(self.current_animation):
                print("Attack done")
                # Llama al método hurt de la tortuga atacada
                if self.target_turtle:
                    self.target_turtle.hurt()

                self.attack_steps = 0
                self.attack_count += 1
                self.attack_cooldown = 120  # Establece el tiempo de cooldown
                
                if self.attack_count >= 3:  # Limitar a 3 ataques antes de establecer cooldown
                    self.attack_count = 0
                    self.attack_cooldown = 180  # Establecer cooldown más largo después de 3 ataques
                    self.is_attacking = False
                    self.current_animation = self.animaciones["walk"]
        else:
            if not self.is_attacking:
                self.current_animation = self.animaciones["walk"]

        self.current_sprite += 1
        if self.current_sprite >= len(self.current_animation):
            self.current_sprite = 0

        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Mover hacia la tortuga más cercana si existe un objetivo
        if self.target_turtle:
            if self.target_turtle.x > self.x:
                self.x += self.velocidad
            elif self.target_turtle.x < self.x:
                self.x -= self.velocidad

            if self.target_turtle.y > self.y:
                self.y += self.velocidad
            elif self.target_turtle.y < self.y:
                self.y -= self.velocidad

    def move(self):
        """Mueve el cangrejo hacia la tortuga más cercana o camina por su cuenta."""
        if self.target_turtle:
            if self.target_turtle.x > self.x:
                self.x += self.velocidad
            elif self.target_turtle.x < self.x:
                self.x -= self.velocidad

            if self.target_turtle.y > self.y:
                self.y += self.velocidad
            elif self.target_turtle.y < self.y:
                self.y -= self.velocidad
    
        else:
            if self.direccion == "walk":
                self.y += self.velocidad
                if self.y > HEIGHT or self.y < 0:
                    self.y = random.choice([0, HEIGHT])
                    self.x = random.randint(0, WIDTH)

    def attack(self):
        """Inicia el ataque del cangrejo si no está en cooldown."""        
        if self.attack_cooldown == 0:  # Solo atacar si no hay cooldown
            self.is_attacking = True
            

    def stop_attack(self):
        """Detiene el ataque."""        
        self.is_attacking = False

    def find_closest_turtle(self):
        """Encuentra la tortuga más cercana para atacar."""
        closest_turtle = None
        min_distance = float('inf')

        for turtle in self.turtles_group:
            distance = pygame.math.Vector2(self.x - turtle.x, self.y - turtle.y).length()

            if distance < min_distance and distance < 100:
                min_distance = distance
                closest_turtle = turtle

        self.target_turtle = closest_turtle

    def draw(self, screen):
        """Dibuja el cangrejo en la pantalla."""
        screen.blit(self.image, (self.x, self.y))
