import pygame
import utilities
import menu_builder
import game

pygame.init()
screen = pygame.display.set_mode((utilities.SCREEN_WIDTH, utilities.SCREEN_HEIGHT))
clock = pygame.time.Clock()

state = utilities.GameState.NONE
start_menu = menu_builder.Menu(screen, [menu_builder.quit_button, menu_builder.start_button])
play_menu = menu_builder.Menu(screen, [menu_builder.quit_button, menu_builder.start_button])

game_instance = game.Game(screen, "start", start_menu)
game_instance.set_up()

while state != utilities.GameState.ENDED:
    clock.tick(50)
    if state == utilities.GameState.NONE:
        game_instance.update()
    elif state == utilities.GameState.RUNNING:
        pass
    pygame.display.flip()