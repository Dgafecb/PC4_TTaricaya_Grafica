import pygame

class AssetLoader:
    @staticmethod
    def load_image(image_path):
        return pygame.image.load(image_path).convert_alpha()

    @staticmethod
    def load_sprite_sheet(sprite_name, size=(32, 32)):
        sprite_sheet = AssetLoader.load_image(sprite_name + ".png")
        sprites = {}
        with open(sprite_name + ".data", "r") as data:
            for line in data:
                name, x, y, width, height = line.split(",")
                sprites[name] = pygame.transform.scale(sprite_sheet.subsurface(int(x), int(y), int(width), int(height)), size=size)
        return sprites