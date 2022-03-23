import random


def validate_guess(guess, ans):
    # iterates through guess and answer lists element-by-element. Whenever it finds a match,
    # removes the value from a copy of answer so that nothing is double counted.
    hints = []
    ans_temp = ans.copy()
    for i, (guess_elem, ans_elem) in enumerate(zip(guess, ans_temp)):
        if guess_elem == ans_elem:
            hints.append("B")
            ans_temp[i] = "USED"
    for guess_elem, ans_elem in zip(guess, ans_temp):
        if guess_elem in ans_temp:
            hints.append("W")
            ans_temp[ans_temp.index(guess_elem)] = "USED"

    random.shuffle(hints)

    return hints


# main loop
# almost no error handling at all, but this is just to demonstrate
while True:
    answer = [random.randint(0, 4) for _ in range(5)]
    answer_str = "".join([str(num) for num in answer])
    guesses_remaining = 6
    while guesses_remaining > 0:
        while True:
            guess_str = input("Guess a 5 number combination using 0 - 4: ")
            guess = [int(num) for num in guess_str]
            if len(guess) != 5:
                print("Guess must be 5 numbers exactly")
                continue
            else:
                break

        hints = "".join(validate_guess(guess, answer))
        if hints == "BBBBB":
            print(hints, "\n")
            print(f"You win! Well done! Answer was {answer_str}")
            while True:
                restart_q = input("Do you want to play again? (Y \\ N): ")
                if restart_q == "Y":
                    print("Restarting game...")
                    break
                elif restart_q == "N":
                    exit()
        else:
            guesses_remaining -= 1
            if guesses_remaining == 0:
                print(hints, "\n")
                print(f"You lose! Correct answer: {answer_str}")
                while True:
                    restart_q = input("Do you want to play again? (Y \\ N): ")
                    if restart_q == "Y":
                        print("Restarting game...")
                        break
                    elif restart_q == "N":
                        exit()
            else:
                print(hints, "\n")
                print(f"Guesses Remaining: {guesses_remaining}")