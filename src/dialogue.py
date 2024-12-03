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
    def change_position(self,new_position):
        self.position =  new_position
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

    def draw(self, screen, color_fondo = '#071821', color_letra='#e4fccc'):
        """
        Dibuja el cuadro de diálogo y el texto.
        """
        if self.is_visible:
            # Dibuja el rectángulo del cuadro de diálogo
            pygame.draw.rect(
                screen, 
                color_fondo,  # Color del cuadro # 346c54 (letra dia) - # #e4fccc (fondo dia)
                (self.position[0], self.position[1], self.box_width, self.box_height)
            )
            pygame.draw.rect(
                screen, 
                (200, 200, 200),  # Color del borde (gris claro)
                (self.position[0], self.position[1], self.box_width, self.box_height), 
                3  # Grosor del borde
            )

            # Calcular espacio disponible para el texto (considerando las instrucciones)
            instructions_height = 30  # Altura para las instrucciones
            available_height = self.box_height - instructions_height  # Espacio para el texto
            max_line_width = self.box_width - 40  # Ancho máximo para una línea de texto

            # Variables para el dibujo de texto
            x, y = self.position[0] + 20, self.position[1] + 20  # Posición inicial
            line_width = 0  # Ancho de la línea actual

            words = self.visible_text.split(" ")  # Dividir el texto en palabras
            for word in words:
                word_width = 0
                # Calcular el ancho de la palabra
                for char in word:
                    try:
                        # Cargar la imagen correspondiente al carácter
                        char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                        char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))
                        word_width += char_image.get_width()  # Sumar el ancho de cada carácter
                    except FileNotFoundError:
                        print(f"Advertencia: Imagen no encontrada para '{char}'")

                # Verificar si la palabra cabe en la línea
                if line_width + word_width <= max_line_width:
                    # Si cabe, agregar la palabra a la línea actual
                    for char in word:
                        try:
                            # Cargar la imagen correspondiente al carácter
                            char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                            char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))

                            # Dibuja el carácter en la pantalla
                            screen.blit(char_image, (x, y))

                            # Actualiza la posición en X y el ancho de la línea
                            x += self.letter_width
                            line_width += self.letter_width
                        except FileNotFoundError:
                            print(f"Advertencia: Imagen no encontrada para '{char}'")

                    # Agregar un espacio entre las palabras
                    x += self.letter_width  # Ajuste de espacio entre palabras
                    line_width += self.letter_width  # Ajuste del ancho de la línea
                else:
                    # Si no cabe, pasa a la siguiente línea
                    x = self.position[0] + 20  # Reiniciar la posición X
                    y += self.letter_height + 5  # Saltar a la siguiente línea
                    line_width = 0  # Reiniciar el ancho de la línea

                    # Asegurarnos de que la palabra cabe en la nueva línea
                    if y + self.letter_height + instructions_height > self.position[1] + self.box_height:
                        break  # Si no cabe más texto, no dibujar nada más

                    # Dibuja la palabra en la nueva línea
                    for char in word:
                        try:
                            # Cargar la imagen correspondiente al carácter
                            char_image = pygame.image.load(f"{self.letters_path}/{ord(char)}.png")
                            char_image = pygame.transform.scale(char_image, (self.letter_width, self.letter_height))

                            # Dibuja el carácter en la pantalla
                            screen.blit(char_image, (x, y))

                            # Actualiza la posición en X y el ancho de la línea
                            x += self.letter_width
                            line_width += self.letter_width
                        except FileNotFoundError:
                            print(f"Advertencia: Imagen no encontrada para '{char}'")

                    # Después de escribir la palabra, agregamos un espacio
                    x += self.letter_width  # Para dejar un espacio después de la palabra
                    line_width += self.letter_width  # Ajustar el ancho de la línea después del espacio

            # Dibuja las instrucciones debajo del texto
            instructions = "Presiona: (ESPACIO) para terminar   (Q) para continuar"
            instructions_surface = self.font.render(instructions, True, color_letra)  # Texto blanco
            screen.blit(instructions_surface, (self.position[0] + 20, self.position[1] + self.box_height - instructions_height))
