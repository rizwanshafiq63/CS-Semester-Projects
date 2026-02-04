# Generate a random number between 1 and 9 (including 1 and 9). 
# Ask the user to guess the number, then tell them whether they guessed too low, too high, or exactly right. 
# (Hint: remember to use the user input lessons from the very first exercise)
# Extras:
# Keep the game going until the user types “exit”
# Keep track of how many guesses the user has taken, and when the game ends, print this out.

import random # Awroken
MINIMUM = 1
MAXIMUM = 9
NUMBER = random.randint(MINIMUM, MAXIMUM) 
GUESS = None
TRY = 0 
RUNNING = True
print("=== Number Guess Game ===") 
while RUNNING:
    GUESS = input("What is your Guess? ")
    if GUESS.lower() == "exit":
        print("Better luck next time.")
        print("Exiting...")
        RUNNING = False
    elif int(GUESS) < NUMBER:
        print("Wrong, too low.") 
    elif int(GUESS) > NUMBER:
        print("Wrong, too high.")
    elif int(GUESS) == NUMBER:
        print("Yes, that's the one, ", NUMBER)
        if TRY < 2:
            print("Impressive, only %s tries." % str(TRY)) 
        elif TRY > 2 and TRY < 10:
            print("Pretty good, %s tries." % str(TRY))
        else:
            print("Bad, %s tries." % str(TRY))
        RUNNING = False
    TRY += 1
