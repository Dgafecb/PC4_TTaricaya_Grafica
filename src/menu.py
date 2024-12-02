import pygame
import pygame_menu
from dialogue import draw_text

# Configuración del menú
def start_game():
    """Función para iniciar el juego."""
    global estado_actual
    estado_actual = ESTADOS["narrativa_inicio"]  # Cambia al estado inicial del juego
    main()  # Llama a la función principal del juego