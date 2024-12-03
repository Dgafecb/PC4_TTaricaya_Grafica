import pygame
import pygame_menu
import os
import sys
import imageio
from utils import imprimir_letras
from gif import GifBackground
import subprocess
WIDTH = 800
HEIGHT = 600
green = (228, 252, 204)


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def set_color(texto, color, font_size=30):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(texto, True, color)
    return text_surface

pygame.mixer.init()
music_menu = "../assets/sounds/arcade.ogg"

try:
    pygame.mixer.music.load(music_menu)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    print("Música cargada correctamente.")
except Exception as e:
    print(f"Error al cargar la música: {e}")

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Taricaya')

gif_bg = GifBackground("../video.gif", (WIDTH, HEIGHT))

def fade_out():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        surface.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(40)

def start_game():
    pygame.mixer.music.stop()
    fade_out()
    pygame.quit()
    #os.system("python main.py")
    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar ejecutar main.py: {e}")
    sys.exit()


def create_instructions_menu():
    instructions_menu = pygame_menu.Menu('Instrucciones', WIDTH, HEIGHT, theme=theme)
    
    # Agregar las instrucciones
    instructions_menu.add.label("1. Usa las flechas del teclado para moverte por el mapa.",font_color=green)
    instructions_menu.add.label("2. Usa \"A\" para guiar a las tortugas.",font_color=green)
    instructions_menu.add.label("3. Usa \"S\" para darles un empujon.",font_color=green)
    
    # Agregar el botón "Volver" en una posición más baja
    back_button = instructions_menu.add.button('Volver', go_back_to_main_menu, font_color=green)
    
    # Cambiar la posición del botón manualmente
    back_button.set_position(WIDTH // 2 -50, HEIGHT - 100)  # Ajusta estas coordenadas según sea necesario
    
    return instructions_menu


def go_back_to_main_menu():
    global current_menu
    current_menu = menu



theme = pygame_menu.themes.THEME_GREEN.copy()
theme.background_color = (0, 0, 0, 0)
theme.title_font_color = green
theme.button_font_color = green

menu = pygame_menu.Menu('         Taricaya: Guardian del Amazonas        ', WIDTH, HEIGHT, theme=theme)
menu.add.button('Empezar Juego', start_game)
menu.add.button('Ver Instrucciones', lambda: switch_menu(instructions_menu))
menu.add.button('Salir', pygame_menu.events.EXIT)

instructions_menu = create_instructions_menu()

current_menu = menu

def switch_menu(new_menu):
    global current_menu
    current_menu = new_menu

if __name__ == "__main__":
    clock = pygame.time.Clock()

    running = True
    while running:
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        surface.blit(gif_bg.get_frame(), (0, 0))  # Renderizar el fondo GIF
        current_menu.update(events)
        current_menu.draw(surface)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
