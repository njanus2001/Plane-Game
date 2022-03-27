import pygame


class Coin:
    """A class that represents a coin object in the game."""

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def move(self, velocity):
        self.y += velocity

    def is_off_screen(self, window_height):
        if self.y >= window_height:
            return True
