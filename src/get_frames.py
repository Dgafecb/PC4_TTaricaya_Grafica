import pygame
import os

def load_and_save_tiles(image_path, tile_width, tile_height, output_folder, scale=None):
    """Divide el tileset en tiles individuales y los guarda en una carpeta."""
    # Inicializar pygame y el display para poder usar convert_alpha()
    pygame.init()
    pygame.display.set_mode((1, 1))  # No es necesario mostrar la ventana, solo inicializarla

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tileset = pygame.image.load(image_path).convert_alpha()
    tileset_width, tileset_height = tileset.get_size()
    tile_count = 0

    for row in range(0, tileset_height, tile_height):
        for col in range(0, tileset_width, tile_width):
            tile = tileset.subsurface((col, row, tile_width, tile_height))
            if scale:
                tile = pygame.transform.scale(tile, (scale[0], scale[1]))

            # Guardar el tile en la carpeta de salida
            tile_filename = os.path.join(output_folder, f"tile_{tile_count}.png")
            pygame.image.save(tile, tile_filename)
            tile_count += 1

    print(f"Se han guardado {tile_count} tiles en '{output_folder}'.")

# Ejemplo de uso:
load_and_save_tiles("../assets/images/escenes/gentle forest v03.png", 32, 32, "../assets/images/ui/frames/", scale=(64, 64))
