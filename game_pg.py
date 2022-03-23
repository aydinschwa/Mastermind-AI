import pygame as pg
import random
import itertools
import sys

pg.init()

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
COLOR_CHOICES = ["Red", "Green", "Blue", "Yellow", "Pink"]
GUESS_RADIUS = 20
HINT_RADIUS = 15
COLOR_MAP = {"Red": (255, 0, 0),
             "Green": (0, 255, 0),
             "Blue": (0, 0, 255),
             "Yellow": (255, 255, 0),
             "Pink": (255, 0, 255),
             "Black": (0, 0, 0),
             "White": (255, 255, 255),
             "": (1, 122, 1)}

# game state globals
ANSWER = random.choices(COLOR_CHOICES, k=5)
GUESSES_LEFT = 6
CURRENT_HOLE = 0

pg.display.set_caption("Mastermind")


def draw_guess_grid(guess_grid):
    # expects a 6 x 5 list of lists
    grid_y = 65
    for row in guess_grid:
        grid_x = 200
        for val in row:
            SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (40, 40)), (grid_x - 20, grid_y - 20))
            if val:
                pg.draw.circle(SCREEN, COLOR_MAP[val], (grid_x, grid_y), GUESS_RADIUS)
            grid_x += 60
        grid_y += 110


# TODO: this is appalling, I'm sure I can find a better way to draw the hints
def draw_hint_grid(hint_grid):
    grid_y = 35
    for row in hint_grid:
        grid_x = 55
        for i, val in enumerate(row):
            if i in (0, 1):
                SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 15, grid_y - 15))
                if val:
                    pg.draw.circle(SCREEN, COLOR_MAP[val], (grid_x, grid_y), HINT_RADIUS)
                grid_x += 60
            elif i == 2:
                SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 90 - 15, grid_y + 30 - 15))
                if val:
                    pg.draw.circle(SCREEN, COLOR_MAP[val], (grid_x - 90, grid_y + 30), HINT_RADIUS)
                grid_x = 55
            elif i in (3, 4):
                SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 15, grid_y + 60 - 15))
                if val:
                    pg.draw.circle(SCREEN, COLOR_MAP[val], (grid_x, grid_y + 60), HINT_RADIUS)
                grid_x += 60
        grid_y += 110


def draw_player_choices(choice_grid):
    grid_y = 700
    grid_x = 200
    choice_rects = []
    for val in choice_grid:
        choice_rects.append(pg.draw.circle(SCREEN, COLOR_MAP[val], (grid_x, grid_y), GUESS_RADIUS))
        grid_x += 60
    return choice_rects


def draw_submit_button():
    button_x = 45
    button_y = 680
    button_rect = pg.Rect(button_x, button_y, 80, 40)
    pg.draw.rect(SCREEN, (255, 255, 255), button_rect)
    button_word = GAME_FONT.render("Submit", True, (0, 0, 0))
    button_word_rect = button_word.get_rect(center=button_rect.center)
    SCREEN.blit(button_word, button_word_rect)
    return button_rect


def validate_guess(guess, ans):
    # iterates through guess and answer lists element-by-element. Whenever it finds a match,
    # removes the value from a copy of answer so that nothing is double counted.
    hints = []
    ans_temp = ans.copy()
    print(guess, ans_temp)
    # first pass for black pegs
    for i, (guess_elem, ans_elem) in enumerate(zip(guess, ans_temp)):
        if guess_elem == ans_elem:
            hints.append("Black")
            ans_temp[i] = ""

    # second pass for white pegs
    for guess_elem, ans_elem in zip(guess, ans_temp):
        if guess_elem in ans_temp:
            hints.append("White")
            ans_temp[ans_temp.index(guess_elem)] = ""
        else:
            hints.append("")

    random.shuffle(hints)

    return hints


while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()

            # choosing which colors to play
            choice_rects = draw_player_choices(COLOR_CHOICES)
            for color, rect in zip(COLOR_CHOICES, choice_rects):
                if rect.collidepoint(mouse_x, mouse_y):
                    if CURRENT_HOLE < 5:
                        GUESS_GRID[6 - GUESSES_LEFT][CURRENT_HOLE] = color
                        CURRENT_HOLE += 1

            # submitting a guess
            submit_rect = draw_submit_button()
            if submit_rect.collidepoint(mouse_x, mouse_y):
                if CURRENT_HOLE == 5:
                    guess = GUESS_GRID[6 - GUESSES_LEFT]
                    hints = validate_guess(guess, ANSWER)
                    HINT_GRID[6 - GUESSES_LEFT] = hints
                    GUESSES_LEFT -= 1
                    CURRENT_HOLE = 0

                    if guess == ANSWER:
                        print("HORRAY HOORAH")

                    elif guess != ANSWER and GUESSES_LEFT == 0:
                        print(ANSWER)

        # changing color choices before submitting
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                if CURRENT_HOLE > 0:
                    CURRENT_HOLE -= 1
                    GUESS_GRID[6 - GUESSES_LEFT][CURRENT_HOLE] = ""

    SCREEN.blit(BACKGROUND, (0, 0))
    draw_guess_grid(GUESS_GRID)
    draw_hint_grid(HINT_GRID)
    draw_player_choices(COLOR_CHOICES)
    draw_submit_button()

    pg.display.update()
