import random
import pygame
from settings import WIDTH, HEIGHT
import time

class Turtle(pygame.sprite.Sprite):
    score = 0
    def __init__(self, x, y, asset_path):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 1
        self.direccion = "walk"
        self.asset_path = asset_path

        self.attack_counter = 0
        self.is_attacked = False

        self.animaciones = {
            "idle": self.cargar_sprites("Idle.png", 4),
            "walk": self.cargar_sprites("Walk.png", 6),
            "attack": self.cargar_sprites("Attack.png", 6),
            "hurt": self.cargar_sprites("Hurt.png", 8),  # Animación de herido (2 frames)
            "death": self.cargar_sprites("Death.png", 6)
        }
        self.current_sprite = 0
        self.current_animation = self.animaciones["walk"]
        self.image = self.current_animation[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.is_following_player = False
        self.is_attacking = False
        self.animation_steps = 0
        self.health = 3
        self.is_dead = False
        self.last_appearance_time = time.time()

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
            sprites.append(sprite)
            sprites.append(sprite)
            sprites.append(sprite)

        return sprites

    def update(self):
        """Actualiza la animación según la dirección."""
        # Control de animación para 'death' (si está muerta)
        if self.is_dead:
            self.current_animation = self.animaciones["death"]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)
            self.image = self.current_animation[self.animation_steps]
            self.rect = self.image.get_rect(center=(self.x, self.y))
       # Control de animación para 'attack'
        elif self.is_attacking:
            self.current_animation = self.animaciones["attack"]
            self.x += self.velocidad * 10
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)

            if self.animation_steps == 0:  # Cuando la animación de ataque termina
                self.is_attacking = False
                self.current_animation = self.animaciones["walk"]

        # Control de animación para 'hurt'
        elif self.is_attacked:
            self.current_animation = self.animaciones["hurt"]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)
            
            if self.animation_steps == 0:  # Cuando la animación de 'hurt' termina
                self.is_attacked = False  # Resetear el estado de ataque
                if self.health > 0:  # Solo vuelve a caminar si no está muerta
                    self.current_animation = self.animaciones["walk"]

        # Control de animación cuando sigue al jugador o está en modo "walk"
        elif self.is_following_player:
            self.current_animation = self.animaciones["walk"]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)

        else:
            self.current_animation = self.animaciones[self.direccion]
            self.animation_steps = self.update_sprite(self.animation_steps, self.current_animation)

        # Actualizamos la imagen de la tortuga
        self.image = self.current_animation[self.animation_steps]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update_sprite(self, animation_steps, current_animation):
        """Actualizar el índice del sprite de la animación, reiniciando si es necesario."""
        animation_steps += 1
        if animation_steps >= len(current_animation):
            animation_steps = 0
            if self.is_dead:
                self.kill()
        return animation_steps

    def move(self, player):
        """Mueve la tortuga."""
        if self.is_following_player:
            if player.x > self.x:
                self.x += self.velocidad
                self.direccion = "walk"
            elif player.x < self.x:
                self.x -= self.velocidad
                self.direccion = "walk"

            if player.y > self.y:
                self.y += self.velocidad
            elif player.y < self.y:
                self.y -= self.velocidad

        elif not self.is_attacking and not self.is_dead:
            if self.direccion == "walk":
                self.x += self.velocidad
                if self.x > WIDTH:
                    self.x = random.randint(-50, -10)
                    self.y = random.randint(100, HEIGHT - 100)

            if self.x > WIDTH - 278:
                # Aumentar el puntaje si la tortuga llega al final
                Turtle.score += 1
                self.kill()

    def draw(self, screen):
        """Dibuja la tortuga en la pantalla."""
        screen.blit(self.image, (self.x, self.y))

    def attack(self):
        """Inicia el ataque de la tortuga.""" 
        self.animation_steps = 0       
        self.is_attacking = True

    def stop_following(self):
        """Deja de seguir al jugador y vuelve a caminar.""" 
        self.animation_steps = 0 
        self.is_following_player = False
        self.direccion = "walk"

    def start_following(self):
        """Comienza a seguir al jugador.""" 
        self.animation_steps = 0
        self.is_following_player = True

    def hurt(self):
        """Cuando la tortuga recibe daño."""   
        self.attack_counter += 1  
        self.is_attacked = True  
        if self.attack_counter >= 3:
            self.is_dead = True
            # Si la tortuga muere, restamos 1 al puntaje
            Turtle.score -= 1
        else:
            
            self.attack_steps = 0  
            self.health -= 1  # Reducir la vida de la tortuga
