import pygame
import random

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path):
        super().__init__()
        self.x = x
        self.y = y
        self.asset_path = asset_path  # Carpeta base de recursos
        #self.ability = ability  # Habilidad que otorgará al jugador al colisionar
        self.frames, self.type = self.load_animations()  # Cargar las animaciones según el tipo
        self.current_sprite = 0
        self.image = self.frames[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.duration = 500  # Duración del power-up (en frames)

    def load_animations(self):
        """Carga las animaciones del power-up según su tipo."""
        # Definir las rutas de los tipos de power-up
        power_up_types = {
            "crystal": ["crystal_01.png", "crystal_02.png", "crystal_03.png"],
            "herb": ["herb_02.png", "herb_03.png"],
            "potion": ["potion_01.png", "potion_02.png", "potion_03.png", "potion_04.png"]
        }

        # Seleccionamos un tipo de power-up aleatorio
        selected_type = random.choice(list(power_up_types.keys()))
        frames = []
        
        # Cargar las imágenes de ese tipo
        for image_name in power_up_types[selected_type]:
            image_path = f"{self.asset_path}/{image_name}"
            frames.append(pygame.image.load(image_path).convert_alpha())

        return frames, selected_type  # Retornar las imágenes y el tipo de power-up

    def update(self):
        """Actualiza la animación del power-up."""
        # Eliminar el power-up después de que haya pasado su duración
        if self.duration > 0:
            self.duration -= 1
        if self.duration < 20:
            # Generar un efecto de desaparición
            self.image.set_alpha(self.duration * 10)
        if self.duration == 0:
            self.kill()

        # Actualizar la animación
        self.current_sprite += 1
        if self.current_sprite >= len(self.frames):
            self.current_sprite = 0
        self.image = self.frames[self.current_sprite]

    def apply_ability(self, player):
        """Aplica la habilidad al jugador."""
        # Aplicar la habilidad según el tipo de power-up
        if self.type == "herb":
            player.can_get_turtles = True
        elif self.type == "potion":
            player.can_speed_turtle_up = True
        elif self.type == "crystal":
            player.speed = 20

    # Dibuja el power-up en la pantalla
    def draw(self, screen):
        screen.blit(self.image, self.rect)
