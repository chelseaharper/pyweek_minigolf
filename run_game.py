import pygame
import utilities
import menu_builder
import game
import course

# Initial setup of pygame elements
pygame.init()
screen = pygame.display.set_mode((utilities.SCREEN_WIDTH, utilities.SCREEN_HEIGHT))
pygame.display.set_caption("Minigolf")
clock = pygame.time.Clock()

# Initial setup of game-specific elements, including definition of menus, game instance, and courses
# Need to move course and menu definition to separate document?
start_menu = menu_builder.Menu(
    screen, [menu_builder.quit_button, menu_builder.start_button]
)

course1 = course.Course("course1", [])
course2 = course.Course("course2", [])

game_instance = game.Game(screen, [course1, course2], start_menu)

# Main Game Loop; all game mechanics managed in game_instance.update()
while True:
    clock.tick(50)
    game_instance.update(1 / 50)
    pygame.display.flip()
