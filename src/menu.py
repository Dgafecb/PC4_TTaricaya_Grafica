import pygame
import pygame_menu
import os
import sys

# Añadir la ruta del proyecto al path de Python
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

WIDTH = 800
HEIGHT = 600

# Inicializar Pygame
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Taricaya')

# Función para iniciar el juego
def start_game():
    os.system("python main.py")  # Ejecuta el archivo main.py

# Crear el submenú de instrucciones
def create_instructions_menu():
    instructions_menu = pygame_menu.Menu('Instrucciones', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    instructions_menu.add.label('Usa las flechas para moverte.')
    instructions_menu.add.label('Presiona ESPACIO para disparar.')
    instructions_menu.add.button('Volver', pygame_menu.events.BACK)
    return instructions_menu

# Cargar la imagen de fondo
try:
    # Ruta completa al archivo MapaDia.png desde el directorio raíz del proyecto
    background_image = pygame.image.load(os.path.join(project_root, "MapaDia.png"))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error cargando la imagen de fondo: {e}")
    background_image = None

# Crear un tema personalizado con fondo transparente
theme = pygame_menu.themes.THEME_GREEN.copy()
theme.background_color = (0, 0, 0, 0)  # Totalmente transparente

# Crear el menú principal
menu = pygame_menu.Menu('Taricaya', WIDTH, HEIGHT, theme=theme)
menu.add.button('Empezar Juego', start_game)
menu.add.button('Ver Instrucciones', lambda: instructions_menu.mainloop(surface))
menu.add.button('Salir', pygame_menu.events.EXIT)

# Generar el submenú de instrucciones
instructions_menu = create_instructions_menu()

# Bucle principal
if __name__ == "__main__":
    clock = pygame.time.Clock()

    running = True
    while running:
        # Capturar eventos
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Renderizar el fondo primero
        if background_image:
            surface.blit(background_image, (0, 0))
        else:
            # Fondo de color si no hay imagen
            surface.fill((50, 50, 50))  # Gris oscuro

        # Actualizar y dibujar el menú
        menu.update(events)
        menu.draw(surface)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar los FPS
        clock.tick(60)

    # Salir correctamente
    pygame.quit()
    sys.exit()