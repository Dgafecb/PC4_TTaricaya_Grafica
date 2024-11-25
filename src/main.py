import pygame
from settings import WIDTH, HEIGHT, FPS

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guardianes de las Taricayas")
clock = pygame.time.Clock()

# Bucle principal

def main():
    running = True
    while running:
        # Mantener el bucle a la velocidad correcta
        clock.tick(FPS)

        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar

        # Dibujar
        

        # Después de dibujar todo, mostrarlo en la pantalla
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()