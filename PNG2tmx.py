from PIL import Image
import xml.etree.ElementTree as ET

# Función para dividir la imagen en tiles
def dividir_imagen_en_tiles(imagen_path, tamano_tile=32):
    img = Image.open(imagen_path)
    img_width, img_height = img.size
    tiles = []

    # Dividir la imagen en tiles
    for y in range(0, img_height, tamano_tile):
        for x in range(0, img_width, tamano_tile):
            tile = img.crop((x, y, x + tamano_tile, y + tamano_tile))
            tiles.append(tile)

    return tiles, img_width // tamano_tile, img_height // tamano_tile

# Función para guardar el mapa TMX usando ElementTree
def guardar_mapa_tmx(tiles, map_width, map_height, salida_tmx_path, tileset_image_path, tamano_tile=32):
    # Crear el elemento raíz del archivo TMX
    map_elem = ET.Element('map', {
        'version': '1.0',
        'tiledversion': '1.9.2',
        'orientation': 'orthogonal',
        'width': str(map_width),
        'height': str(map_height),
        'tilewidth': str(tamano_tile),
        'tileheight': str(tamano_tile),
    })

    # Crear un tileset real para representar los tiles
    tileset_elem = ET.SubElement(map_elem, 'tileset', {
        'firstgid': '1',
        'name': 'tileset',
        'tilewidth': str(tamano_tile),
        'tileheight': str(tamano_tile),
        'spacing': '0',
        'margin': '0'
    })

    # Añadir el archivo de imagen al tileset
    image_elem = ET.SubElement(tileset_elem, 'image', {
        'source': tileset_image_path,
        'width': str(len(tiles) * tamano_tile),
        'height': str(tamano_tile)
    })

    # Crear la capa de tiles
    layer_elem = ET.SubElement(map_elem, 'layer', {
        'name': 'Layer 1',
        'width': str(map_width),
        'height': str(map_height)
    })

    # Crear el array de datos de los tiles
    data_elem = ET.SubElement(layer_elem, 'data', encoding='csv')

    # Aquí debemos añadir las ID de los tiles en formato CSV
    tile_ids = []
    for y in range(map_height):
        for x in range(map_width):
            # Asignar un ID de tile secuencialmente (esto se puede personalizar)
            tile_ids.append(str((y * map_width + x) + 1))

    data_elem.text = ','.join(tile_ids)

    # Crear el árbol XML y guardarlo en un archivo
    tree = ET.ElementTree(map_elem)
    tree.write(salida_tmx_path)

# Función para convertir PNG a TMX
def convertir_png_a_tmx(imagen_path, salida_tmx_path, tileset_image_path, tamano_tile=32):
    tiles, map_width, map_height = dividir_imagen_en_tiles(imagen_path, tamano_tile)
    guardar_mapa_tmx(tiles, map_width, map_height, salida_tmx_path, tileset_image_path, tamano_tile)

# Convertir la imagen PNG a TMX
convertir_png_a_tmx("MapaNoche.png", "MapaNoche.tmx", "tileset.png", tamano_tile=32)
