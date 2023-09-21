import pygame
import utilities
import pymunk
import math


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
        if self.needsbody == True:
            moment = pymunk.moment_for_circle(
                    mass=mass, inner_radius=0, outer_radius=radius
                )
            self.body = pymunk.Body(mass, moment)
            self.body.position = self.position
            self.shape = pymunk.Circle(self.body, radius)
            self.shape.elasticity = elasticity
        else:
            pass
        

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
        self.original_image = self.image
        self.angle = 270
        self.image = pygame.transform.rotate(self.image, self.angle)
    
    def render_object(self, screen):
        shape = pygame.Rect(
            self.position[0] - utilities.SCALE / 2,
            self.position[1] - utilities.SCALE / 2,
            self.width * 2,
            self.height,
        )
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        screen.blit(self.image, shape)
    
    def update(self, mouse_pos):
        x_dist = self.position[0] - mouse_pos[0]
        y_dist = -(self.position[1] - mouse_pos[1]) # negative vector because pygame increases y down the screen
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.angle = angle
