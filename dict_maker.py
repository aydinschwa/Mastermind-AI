import collections
import itertools
import pickle


def score_guess(guess, ans):
    # iterates through guess and answer lists element-by-element. Whenever it finds a match,
    # removes the value from a copy of answer so that nothing is double counted.
    hints = []
    ans_no_match = []
    guess_no_match = []
    for guess_elem, ans_elem in zip(guess, ans):
        if guess_elem == ans_elem:
            hints.append("B")
        else:
            guess_no_match.append(guess_elem)
            ans_no_match.append(ans_elem)

    for guess_elem in guess_no_match:
        if guess_elem in ans_no_match:
            hints.append("W")
            ans_no_match.remove(guess_elem)

    return hints


# default dict avoids storing keys as tuple, saves lookup time
score_dict = collections.defaultdict(dict)
all_guesses = itertools.product(["0", "1", "2", "3", "4"], repeat=5)

for i, (guess, answer) in enumerate(itertools.product(all_guesses, repeat=2)):
    guess_str = "".join(guess)
    ans_str = "".join(answer)
    score_str = "".join(score_guess(guess, answer))
    score_dict[guess_str][ans_str] = score_str

FileStore = open("stored_objects/score_dict.pickle", "wb")
pickle.dump(score_dict, FileStore)
FileStore.close()