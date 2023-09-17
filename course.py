import pygame
import utilities

class Course():
    def __init__(self, objects):
        self.courselist = []
        self.objects = objects
    
    def load_course(self, coursename):
        with open(f"images/{coursename}.txt") as coursefile:
            for line in coursefile:
                tiles = []
                for i in range(0, len(line) - 1, 2):
                    tiles.append(line[i])
                self.courselist.append(tiles)
    
    def render_course(self, screen):
        y_pos = 0
        for line in self.courselist:
            x_pos = 0
            for tile in line:
                image = course_tile_images[tile]
                rect = pygame.Rect (x_pos * utilities.SCALE, y_pos * utilities.SCALE, utilities.SCALE, utilities.SCALE)
                screen.blit(image, rect)
                x_pos += 1
            y_pos += 1

course_tile_images = {
    utilities.COURSE_TILE_GRASS : pygame.transform.scale(pygame.image.load("images/grass.png"), (utilities.SCALE, utilities.SCALE)),
    utilities.COURSE_TILE_WATER : pygame.transform.scale(pygame.image.load("images/water.png"), (utilities.SCALE, utilities.SCALE)),
    utilities.COURSE_TILE_OFFCOURSE : pygame.transform.scale(pygame.image.load("images/dirt.png"), (utilities.SCALE, utilities.SCALE)),
    utilities.COURSE_TILE_START : pygame.transform.scale(pygame.image.load("images/start.png"), (utilities.SCALE, utilities.SCALE))
}