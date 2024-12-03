import pygame
import pygame_menu
import os
import sys
import subprocess
from utils import imprimir_letras
from gif import GifBackground
from dialogue import DialogueBox  # Asegúrate de tener esta clase implementada

WIDTH = 800
HEIGHT = 600
# Colores de dia
lg_bg = '#e4fccc'
dg_bg = '#071821'

lg_font = '#e4fccc'
# Colores de noche

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
    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar ejecutar main.py: {e}")
    sys.exit()

def create_instructions_menu():
    # Crear cuadros de diálogo para las instrucciones
    dialogue_boxes = []

    box_width, box_height = 700, 100
    text_speed = 2
    letter_size = (16, 16)
    letters_path_day = "../assets/images/ui/ascii"  # Cambia a la ruta de tus letras
    letters_path_night = "../assets/images/ui/ascii_noche"  # Cambia a la ruta de tus letras

    # Crear los cuadros de diálogo
    dialogue_boxes.append(DialogueBox(letters_path_day, (50, 50), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text("Usa las flechas del teclado para moverte por el mapa.")

    dialogue_boxes.append(DialogueBox(letters_path_day, (50, 150), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text("a. De dia: Usa \"A\" para guiar a las tortugas.\nUsa \"S\" para darles un empujon.")

    dialogue_boxes.append(DialogueBox(letters_path_night, (50, 250), text_speed, box_width, box_height, letter_size))
    dialogue_boxes[-1].set_text("b. De noche: Presiona los botones para ahuyentar depredadores.")

    # Cambiando los fondos de los cuadros de diálogo
    # Dibujar y actualizar cuadros de diálogo
    dialogue_boxes[0].draw_menu(surface,color_fondo=lg_bg, color_letra=dg_bg)
    dialogue_boxes.update()
    dialogue_boxes[1].draw_menu(surface,color_fondo=lg_bg, color_letra=dg_bg)
    dialogue_boxes.update()
    dialogue_boxes[2].draw_menu(surface,color_fondo= dg_bg, color_letra=lg_bg)
    dialogue_boxes.update()
   
    # Botón para volver al menú principal
    back_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 40)
    back_button_color = (100, 200, 100)

    # Función para manejar eventos
    def handle_events(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button_rect.collidepoint(event.pos):
                return True
        return False

    def instructions_menu_loop():
        clock = pygame.time.Clock()
        running = True

        while running:
            surface.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if handle_events(event):
                    running = False

            

            # Dibujar botón "Volver"
            pygame.draw.rect(surface, back_button_color, back_button_rect)
            font = pygame.font.SysFont('arial', 24)
            text = font.render("Volver", True, (0, 0, 0))
            surface.blit(text, (back_button_rect.x + 10, back_button_rect.y + 5))

            pygame.display.flip()
            clock.tick(60)

    instructions_menu_loop()

def go_back_to_main_menu():
    global current_menu
    current_menu = menu

theme = pygame_menu.themes.THEME_DARK.copy()
theme.background_color = (0, 0, 0, 0)
theme.button_font_color = lg_bg

menu = pygame_menu.Menu('         Taricaya: Guardian del Amazonas        ', WIDTH, HEIGHT, theme=theme)
menu.add.button('Empezar Juego', start_game)
menu.add.button('Ver Instrucciones', create_instructions_menu)
menu.add.button('Salir', pygame_menu.events.EXIT)

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