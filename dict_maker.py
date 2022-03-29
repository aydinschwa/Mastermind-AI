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

    return "".join(hints)


def build_dict():
    # default dict avoids storing keys as tuple, saves lookup time
    score_dict = collections.defaultdict(dict)
    all_guesses = itertools.product(["R", "G", "B", "Y", "P"], repeat=5)

    for guess, answer in itertools.product(all_guesses, repeat=2):
        guess_str = "".join(guess)
        ans_str = "".join(answer)
        score_dict[guess_str][ans_str] = score_guess(guess, answer)

    FileStore = open("stored_objects/score_dict.pickle", "wb")
    pickle.dump(score_dict, FileStore)
    FileStore.close()


if __name__ == "__main__":
    build_dict()
