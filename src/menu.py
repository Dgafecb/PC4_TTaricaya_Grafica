import pygame
import pygame_menu
from dialogue import draw_text
pygame.init()
surface = pygame.display.set_mode((600, 400))

# Ruta donde se encuentran las letras ASCII
letters_path = "../assets/images/ui/ascii"


draw_text(surface, "Hello World!", 100, 100)

menu = pygame_menu.Menu(800, 600, 'Welcome',
                       theme=pygame_menu.themes.THEME_GREEN)

menu.mainloop(surface)