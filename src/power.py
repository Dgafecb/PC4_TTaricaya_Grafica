import pygame
import random

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path):
        super().__init__()
        self.x = x
        self.y = y
        self.asset_path = asset_path  # Carpeta base de recursos
        self.frames, self.type = self.load_animations()  # Cargar las animaciones según el tipo
        self.current_sprite = 0
        self.image = self.frames[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.duration = 5000  # Duración del power-up (en frames)
        self.collected = False  # Variable para saber si el power-up fue recogido

    def load_animations(self):
        """Carga las animaciones del power-up según su tipo."""
        # Definir las rutas de los tipos de power-up
        power_up_types = {
            "speed": ["crystal_01.png", "crystal_02.png", "crystal_03.png"],
            "turtle_speed": ["herb_02.png", "herb_03.png"],
            "invisible_turtle_follower": ["potion_01.png", "potion_02.png", "potion_03.png", "potion_04.png"]
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
        if self.collected:
            return  # Si el power-up ya fue recogido, no actualiza más

        # Eliminar el power-up después de que haya pasado su duración
        if self.duration > 0:
            self.duration -= 1
        if self.duration < 20:
            # Generar un efecto de desaparición
            self.image.set_alpha(self.duration * 10)
        if self.duration == 0:
            self.kill()  # Si el power-up no se recogió, se elimina por tiempo

        # Actualizar la animación
        self.current_sprite += 1
        if self.current_sprite >= len(self.frames):
            self.current_sprite = 0
        self.image = self.frames[self.current_sprite]

    def apply_ability(self, player):
        """Aplica la habilidad al jugador."""
        if self.collected:
            return  # Si el power-up ya fue recogido, no aplicar la habilidad de nuevo

        # Aplicar la habilidad según el tipo de power-up
        if self.type == "invisible_turtle_follower":
            player.can_put_invisible = True
        elif self.type == "turtle_speed":
            player.can_speed_turtle_up = True
        elif self.type == "speed":
            player.speed = 12  # Ajustar la velocidad del jugador

        # Marcar como recogido y eliminarlo después de aplicar la habilidad
        self.collected = True
        self.kill()

    # Dibuja el power-up en la pantalla
    def draw(self, screen):
        if not self.collected:  # Solo dibujar si no fue recogido
            screen.blit(self.image, self.rect)
