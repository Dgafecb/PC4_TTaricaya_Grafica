import pygame
import pytmx
import random 

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_path, map_file):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 5
        self.direccion = "down"
        self.asset_path = asset_path
        self.map = pytmx.load_pygame(map_file)  # Cargar el mapa de Tiled
        # Atributo que indica si el jugador ha recogido un power-up
        self.has_power = False
        # Tiempo de duración del power-up
        self.power_duration = 0

        
        self.can_get_turtles = False
        self.can_speed_turtle_up = False

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
        self.player_sprites_powers = None

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

        # Control del tiempo de duración del power-up
        if self.has_power:
            self.power_duration += 1
            if self.power_duration >= 200:
                
                self.has_power = False
                self.power_duration = 0

                # Restablecer las habilidades del jugador
                self.can_get_turtles = False
                self.can_speed_turtle_up = False
                self.velocidad = 5
            
            # Agregar una animacion del personaje con el power-up , efecto de apagado
            self.apply_power_effect()
        

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
    
    def apply_power_effect(self):
        """Aplica un efecto visual durante el power-up (cambio de color y vibración)."""
        # Cambio de color (usando RGB)
        if self.power_duration % 2 == 0:  # Cambiar cada pocos ciclos
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            self.image.fill((r, g, b), special_flags=pygame.BLEND_RGB_MULT)

        # Efecto de vibración (pequeños desplazamientos aleatorios)
        if self.power_duration % 5 == 0:
            self.rect.x += random.randint(-2, 2)  # Desplazamiento horizontal
            self.rect.y += random.randint(-2, 2)  # Desplazamiento vertical

        # Agregar opacidad (parpadeo)
        if self.power_duration % 20 == 0:
            alpha = random.randint(180, 255)
            self.image.set_alpha(alpha)

    # Creamos habilidades ocultas para el jugador

    # Atraer tortugas a todas las tortugas cercanas en un radio
    def attract_turtles(self, turtles_group):
        for turtle in turtles_group:
            # Si la tortuga esta cerca del jugador
            if self.rect.colliderect(turtle.rect):
                turtle.is_following_player = True
    
    # Aumentar la velocidad de las tortugas que lo siguen
    def speed_up_turtles(self, turtles_group):
        for turtle in turtles_group:
            if turtle.is_following_player:
                turtle.velocidad = 3
    
