from setup import *
from solver import MastermindSolver


class Mastermind:

    def __init__(self):
        self.guesses_left = 6
        self.current_hole = 0

    @staticmethod
    def draw_guess_grid(guess_grid, x, y):
        grid_y = y
        for row in guess_grid:
            grid_x = x
            for val in row:
                SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (40, 40)), (grid_x - 20, grid_y - 20))
                if val:
                    pg.draw.circle(SCREEN, GUESS_COLOR_MAP[val], (grid_x, grid_y), GUESS_RADIUS)
                grid_x += 60
            grid_y += 110

    @staticmethod
    def draw_hint_grid(hint_grid, x, y):
        grid_y = y
        for row in hint_grid:
            # draw empty peg when there is no hint peg to draw
            row = [let for let in row]
            if len(row) < 5:
                row.extend([""] * (5 - len(row)))

            grid_x = x
            for i, val in enumerate(row):
                if i in (0, 1):
                    SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 15, grid_y - 15))
                    if val:
                        pg.draw.circle(SCREEN, HINT_COLOR_MAP[val], (grid_x, grid_y), HINT_RADIUS)
                    grid_x += 60
                elif i == 2:
                    SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 90 - 15, grid_y + 30 - 15))
                    if val:
                        pg.draw.circle(SCREEN, HINT_COLOR_MAP[val], (grid_x - 90, grid_y + 30), HINT_RADIUS)
                    grid_x = 55
                elif i in (3, 4):
                    SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 15, grid_y + 60 - 15))
                    if val:
                        pg.draw.circle(SCREEN, HINT_COLOR_MAP[val], (grid_x, grid_y + 60), HINT_RADIUS)
                    grid_x += 60
            grid_y += 110

    @staticmethod
    def draw_choices(choice_grid, x, y):
        choice_rects = []
        for val in choice_grid:
            choice_rects.append(pg.draw.circle(SCREEN, GUESS_COLOR_MAP[val], (x, y), GUESS_RADIUS))
            x += 60
        return choice_rects

    @staticmethod
    def draw_separators():
        # draw separator between guesses and choices
        pg.draw.line(SCREEN, (0, 0, 0), (0, 670), (500, 670), 10)

        # draw separator between guess and hints
        pg.draw.line(SCREEN, (0, 0, 0), (155, 0), (155, 900), 10)

    @staticmethod
    def draw_button(x, y, word):
        button_rect = pg.Rect(0, 0, 90, 40)
        button_rect.center = x, y
        pg.draw.rect(SCREEN, (0, 0, 0), button_rect, 1)
        button_word = GAME_FONT.render(word, True, (0, 0, 0))
        button_word_rect = button_word.get_rect(center=button_rect.center)
        SCREEN.blit(button_word, button_word_rect)
        return button_rect

    def draw_win_screen(self, status):
        if status:
            status_text = TITLE_FONT.render(f"You {status}!", True, (0, 0, 0))
            status_rect = status_text.get_rect()
            status_rect.center = (SCREEN_WIDTH / 2 + 75, SCREEN_HEIGHT / 2 - 30)
            SCREEN.blit(status_text, status_rect)

            self.draw_button(SCREEN_WIDTH / 2 + 75, SCREEN_HEIGHT / 2 + 75, "EXIT")

        if status == "LOSE":
            self.draw_choices(ANSWER, 200, 710)

    def draw_codebreaker_screen(self):
        self.draw_guess_grid(GUESS_GRID, 200, 65)
        self.draw_hint_grid(HINT_GRID, 55, 35)
        self.draw_choices(COLOR_CHOICES, 200, 710)
        self.draw_separators()
        self.draw_button(75, 710, "SUBMIT")

    def draw_solver_screen(self):
        self.draw_guess_grid(GUESS_GRID, 200, 65)
        self.draw_hint_grid(HINT_GRID, 55, 35)
        self.draw_separators()
        self.draw_button(SCREEN_WIDTH / 2 + 70, SCREEN_HEIGHT - 40, "EXIT")

    def draw_codemaker_screen(self):

        # draw explainer text
        instruction_text1 = SUB_TITLE_FONT.render("Choose a secret code", True, (0, 0, 0))
        instruction_rect1 = instruction_text1.get_rect()
        instruction_rect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.5)
        SCREEN.blit(instruction_text1, instruction_rect1)

        instruction_text2 = SUB_TITLE_FONT.render("For computer to guess", True, (0, 0, 0))
        instruction_rect2 = instruction_text2.get_rect()
        instruction_rect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.8)
        SCREEN.blit(instruction_text2, instruction_rect2)

        # draw secret answer
        self.draw_guess_grid([CODEMAKER_ANSWER], x=SCREEN_WIDTH / 3.75, y=SCREEN_HEIGHT / 2 - 30)

        # draw choices
        self.draw_choices(COLOR_CHOICES, x=SCREEN_WIDTH / 3.75, y=SCREEN_HEIGHT / 2 + 30)

        # draw submit button
        self.draw_button(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2 + 150, word="SUBMIT")

    @staticmethod
    def draw_title():
        # draw title
        title_word = TITLE_FONT.render("MASTERMIND", True, (0, 0, 0))
        title_rect = title_word.get_rect()
        title_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6)
        SCREEN.blit(title_word, title_rect)

        # draw subtitle
        subtitle_text = SUB_TITLE_FONT.render("Select game mode", True, (0, 0, 0))
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        SCREEN.blit(subtitle_text, subtitle_rect)

    @staticmethod
    def draw_codebreaker():
        # codebreaker
        codebreaker_text = SUB_TITLE_FONT.render("Codebreaker", True, (0, 0, 0))
        codebreaker_rect = codebreaker_text.get_rect()
        codebreaker_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        SCREEN.blit(codebreaker_text, codebreaker_rect)

        # codebreaker icon
        grid_x = SCREEN_WIDTH / 3.75
        grid_y = SCREEN_HEIGHT / 2 + 45
        for val in COLOR_CHOICES:
            pg.draw.circle(SCREEN, GUESS_COLOR_MAP[val], (grid_x, grid_y), GUESS_RADIUS)
            grid_x += 60

        # codebreaker selection rect
        window = pg.Rect(100, 340, 300, 110)
        pg.draw.rect(SCREEN, (0, 0, 0), window, width=1)
        return window

    @staticmethod
    def draw_codemaker():
        # codemaker text
        codemaker_text = SUB_TITLE_FONT.render("Codemaker", True, (0, 0, 0))
        codemaker_rect = codemaker_text.get_rect()
        codemaker_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.4)
        SCREEN.blit(codemaker_text, codemaker_rect)

        # codemaker icon
        grid_x = SCREEN_WIDTH / 2 - 32
        grid_y = SCREEN_HEIGHT / 1.3
        for i in range(5):
            if i in (0, 1):
                SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 15, grid_y - 15))
                pg.draw.circle(SCREEN, HINT_COLOR_MAP["B"], (grid_x, grid_y), HINT_RADIUS)
                grid_x += 60
            elif i == 2:
                SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 90 - 15, grid_y + 30 - 15))
                pg.draw.circle(SCREEN, HINT_COLOR_MAP["W"], (grid_x - 90, grid_y + 30), HINT_RADIUS)
                grid_x = SCREEN_WIDTH / 2 - 30
            elif i in (3, 4):
                SCREEN.blit(pg.transform.scale(HOLE_BACKGROUND, (30, 30)), (grid_x - 15, grid_y + 60 - 15))
                grid_x += 60

        # codebreaker selection rect
        window = pg.Rect(100, 500, 300, 160)
        pg.draw.rect(SCREEN, (0, 0, 0), window, width=1)

        return window

    def draw_start_screen(self):
        self.draw_title()
        self.draw_codebreaker()
        self.draw_codemaker()

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
                hints.append("B")
                ans_temp[i] = ""
                guess_temp[i] = ""

        # second pass for white pegs
        for guess_elem, ans_elem in zip(guess_temp, ans_temp):
            if guess_elem in ans_temp and guess_elem:
                hints.append("W")
                ans_temp[ans_temp.index(guess_elem)] = ""

        return hints

    def play(self):
        game_status = "start"
        win_status = None
        current_time = pg.time.get_ticks()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()

                    if game_status == "start":
                        breaker_rect = self.draw_codebreaker()
                        maker_rect = self.draw_codemaker()
                        if breaker_rect.collidepoint(mouse_x, mouse_y):
                            game_status = "codebreaker"
                        elif maker_rect.collidepoint(mouse_x, mouse_y):
                            game_status = "codemaker"

                    elif game_status == "codebreaker":
                        # choosing which colors to play
                        choice_rects = self.draw_choices(COLOR_CHOICES, 200, 710)
                        for color, rect in zip(COLOR_CHOICES, choice_rects):
                            if rect.collidepoint(mouse_x, mouse_y):
                                if self.current_hole < 5:
                                    GUESS_GRID[6 - self.guesses_left][self.current_hole] = color
                                    self.current_hole += 1

                        # submitting a guess
                        submit_rect = self.draw_button(75, 710, "SUBMIT")
                        if submit_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_hole == 5:
                                guess = GUESS_GRID[6 - self.guesses_left]
                                hints = self.validate_guess(guess, ANSWER)
                                random.shuffle(hints)
                                HINT_GRID[6 - self.guesses_left] = hints
                                self.guesses_left -= 1
                                self.current_hole = 0

                                if guess == ANSWER:
                                    win_status = "WIN"

                                elif guess != ANSWER and self.guesses_left == 0:
                                    win_status = "LOSE"

                        if win_status in ("WIN", "LOSE"):
                            exit_rect = self.draw_button(SCREEN_WIDTH / 2 + 75, SCREEN_HEIGHT / 2 + 75, "EXIT")
                            if exit_rect.collidepoint(mouse_x, mouse_y):
                                sys.exit()

                    elif game_status == "codemaker":
                        # choosing which colors to play
                        choice_rects = self.draw_choices(COLOR_CHOICES, x=SCREEN_WIDTH / 3.75, y=SCREEN_HEIGHT / 2 + 45)
                        for color, rect in zip(COLOR_CHOICES, choice_rects):
                            if rect.collidepoint(mouse_x, mouse_y):
                                if self.current_hole < 5:
                                    CODEMAKER_ANSWER[self.current_hole] = color
                                    self.current_hole += 1

                        submit_rect = self.draw_button(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150, "SUBMIT")
                        if submit_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_hole == 5:
                                guesses, hints = MastermindSolver("".join(CODEMAKER_ANSWER)).solve()
                                self.current_hole = 0
                                for i, (guess, hint) in enumerate(zip(guesses, hints)):
                                    COMPUTER_GUESSES[i] = guess
                                    COMPUTER_HINTS[i] = hint
                                game_status = "solver_showcase"

                    elif game_status == "solver_showcase":
                        exit_rect = self.draw_button(SCREEN_WIDTH / 2 + 70, SCREEN_HEIGHT - 40, "EXIT")
                        if exit_rect.collidepoint(mouse_x, mouse_y):
                            sys.exit()

                if game_status == "codebreaker":
                    # changing color choices before submitting
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            if self.current_hole > 0:
                                self.current_hole -= 1
                                GUESS_GRID[6 - self.guesses_left][self.current_hole] = ""

                elif game_status == "codemaker":
                    # changing color choices before submitting
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            if self.current_hole > 0:
                                self.current_hole -= 1
                                CODEMAKER_ANSWER[self.current_hole] = ""

            SCREEN.blit(BACKGROUND, (0, 0))
            if game_status == "start":
                self.draw_start_screen()
            elif game_status == "codebreaker":
                self.draw_codebreaker_screen()
                self.draw_win_screen(win_status)
            elif game_status == "codemaker":
                self.draw_codemaker_screen()
            elif game_status == "solver_showcase":
                self.draw_solver_screen()
                if pg.time.get_ticks() - current_time > 3000:
                    i = self.current_hole
                    if COMPUTER_GUESSES[i]:
                        GUESS_GRID[i] = COMPUTER_GUESSES[i]
                        HINT_GRID[i] = COMPUTER_HINTS[i]
                        current_time = pg.time.get_ticks()
                        self.current_hole += 1

            pg.display.update()


Mastermind().play()
