import random
    ### I Kept:
    # 1 for Rock
    # 2 for Paper
    # 3 for Scissors

### Defined two functions to display each player's choice
def player_1_choice_display(player1Input, player1):
    if(player1Input==1):
        player1choice = f"\n{player1}'s Choice: Rock"
    elif(player1Input==2):
        player1choice = f"\n{player1}'s Choice: Paper"
    elif(player1Input==3):
        player1choice = f"\n{player1}'s Choice: Scissors"
    return print(player1choice)
      
def player_2_choice_display(player2Input, player2):
    if(player2Input==1):       
        player2choice = f"{player2}'s Choice: Rock"
    elif(player2Input==2):
        player2choice = f"{player2}'s Choice: Paper"
    elif(player2Input==3):     
        player2choice = f"{player2}'s Choice: Scissors"
    return print(player2choice)

### Defined a function here to display each turn's winner
def turnWinner(player1Input, player2Input, player1, player2):
    ### Defined a nested function to compare the choices of players
    ### It shows which choice is beating the other
    def comparision(a, b):
        if(a==1 and b==3):
            comp = "\nRock beats Scissors"
        elif(a==2 and b==1):
            comp = "\nPaper beats Rock"
        elif(a==3 and b==2):
            comp = "\nScissors beat Paper "
        return print(comp)
    if((player1Input==1 and player2Input==3)or(player1Input==2 and player2Input==1)or(player1Input==3 and player2Input==2)):  
        comparision(player1Input, player2Input)
        print(f"{player1} Wins the turn!")
        result = 1
    elif((player1Input==1 and player2Input==1)or(player1Input==2 and player2Input==2)or(player1Input==3 and player2Input==3)):
        print("\nIt's a DRAW!\nBoth players made the same choice.")
        result = 0
    else:
        comparision(player2Input, player1Input)
        print(f"{player2} Wins the turn!")
        result = 2
    ### Kept 1 for player_1, 2 for Player_2 and 0 for draw
    return result

### Defined a function to announce the final winner
def game_winner(player1Wins, player2Wins, playerMode, player1, player2):
    if(player1Wins==player2Wins):
        finalwinner = "\nIt's a DRAW! Nobody wins the game."
    elif(playerMode==1 and player1Wins!=player2Wins):
        if(player1Wins>player2Wins):
           finalwinner = "\nCongratulations! You beat the computer."
        else:
            finalwinner = "\nYou've Lost the Game. Try Again."
    elif(playerMode==2 and player1Wins!=player2Wins):
        if(player1Wins>player2Wins):
            finalwinner = f"\nCongratulations {player1}! You won the game."
        else:
            finalwinner = f"\nCongratulations {player2}! You won the game."
    return print(finalwinner)

### Defined a main function which consists of the actual game
def main():
    ### Asked for player mode from the user
    playerMode = input("\nEnter 1 for single player mode and 2 for two players mode: ")
    while(playerMode!='1' and playerMode!='2'):
        playerMode = input("\nInvalid Input! Please enter 1 for single player mode and 2 for two players mode: ")
    playerMode = int(playerMode)
    ### Assigned some variables here for further use
    turn = 1
    player1Wins = 0
    player2Wins = 0
    drawcount = 0
    print("\nBest of five will win the final game.")
    while (turn<6):
        print("\nTURN: ", turn)
        if(playerMode==2 and turn==1): ### Assigning player names
            player1 = input("Enter name for player 1: ")
            player2 = input("Enter name for player 2: ")
        elif(playerMode==1 and turn==1):
            player1 = input("Enter your name: ")
            player2 = "Computer"
        elif(turn>1): ### Printing a score board
            print(f"{player1}'s Win Count:", player1Wins,f"\t{player2}'s Win Count:", player2Wins,f"\tNo. of Draws:", drawcount)
        ### Taking input from player_1
        player1Input = input(f"\n{player1}'s Chance\n1 for Rock\n2 for Paper\n3 for Scissors\nEnter Your Choice: ")
        while(player1Input!='1' and player1Input!='2' and player1Input!='3'):
            player1Input = input("\nInvalid Input! Please make a valid choice:\n1 for Rock\n2 for Paper\n3 for Scissors\nEnter Your Choice: ")
        player1Input = int(player1Input)
        ### Taking input from player_2
        if(playerMode==1):
            player2Input = random.randint(1, 4) ### Input by computer
        elif(playerMode==2):
            player2Input = input(f"\n{player2}'s Chance\n1 for Rock\n2 for Paper\n3 for Scissors\nEnter Your Choice: ") ### Input by player_2
            while(player2Input!='1' and player2Input!='2' and player2Input!='3'):
                player2Input = input("\nInvalid Input! Please make a valid choice:\n1 for Rock\n2 for Paper\n3 for Scissors\nEnter Your Choice: ")
            player2Input = int(player2Input)
        
        player_1_choice_display(player1Input, player1) ### Printing each players choice
        player_2_choice_display(player2Input, player2)
        ### Checking for winner of turn
        winner = turnWinner(player1Input, player2Input, player1, player2) 
        if(winner==1): ### Changing scores here
            player1Wins += 1
        elif(winner==2):
            player2Wins += 1
        else:
            drawcount += 1
        turn += 1 ### Incrementing number of turns
    ### To be executed after the loop ends
    ### Announcing the results and the final winner
    print(f"\nScore Board:\n{player1}'s Win Count:", player1Wins,f"\t{player2}'s Win Count:", player2Wins,f"\tNo. of Draws:", drawcount)
    game_winner(player1Wins, player2Wins, playerMode, player1, player2)
    

if __name__ == '__main__':
    ### Game Start
    print("\n\t\t\t\t\tWelcome to Rock Paper Scissors Game") ### Welcome Quote
    x = input("Enter '1' to continue & '0' to quit: ")
    while (x != '1') and (x != '0'):
        x = input("Invalid input! Please enter '1' to continue & '0' to quit: ")
    condition = x
    if condition == '1':
        print("\n\t\t\t\t\t\tLet's Play the Game.")
    ### Looping the Game to play multiple times
    while condition == '1':
        main()
        ### Asking whether tonplay again or to exit
        condition = input("\nWanna Play more?\nEnter '1' to continue & '0' to quit: ")
        while (condition != '1') and (condition != '0'):
            condition = input("Invalid input! Please enter '1' to continue & '0' to quit: ")
        if (condition == '1'):
          print("\n\t\t\t\t\t    Welcome Back to the Game!") #if chooses to play again
    ### If the player quits the game   
    if x == '0':
        print("You quit without playing. Exiting the game.")
    else:
        print("Thank You! For playing Rock Paper Scissors. Exiting the game.")
### ENDING OF CODE