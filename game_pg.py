import pygame as pg
import random
import sys
from setup import *
from solver import MastermindSolver


class Mastermind:

    def __init__(self):
        self.guesses_left = 6
        self.current_hole = 0

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def draw_player_choices(choice_grid):
        grid_y = 700
        grid_x = 200
        choice_rects = []
        for val in choice_grid:
            choice_rects.append(pg.draw.circle(SCREEN, COLOR_MAP[val], (grid_x, grid_y), GUESS_RADIUS))
            grid_x += 60
        return choice_rects

    @staticmethod
    def draw_submit_button():
        button_x = 45
        button_y = 680
        button_rect = pg.Rect(button_x, button_y, 80, 40)
        pg.draw.rect(SCREEN, (255, 255, 255), button_rect)
        button_word = GAME_FONT.render("Submit", True, (0, 0, 0))
        button_word_rect = button_word.get_rect(center=button_rect.center)
        SCREEN.blit(button_word, button_word_rect)
        return button_rect

    @staticmethod
    def validate_guess(guess, ans):
        # iterates through guess and answer lists element-by-element. Whenever it finds a match,
        # removes the value from a copy of answer so that nothing is double counted.
        hints = []
        ans_temp = ans.copy()
        guess_temp = guess.copy()
        # first pass for black pegs
        for i, (guess_elem, ans_elem) in enumerate(zip(guess_temp, ans_temp)):
            if guess_elem == ans_elem:
                hints.append("Black")
                ans_temp[i] = ""
                guess_temp[i] = ""

        # second pass for white pegs
        for guess_elem, ans_elem in zip(guess_temp, ans_temp):
            if guess_elem in ans_temp and guess_elem:
                hints.append("White")
                ans_temp[ans_temp.index(guess_elem)] = ""

        if len(hints) < 5:
            hints.extend([""] * (5 - len(hints)))

        return hints

    def play(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()

                    # choosing which colors to play
                    choice_rects = self.draw_player_choices(COLOR_CHOICES)
                    for color, rect in zip(COLOR_CHOICES, choice_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            if self.current_hole < 5:
                                GUESS_GRID[6 - self.guesses_left][self.current_hole] = color
                                self.current_hole += 1

                    # submitting a guess
                    submit_rect = self.draw_submit_button()
                    if submit_rect.collidepoint(mouse_x, mouse_y):
                        if self.current_hole == 5:
                            guess = GUESS_GRID[6 - self.guesses_left]
                            hints = self.validate_guess(guess, ANSWER)
                            random.shuffle(hints)
                            HINT_GRID[6 - self.guesses_left] = hints
                            self.guesses_left -= 1
                            self.current_hole = 0

                            if guess == ANSWER:
                                print("HORRAY HOORAH")

                            elif guess != ANSWER and self.guesses_left == 0:
                                print(ANSWER)

                # changing color choices before submitting
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        if self.current_hole > 0:
                            self.current_hole -= 1
                            GUESS_GRID[6 - self.guesses_left][self.current_hole] = ""
                    if event.key == pg.K_SPACE:
                        print(MastermindSolver("".join(ANSWER)).solve())

            SCREEN.blit(BACKGROUND, (0, 0))
            self.draw_guess_grid(GUESS_GRID)
            self.draw_hint_grid(HINT_GRID)
            self.draw_player_choices(COLOR_CHOICES)
            self.draw_submit_button()

            pg.display.update()


Mastermind().play()
