import pickle
import itertools
import collections
from dict_maker import score_guess


# this is a one-time use class at the moment since internal variables get modified.
# copying them was too time and memory intensive, think it's better to just load
# from stored_objects every time
class MastermindSolver:
    def __init__(self, answer):
        self.all_answers = itertools.product(["R", "G", "B", "Y", "P"], repeat=5)
        self.all_answers = {"".join(answer) for answer in self.all_answers}
        self.guesses_left = 6
        self.guess_history = []
        self.answer = answer

        FileStore = open("stored_objects/score_dict.pickle", "rb")
        self.score_dict = pickle.load(FileStore)
        FileStore.close()

    def make_guess(self):
        guesses_to_try = []
        for guess, scores_by_answer_dict in self.score_dict.items():
            # reduce possible_score_dict to only include possible answers
            scores_by_answer_dict = {answer: score for answer, score in scores_by_answer_dict.items()
                                     if answer in self.all_answers}
            self.score_dict[guess] = scores_by_answer_dict

            # find how often a score appears in scores_by_answer_dict, get max
            possibilities_per_score = collections.Counter(scores_by_answer_dict.values())
            worst_case = max(possibilities_per_score.values())

            # prefer possible guesses over impossible ones
            impossible_guess = guess not in self.all_answers

            guesses_to_try.append((worst_case, impossible_guess, guess))

        return min(guesses_to_try)[-1]

    def solve(self):
        while self.guesses_left > 0:
            if self.guesses_left == 6:
                guess = "RRGGB"
            else:
                guess = self.make_guess()

            self.guess_history.append(guess)

            # reduce amount of possible answers by checking answer against guess and score
            score = score_guess(guess, self.answer)
            self.all_answers = {answer for answer in self.all_answers
                                if self.score_dict[guess][answer] == score}

            self.guesses_left -= 1
            if guess == self.answer:
                return self.guess_history