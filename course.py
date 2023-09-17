import pygame
import utilities

class Course():
    def __init__(self, coursename, objects):
        self.objects = objects

        self.tiles = []
        self.start = None
        with open(f"images/{coursename}.txt") as coursefile:
            for y, line in enumerate(coursefile):
                row = []
                for i in range(0, len(line) - 1, 2):
                    row.append(line[i])
                    if line[i] == utilities.COURSE_TILE_START:
                        x = i // 2
                        self.start = (x, y)
                self.tiles.append(row)

    def render_course(self, screen):
        for y_pos, line in enumerate(self.tiles):
            for x_pos, tile in enumerate(line):
                image = course_tile_images[tile]
                rect = pygame.Rect (x_pos * utilities.SCALE, y_pos * utilities.SCALE, utilities.SCALE, utilities.SCALE)
                screen.blit(image, rect)

course_tile_images = {
    utilities.COURSE_TILE_GRASS : pygame.transform.scale(pygame.image.load("images/grass.png"), (utilities.SCALE, utilities.SCALE)),
    utilities.COURSE_TILE_WATER : pygame.transform.scale(pygame.image.load("images/water.png"), (utilities.SCALE, utilities.SCALE)),
    utilities.COURSE_TILE_OFFCOURSE : pygame.transform.scale(pygame.image.load("images/dirt.png"), (utilities.SCALE, utilities.SCALE)),
    utilities.COURSE_TILE_START : pygame.transform.scale(pygame.image.load("images/start.png"), (utilities.SCALE, utilities.SCALE))
}