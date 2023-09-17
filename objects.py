import pygame
import utilities

class Object:
    def __init__(self, x, y, elasticity, friction, image):
        self.position = [x, y]
        self.elasticity = elasticity
        self.friction = friction
        self.image = pygame.image.load(f"images/{image}.png")
        self.image = pygame.transform.scale(self.image, (utilities.SCALE, utilities.SCALE))
        self.shape = None
    
    def render_object(self, screen):
        screen.blit(self.image, self.shape)
    
    def update_position(self, newposition):
        self.position = [newposition[0], newposition[1]]


class Box(Object):
    def __init__(self, x, y, elasticity, friction, width, height, image):
        super().__init__(x, y, elasticity, friction, image)
        self.shape = pygame.Rect(self.position[0] * utilities.SCALE, self.position[1] * utilities.SCALE, width, height)

class Ball(Object):
    def __init__(self, x, y, elasticity, friction, radius, image):
        super().__init__(x, y, elasticity, friction, image)
        self.radius = radius
        self.shape = None
    
    def render_object(self, screen):
        self.shape = pygame.draw.circle(screen, utilities.BLACK, self.position, self.radius)
        screen.blit(self.image, self.shape)

