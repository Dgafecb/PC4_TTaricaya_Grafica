import pygame

class DialogueBox:
    def __init__(self, letters_path, position, text_speed=2, box_width=700, box_height=120, letter_size=(16, 16)):
        """
        Inicializa el cuadro de diálogo.
        :param letters_path: Carpeta donde están las imágenes de letras.
        :param position: Posición del cuadro de diálogo (x, y).
        :param text_speed: Velocidad de animación del texto.
        :param box_width: Ancho del cuadro de diálogo.
        :param box_height: Alto del cuadro de diálogo.
        :param letter_size: Tamaño de cada letra (ancho, alto).
        """
        self.letters_path = letters_path
        self.position = position
        self.text_speed = text_speed
        self.box_width = box_width
        self.box_height = box_height
        self.letter_width, self.letter_height = letter_size
        self.text = ""
        self.visible_text = ""
        self.current_index = 0
        self.is_visible = False
        self.font = pygame.font.SysFont("arial", 18)  # Fuente para el texto simple de las instrucciones

    def set_text(self, text):
        """
        Establece el texto para mostrar y reinicia el progreso.
        """
        self.text = text
        self.visible_text = " " * len(text)  # Llena el cuadro con espacios al inicio
        self.current_index = 0
        self.is_visible = True

    def hide(self):
        """Oculta el cuadro de diálogo."""
        self.is_visible = False

    def update(self):
        """
        Actualiza el texto animado, mostrando caracteres gradualmente.
        """
        if self.is_visible and self.current_index < len(self.text):
            self.current_index += self.text_speed
            # Reemplaza gradualmente los espacios con las letras reales
            self.visible_text = self.text[:int(self.current_index)] + " " * (len(self.text) - int(self.current_index))

    def draw(self, screen):
        """
        Dibuja el cuadro de diálogo y el texto.
        """
        if self.is_visible:
            # Dibuja el rectángulo del cuadro de diálogo
            pygame.draw.rect(
                screen, 
                (50, 50, 50),  # Color del cuadro (gris oscuro)
                (self.position[0], self.position[1], self.box_width, self.box_height)
            )
            pygame.draw.rect(
                screen, 
                (200, 200, 200),  # Color del borde (gris claro)
                (self.position[0], self.position[1], self.box_width, self.box_height), 
                3  # Grosor del borde
            )

            # Dibuja las letras del texto principal
            x, y = self.position[0] + 20, self.position[1] + 20
            for char in self.visible_text:
                if char != " ":
                    try:
                        # Carga la imagen correspondiente al carácter
                        char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                        char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))
                        screen.blit(char_image, (x, y))
                    except FileNotFoundError:
                        print(f"Advertencia: Imagen no encontrada para '{char}'")
                x += self.letter_width  # Espacio entre letras

                # Salto de línea si el texto excede el ancho del cuadro
                if x > self.position[0] + self.box_width - 20:
                    x = self.position[0] + 20
                    y += self.letter_height + 5

            # Dibuja las instrucciones debajo del texto
            instructions = "Presiona: (ESPACIO) para terminar   (Q) para continuar"
            instructions_surface = self.font.render(instructions, True, (255, 255, 255))  # Texto blanco
            screen.blit(instructions_surface, (self.position[0] + 20, self.position[1] + self.box_height - 30))
