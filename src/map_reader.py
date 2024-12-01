import xml.etree.ElementTree as ET

def load_map(file_path):
    """Carga el archivo XML y devuelve la estructura del mapa."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def get_tile_value_at_position(tmx_map, row, col):
    """Obtiene el valor de la celda en la posición (row, col) del mapa usando pytmx."""
    layer = tmx_map.get_layer_by_name('Tile Layer 1')  # Obtener la capa por nombre
    # Acceder al GID del tile en la posición (col, row)
    tile = layer.data[row][col]  # Obtener el GID del tile directamente desde la capa
    return tile  # Devolver el GID del tile
