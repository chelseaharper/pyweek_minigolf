import utilities
import pygame

class Game():
    def __init__(self, screen, course, menu):
        self.screen = screen
        self.objects = []
        self.state = utilities.GameState.NONE
        self.playstate = utilities.PlayState.MENU
        self.course = pygame.image.load(f"images/{course}.png")
        self.menu = menu
    
    def set_up(self):
        self.menu.set_up()

    def change_course(self, course):
        pass

    def update(self):
        self.handle_events()
        if self.playstate == utilities.PlayState.MENU:
            self.menu.render_menu(self.screen)
        elif self.playstate == utilities.PlayState.COURSE:
            pass
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                utilities.end_game(self.state)
            for i in self.menu.buttons:
                if i.draw(self.screen):
                    if i.name == "Quit Game":
                        utilities.end_game(self.state)
                    if i.name == "Start Game":
                        pass