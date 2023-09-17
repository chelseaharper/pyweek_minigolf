import pygame
import utilities

pygame.font.init()
font = pygame.font.Font(None, 45)


class Menu():
    def __init__(self, screen, buttons):
        self.screen = screen
        self.buttons = buttons
    
    def set_up(self):
        pass
    
    def render_menu(self, screen):
        for i in self.buttons:
            screen.blit(i.image, i.rect)
            screen.blit(i.text, i.textRect)
    
    def update_menu(self):
        self.handle_menu_events()
    
    def handle_menu_events(self):
        for event in pygame.event.get():
            for i in self.buttons:
                if i.draw(self.screen):
                    if i.name == "Quit Game":
                        utilities.end_game()



class Button():
    def __init__(self, x, y, name, image_name1, image_name2, width, height):
        self.position = [x, y]
        self.width = width
        self.height = height
        self.image = pygame.image.load(f"images/{image_name1}.png")
        self.rect = pygame.Rect(self.position[0], self.position[1], width, height)
        self.name = name
        self.image_name1 = image_name1
        self.image_name2 = image_name2
        self.clicked = False
        self.text = font.render(name, True, utilities.WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.position[0] + (width * 4), self.position[1] + (height * 2))
    
    def draw(self, screen):
        #Get the mouse position
        action = False
        position = pygame.mouse.get_pos()
        # Check if the mouse is over the button and has been clicked
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print("clicked!")
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

quit_button = Button(utilities.SCREEN_WIDTH // 3, 100, "Quit Game", "buttonLong_blue", "buttonLong_blue_pressed", 25, 10)
start_button = Button(utilities.SCREEN_WIDTH // 3, 50, "Start Game", "buttonLong_blue", "buttonLong_blue_pressed", 25, 10)