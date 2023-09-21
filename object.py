import pygame
import utilities
import pymunk


class Object:
    def __init__(self, x, y, width, height, image, name=None, needsbody=True):
        self.position = [(x + 0.5) * utilities.SCALE, (y + 0.5) * utilities.SCALE]
        self.width = width
        self.height = height
        self.needsbody = needsbody
        self.name = name
        self.image = pygame.image.load(f"images/{image}.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.set_up(1, utilities.SCALE / 2, 0.9)
    
    def set_up(self, mass, radius, elasticity):
        moment = pymunk.moment_for_circle(
                    mass=mass, inner_radius=0, outer_radius=radius
                )
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        

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

class Putter(Object):
    def __init__(self, x, y, width, height, image, name=None, needsbody=True):
        super().__init__(x, y, width, height, image, name, needsbody)
        self.image = pygame.transform.rotate(self.image, 270)
