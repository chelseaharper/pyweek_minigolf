import utilities
import pygame
import objects

class Game():
    def __init__(self, screen, course, menu, gamestate):
        self.screen = screen
        self.objects = []
        self.state = utilities.GameState.NONE
        self.playstate = utilities.PlayState.MENU
        self.course = course
        self.menu = menu
        self.gamestate = gamestate
        self.ball = objects.Box(10, 11, 0, 0, utilities.SCALE, utilities.SCALE, "ball")
    
    def set_up(self):
        self.objects.append(self.ball)
        for i in self.course.objects:
            self.objects.append(i)

    def change_course(self, course):
        self.course.load_course(course)
        self.objects = []
        self.set_up()

    def update(self):
        self.handle_events() #accepts input from keyboard or mouse
        if self.playstate == utilities.PlayState.MENU: #displays menu when player wishes to see menu
            self.menu.render_menu(self.screen)
        elif self.playstate == utilities.PlayState.COURSE: #displays course and objects on course, including player ball
            self.screen.fill(utilities.BLACK)
            self.course.load_course("course1")
            self.course.render_course(self.screen)
            for object in self.objects:
                object.render_object(self.screen)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                utilities.end_game(self.state)
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
            for i in self.menu.buttons:
                if i.draw(self.screen):
                    if i.name == "Quit Game":
                        utilities.end_game(self.state)
                    if i.name == "Play Game":
                        self.playstate = utilities.PlayState.COURSE
                        self.gamestate = utilities.GameState.RUNNING
    
    def move_unit(self, unit, position_change): #determines if movement is valid; can be adjusted to cause player ball to return to start when invalid
        new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]
        if new_position[0] < 0 or new_position[0] > (len(self.course.courselist[0]) - 1):
            return
        if new_position[1] < 0 or new_position[1] > ((len(self.course.courselist) / 2) - 1):
            return
        if self.course.courselist[new_position[1]][new_position[0]] in utilities.OFFCOURSE:
            return
        unit.update_position(new_position)