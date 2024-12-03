import imageio
import pygame
class GifBackground:
    def __init__(self, gif_path, screen_size):
        self.reader = imageio.get_reader(gif_path)
        self.screen_size = screen_size
        self.frame_count = len(self.reader)
        self.current_frame = 0

    def get_frame(self):
        frame = self.reader.get_data(self.current_frame)
        self.current_frame = (self.current_frame + 1) % self.frame_count
        surf = pygame.image.fromstring(frame.tobytes(), frame.shape[1::-1], 'RGB')
        return pygame.transform.scale(surf, self.screen_size)
