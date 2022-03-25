import pickle
import itertools
import time

FileStore = open("stored_objects/score_dict.pickle", "rb")
score_dict = pickle.load(FileStore)
FileStore.close()

all_answers = itertools.product(*[["0", "1", "2", "3", "4"]] * 5)

# guess = ""
# score = 0
# possible_answers = [ans for ans in all_answers if score_dict[(guess, ans)] == score]

