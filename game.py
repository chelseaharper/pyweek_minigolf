import utilities
import pygame
import objects

class Game():
    def __init__(self, screen, courses, menu):
        self.screen = screen
        self.objects = []
        self.state = utilities.GameState.NONE
        self.playstate = utilities.PlayState.MENU
        self.courses = courses
        self.course = None
        self.menu = menu
        self.gamestate = utilities.GameState.NONE
        self.ball = objects.Object(10, 11, utilities.SCALE, utilities.SCALE, "ball")
    
    def set_up(self):
        self.objects.append(self.ball)
        for i in self.course.objects:
            self.objects.append(i)

    def change_course(self, course):
        self.course = course
        self.objects = []
        self.set_up()

    def update(self):
        self.handle_events() #accepts input from keyboard or mouse

        self.screen.fill(utilities.BLACK)

        if self.course is not None:
            self.course.render_course(self.screen)
            for object in self.objects:
                object.render_object(self.screen)

        if self.playstate == utilities.PlayState.MENU:
            self.menu.render_menu(self.screen)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                utilities.end_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playstate = utilities.PlayState.MENU
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    print("UP")
                    self.move_unit(self.ball, [0, -1])
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    print("DOWN")
                    self.move_unit(self.ball, [0, 1])
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    print("LEFT")
                    self.move_unit(self.ball, [-1, 0])
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    print("RIGHT")
                    self.move_unit(self.ball, [1, 0])
            if self.playstate == utilities.PlayState.MENU:
                for i in self.menu.buttons:
                    if i.handle_events():
                        if i.name == "Quit Game":
                            utilities.end_game()
                        if i.name == "Play Game":
                            if self.course is None:
                                self.change_course(self.courses[0])
                            self.playstate = utilities.PlayState.COURSE
                            self.gamestate = utilities.GameState.RUNNING
    
    def move_unit(self, unit, position_change): #determines if movement is valid; can be adjusted to cause player ball to return to start when invalid
        new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]
        if new_position[0] < 0 or new_position[0] > (len(self.course.tiles[0]) - 1):
            return
        if new_position[1] < 0 or new_position[1] > (len(self.course.tiles) - 1):
            return
        if self.course.tiles[new_position[1]][new_position[0]] in utilities.OFFCOURSE:
            return
        unit.update_position(new_position)