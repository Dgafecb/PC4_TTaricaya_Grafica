import pygame

def load_image(path, scale=None):
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

def load_tileset(image_path, tile_width, tile_height, scale=None):
    """Divide el tileset en tiles individuales y los escala si es necesario."""
    tiles = []
    tileset = pygame.image.load(image_path).convert_alpha()
    tileset_width, tileset_height = tileset.get_size()

    for row in range(0, tileset_height, tile_height):
        for col in range(0, tileset_width, tile_width):
            tile = tileset.subsurface((col, row, tile_width, tile_height))
            if scale:
                tile = pygame.transform.scale(tile, (scale[0], scale[1]))
            tiles.append(tile)

    return tiles


# Función para dibujar el mapa
def draw_map(screen, map_data, tiles, tile_width, tile_height):
    """Dibuja el mapa en la pantalla directamente con índices."""
    for row_index, row in enumerate(map_data):
        for col_index, tile_index in enumerate(row):
            if tile_index >= 0:  # Evitar índices negativos (espacios vacíos)
                x = col_index * tile_width
                y = row_index * tile_height
                screen.blit(tiles[tile_index], (x, y))




