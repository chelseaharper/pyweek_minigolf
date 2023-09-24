from enum import Enum


class GameState(Enum):
    NONE = (0,)
    RUNNING = (1,)
    ENDED = 2


class PlayState(Enum):
    MENU = (0,)
    COURSE = (1,)
    ENDED = 2


SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCALE = 32

COURSE_TILE_GRASS = "G"
COURSE_TILE_WATER = "W"
COURSE_TILE_START = "S"
COURSE_TILE_HOLE = "H"
COURSE_TILE_BLOCK = "B"
COURSE_TILE_POST = "P"
COURSE_TILE_OFFCOURSE = "`"

OFFCOURSE = [COURSE_TILE_WATER, COURSE_TILE_OFFCOURSE]


def end_game():
    exit()
