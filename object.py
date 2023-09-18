import pygame
import utilities


class Object:
    def __init__(self, x, y, width, height, image, needsbody = True):
        self.position = [(x + 0.5) * utilities.SCALE, (y + 0.5) * utilities.SCALE]
        self.width = width
        self.height = height
        self.needsbody = needsbody
        self.image = pygame.image.load(f"images/{image}.png")
        self.image = pygame.transform.scale(
            self.image, (utilities.SCALE, utilities.SCALE)
        )

    def update_position(self, newposition):
        self.position = [newposition[0], newposition[1]]

    def render_object(self, screen):
        shape = pygame.Rect(
            self.position[0] - utilities.SCALE / 2,
            self.position[1] - utilities.SCALE / 2,
            self.width,
            self.height,
        )
        screen.blit(self.image, shape)
