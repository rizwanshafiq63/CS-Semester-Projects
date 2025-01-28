import java.util.*;
//import java.util.random;

public class Rock_Paper_Scissors {
    public static void main(String[] args) {
        try ( //0 for Rock
        //1 for Paper
        //2 for Scissors
                Scanner sc = new Scanner(System.in)) {
            System.out.print("\nMake a choice:\n0 for Rock\n1 for Paper\n2 for Scissors\nEnter Your Choice: ");
            Integer userInput = sc.nextInt();
            
            Random random = new Random();
            Integer compInput = random.nextInt(3);
            
            switch (compInput) {
                case 0 -> System.out.println("Computer's Choice: Rock");
                case 1 -> System.out.println("Computer's Choice: Paper");
                case 2 -> System.out.println("Computer's Choice: Scissors");
                default -> {
                }
            }
            
            if((userInput==0 && compInput==2)||(userInput==1 && compInput==0)||(userInput==2 && compInput==0)){
                System.out.println("You Win!");
            } else{
                System.out.println("Computer Wins!");
            }
        }
    }
}
