import random
import pygame as pg

pg.init()
pg.display.set_caption("Mastermind")

# screen background globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
BACKGROUND = pg.transform.scale(pg.image.load("assets/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
HOLE_BACKGROUND = pg.image.load("assets/peg.png")
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_FONT = pg.font.SysFont("Verdana", 15)

# game board globals
GUESS_GRID = [["" for _ in range(5)] for _ in range(6)]
HINT_GRID = [["" for _ in range(5)] for _ in range(6)]
COLOR_CHOICES = ["R", "G", "B", "Y", "P"]
GUESS_RADIUS = 20
HINT_RADIUS = 15
COLOR_MAP = {"R": (255, 0, 0),
             "G": (0, 255, 0),
             "B": (0, 0, 255),
             "Y": (255, 255, 0),
             "P": (255, 0, 255),
             "Black": (0, 0, 0),
             "White": (255, 255, 255),
             "": (1, 122, 1)}

# game state globals
ANSWER = random.choices(COLOR_CHOICES, k=5)
