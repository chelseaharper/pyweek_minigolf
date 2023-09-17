from enum import Enum

class GameState(Enum):
    NONE = 0,
    RUNNING = 1,
    ENDED = 2

class PlayState(Enum):
    MENU = 0,
    COURSE = 1,
    ENDED = 2

SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def end_game(state):
    state = GameState.ENDED
    exit()