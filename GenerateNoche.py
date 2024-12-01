from PIL import Image, ImageEnhance

def convertir_a_noche(imagen_path, salida_path):
    # Cargar la imagen
    img = Image.open(imagen_path)

    # Convertir la imagen a RGB (para asegurar que tiene 3 componentes de color)
    img = img.convert("RGB")
    # Oscurecer la imagen
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.4)  # Reducir brillo para simular noche (ajusta este valor)

    # Cambiar el tono de la imagen para hacerla más fría (tono azul)
    pixels = img.load()  # Cargar los píxeles de la imagen

    # Aplicar un filtro de color (tono azul o frío)
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            # Aumentar el componente azul, disminuir rojo y verde para un efecto nocturno
            r = int(r * 0.7)  # Reducir el rojo
            g = int(g * 0.7)  # Reducir el verde
            b = min(255, int(b * 1.2))  # Aumentar el azul para dar un tono frío
            pixels[i, j] = (r, g, b)

    # Guardar la imagen modificada
    img.save(salida_path)

# Usar la función
convertir_a_noche("MapaDia.png", "MapaNoche.png")
