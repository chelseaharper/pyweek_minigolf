import pygame
import utilities


class Object:
    def __init__(self, x, y, width, height, image):
        self.position = [x * utilities.SCALE, y * utilities.SCALE]
        self.width = width
        self.height = height
        self.image = pygame.image.load(f"images/{image}.png")
        self.image = pygame.transform.scale(
            self.image, (utilities.SCALE, utilities.SCALE)
        )

    def update_position(self, newposition):
        self.position = [newposition[0], newposition[1]]

    def render_object(self, screen):
        shape = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        screen.blit(self.image, shape)
