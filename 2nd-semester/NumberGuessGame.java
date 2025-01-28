import java.util.Scanner;

public class NumberGuessGame {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Hi there, Let's play a game. Are You Ready?");
        System.out.print("Enter '1' to continue & '0' to quit: ");
        int x = sc.nextInt(), gameCount = 0;
        while (x != 0 && x != 1) {
            System.out.print("\nInvalid Input! Please enter '1' to continue & '0' to quit: ");
            x = sc.nextInt();
        }
        while (x == 1) {
            System.out.println("\nWelcome to the Number Guessing Game.");
            System.out.println("Try to guess the number that I have chosen between 1 and 100.");
            int myNumber = (int)(Math.random()*100), Low = 0, High = 100, attemptsMade = 0, userNumber = 101;
            do {
                if (attemptsMade == 0) {
                    System.out.print("\nGuess my number (1 - 100): ");
                    userNumber = sc.nextInt();
                } else {
                    System.out.print("\nGuess my number again (1 - 100): ");
                    userNumber = sc.nextInt();
                }
                attemptsMade++;
                while (userNumber<0 || userNumber>100) {
                    System.out.print("\nInvalid Input! The number lies between 0 and 100.");
                    System.out.println("Guess my number again (1 - 100): ");
                    userNumber = sc.nextInt();
                    System.out.println("Number of attempts made: " +attemptsMade);
                }
                if (userNumber > myNumber) {
                    if (userNumber < High) {
                        High = userNumber;
                    }
                    System.out.println("Too High! Number is between " +Low+" and " +High+" Think Harder!");
                } else{
                    if (userNumber > Low) {
                        Low = userNumber;
                    }
                    System.out.println("Too Low! Number is between " +Low+" and " +High+" Think Harder!");
                }
                System.out.println("Number of attempts made: " +attemptsMade);
            } while (userNumber != myNumber);
            if (userNumber == myNumber) {
                System.out.println("\nWOOHOO .. You Guessed the Correct Number!!!");
                System.out.println("My number was: " +myNumber);
                System.out.println("Number of attempts made:" +attemptsMade);
            } else {
                System.out.println("Sorry! There seems to be an error");
            }
            gameCount++;
            System.out.println("Wanna Play Again?");
            System.out.print("Enter '1' to continue & '0' to quit: ");
            x = sc.nextInt();  
            while (x != 0 && x != 1) {
                System.out.print("\nInvalid Input! Please enter '1' to continue & '0' to quit: ");
                x = sc.nextInt();
            }  
        }
        switch (gameCount) {
            case 0:
            System.out.println("You have quit the game without playing. Goodbye!");
                break;
            case 1:
                System.out.println("You have quit the game after playing it " +gameCount+" time. Hope You Had Fun!");
                break;       
            default:
                System.out.println("You have quit the game after playing it "+gameCount+" times. Hope You Had Fun!");
                break;
        }
    }
}
