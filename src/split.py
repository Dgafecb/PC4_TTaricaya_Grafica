from PIL import Image
import os

def split_ascii_image(image_path, output_dir, char_width, char_height, start_ascii=32):
    """
    Divide una imagen ASCII en caracteres individuales y los guarda como imágenes nombradas por sus códigos ASCII.
    """
    image = Image.open(image_path)
    img_width, img_height = image.size

    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Contador para asignar códigos ASCII
    ascii_code = start_ascii

    for y in range(0, img_height, char_height):
        for x in range(0, img_width, char_width):
            if ascii_code > 126:  # Limita a los caracteres ASCII imprimibles (32 a 126)
                break

            # Recortar la letra
            box = (x, y, x + char_width, y + char_height)
            char_image = image.crop(box)

            # Guardar la letra con el nombre basado en el código ASCII
            filename = f"{ascii_code}.png"
            char_image.save(os.path.join(output_dir, filename))
            print(f"Guardado: {filename}")

            # Incrementar el código ASCII
            ascii_code += 1

# Configuración
image_path = "../assets/images/ui/letters/ascii 01.png"  # Cambia al path de tu imagen
output_dir = "../assets/images/ui/ascii/"               # Carpeta donde guardarás las letras
char_width = 8                                          # Ancho de cada carácter
char_height = 8                                         # Alto de cada carácter

# Llamar a la función
split_ascii_image(image_path, output_dir, char_width, char_height)

# Para extraer las imagenes de la imagen ascci 2.png
image_path = "../assets/images/ui/letters/ascii 02.png"  # Cambia al path de tu imagen
output_dir = "../assets/images/ui/ascii_noche/"               # Carpeta donde guardarás las letras
char_width = 8                                          # Ancho de cada carácter
char_height = 8                                         # Alto de cada carácter

# Llamar a la función
split_ascii_image(image_path, output_dir, char_width, char_height)
