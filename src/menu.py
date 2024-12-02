import pygame
from asset_loader import AssetLoader
from utils import Manager

class Menu:
    def __init__(self,screen):
        self.screen = screen
        pygame.display.set_caption("Menu")
        self.play_button = Button(self.screen,250,229,300,150, "PlayButton", self.load_level)
        self.language_button = Button(self.screen,650,450,128,128, "LanguageButton", self.change_language)
        self.language_text = "ESPAÑOL" if Manager.get_language() == "es" else "ENGLISH"
    
    def load_level(self):
        Manager.change_level(Level1(self.screen))
    
    def change_language(self):
        Manager.set_language("en" if Manager.get_language() == "es" else "es")
        self.language_text = "ESPAÑOL" if Manager.get_language() == "es" else "ENGLISH"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw(self):
        self.screen.fill((153, 204, 255))
        self.play_button.draw()
        self.language_button.draw()
        font = pygame.font.Font("easvhs.ttf", 50)
        text = font.render(self.language_text, True, (0, 0, 0))
        self.screen.blit(text, (22, 22))

    def update(self,dt):
        self.handle_events()
        self.play_button.update()
        self.language_button.update()


class Button:
    def __init__(self,screen,x,y,width,height, image_name, clicked_handle):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_clicked = False
        self.image = AssetLoader.load_image(f"{image_name}.png")
        self.image_hover = AssetLoader.load_image(f"{image_name}Hover.png")
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.image_hover = pygame.transform.scale(self.image_hover,(self.width,self.height))
        self.clicked_handle = clicked_handle

    def on_click(self):
        self.clicked_handle()

    def draw(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            self.screen.blit(self.image_hover,(self.x,self.y))
        else:
            self.screen.blit(self.image,(self.x,self.y))

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if not click[0]:
            if self.is_clicked:
                self.on_click()
                self.is_clicked = False
                return
        self.is_clicked = False
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            if click[0]:
                self.is_clicked = True