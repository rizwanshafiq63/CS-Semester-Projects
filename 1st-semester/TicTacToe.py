
def Game_Board(xState, yState):
    ### Arrays      
    one = ('X' if xState[0] else ('O' if yState[0] else 1))
    two = ('X' if xState[1] else ('O' if yState[1] else 2))
    three = ('X' if xState[2] else ('O' if yState[2] else 3))
    four = ('X' if xState[3] else ('O' if yState[3] else 4))
    five = ('X' if xState[4] else ('O' if yState[4] else 5))
    six = ('X' if xState[5] else ('O' if yState[5] else 6))
    seven = ('X' if xState[6] else ('O' if yState[6] else 7))
    eight = ('X' if xState[7] else ('O' if yState[7] else 8))
    nine = ('X' if xState[8] else ('O' if yState[8] else 9))
    ten = ('X' if xState[9] else ('O' if yState[9] else 10))
    eleven = ('X' if xState[10] else ('O' if yState[10] else 11))
    twelve = ('X' if xState[11] else ('O' if yState[11] else 12))
    thirteen = ('X' if xState[12] else ('O' if yState[12] else 13))
    fourteen = ('X' if xState[13] else ('O' if yState[13] else 14))
    fifteen = ('X' if xState[14] else ('O' if yState[14] else 15))
    sixteen = ('X' if xState[15] else ('O' if yState[15] else 16))
    seventeen = ('X' if xState[16] else ('O' if yState[16] else 17))
    eighteen = ('X' if xState[17] else ('O' if yState[17] else 18))
    nineteen = ('X' if xState[18] else ('O' if yState[18] else 19))
    twenty = ('X' if xState[19] else ('O' if yState[19] else 20))
    twentyone = ('X' if xState[20] else ('O' if yState[20] else 21))
    twentytwo = ('X' if xState[21] else ('O' if yState[21] else 22))
    twentythree = ('X' if xState[22] else ('O' if yState[22] else 23))
    twentyfour = ('X' if xState[23] else ('O' if yState[23] else 24))
    twentyfive = ('X' if xState[24] else ('O' if yState[24] else 25))
    ### Game Board Layout
    print(f"\n {one:2} | {two:2} | {three:2} | {four:2} | {five:2} ")
    print(f"----|----|----|----|----")
    print(f" {six:2} | {seven:2} | {eight:2} | {nine:2} | {ten:2} ")
    print(f"----|----|----|----|----")
    print(f" {eleven:2} | {twelve:2} | {thirteen:2} | {fourteen:2} | {fifteen:2} ")
    print(f"----|----|----|----|----")
    print(f" {sixteen:2} | {seventeen:2} | {eighteen:2} | {nineteen:2} | {twenty:2} ")
    print(f"----|----|----|----|----")
    print(f" {twentyone:2} | {twentytwo:2} | {twentythree:2} | {twentyfour:2} | {twentyfive:2} ")

def is_position_occupied(xState, yState, position):
    return xState[position] == 1 or yState[position] == 1

def if_board_finished(xState, yState):
    for i in range(len(xState)):
        if xState[i] == 0 and yState[i] == 0:
            return False
    return True

def Check_Winner(xState, yState):
    def sum_of_five(a, b, c, d, e):
        result = a + b + c + d + e
        return  result
    possibilities_in_rows = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
    possibilities_in_columns = [[0, 5, 10, 15, 20], [1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23], [4, 9, 14, 19, 24]]
    possibilities_in_diagonals = [[0, 6, 12, 18, 24], [4, 8, 12, 16, 20]]
    winner_possibilities = possibilities_in_rows + possibilities_in_columns + possibilities_in_diagonals
    for win in winner_possibilities:
        if(sum_of_five(xState[win[0]], xState[win[1]], xState[win[2]], xState[win[3]], xState[win[4]]) == 5):
            return 1
        if(sum_of_five(yState[win[0]], yState[win[1]], yState[win[2]], yState[win[3]], yState[win[4]]) == 5):
            return 0
    return -1

def Main_Game():
    player_1 = input("\nEnter name for the First Player [X]: ")
    player_2 = input("Enter name for the Second Player [O]: ")
    xState = [0] * 25 # xState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    yState = [0] * 25 # explained above
    turn = 1 # I kept 1 for 'X' and 0 for 'O'
    while True:
        Game_Board(xState, yState)
        if turn == 1:
            print(f"\n{player_1}'s Chance [X]")
            while True:
                user_input = int(input("Enter a value between 1 to 25: "))
                box_value = user_input - 1
                if (0 <= box_value < 25) and not is_position_occupied(xState, yState, box_value):
                    xState[box_value] = 1
                    break
                else:
                    print("\nPosition already occupied or invalid input. Please choose a different position.")
        else:
            print(f"\n{player_2}'s Chance [O]")
            while True:
                user_input = int(input("Enter a value between 1 to 25: "))
                box_value = user_input - 1
                if (0 <= box_value < 25) and not is_position_occupied(xState, yState, box_value):
                    yState[box_value] = 1
                    break
                else:
                    print("\nPosition already occupied or invalid input. Please choose a different position.")
        Winner = Check_Winner(xState, yState)
        if(Winner != -1):
            print("\nGame Finished!")
            if(Winner == 1):
                print(f"Congratulations! {player_1} has won the game")
            else:
                print(f"Congratulations! {player_2} has won the game")
            break
        if if_board_finished(xState, yState):
            print("\nGame Over! It's a draw! Nobody has won the game.")
            break
        turn = 1 - turn


### Game Start
print("Welcome to Tic Tac Toe Game")
x = int(input("Enter '1' to continue & '0' to quit: "))
while (x != 1) and (x != 0):
    x = int(input("Invalid input! Please enter '1' to continue & '0' to quit: "))
condition = x
if condition == 1:
    print("\nLet's Play the Game.")
### Looping the Game to play multiple times
while condition == 1:
    Main_Game()
    print("\nWanna Play more?")
    condition = int(input("Enter '1' to continue & '0' to quit: "))
    while (condition != 1) and (condition != 0):
        condition = int(input("Invalid input! Please enter '1' to continue & '0' to quit: "))
    if (condition == 1):
      print("\nWelcome Back to the Game!")
### If the player quits the game   
if x == 0:
    print("You quit without playing. Exiting the game.")
else:
    print("Thank You! For playing Tic Tac Toe. Exiting the game.")


