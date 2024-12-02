from split import split_ascii_image

# Para extraer las imagenes de la imagen ascci 2.png
image_path = "../assets/images/ui/letters/ascii 02.png"  # Cambia al path de tu imagen
output_dir = "../assets/images/ui/ascii_noche/"               # Carpeta donde guardarás las letras
char_width = 8                                          # Ancho de cada carácter
char_height = 8                                         # Alto de cada carácter

# Llamar a la función
split_ascii_image(image_path, output_dir, char_width, char_height)