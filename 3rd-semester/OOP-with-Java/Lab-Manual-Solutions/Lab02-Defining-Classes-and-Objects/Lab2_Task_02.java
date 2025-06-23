import java.util.Scanner;

class Account {
  //Date Member
  private double balance;

  //Constructors
  public Account(){
    balance = 0.0;
  }
  public Account(double myBalance){
    if (myBalance >= 0) {
      balance = myBalance;
    } else {
      System.out.println("Invalid initial balance! Setting balance to 0.0.");
      balance = 0.0;  // Default value for invalid balance
    }
  }

  //Methods for deposit and withdraw
  public void deposit(double amount){
    if (amount > 0) {
      balance += amount;
      System.out.println("Amount Deposited: " + amount);
    } else {
      System.out.println("The amount entered must be positive.");
    }
  }
  public void withdraw(double amount){
    if (amount > 0 && amount <= balance) {
      balance -= amount;
      System.out.println("Amount Withdraw: " + amount);
    } else {
      System.out.println("Invalid Amount Entered!");
    }
  }

  //Getter
  public double getBalance(){
    return balance;
  }

}

public class Lab2_Task_02 {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);

    Account account1 = new Account();
    System.out.println("Initial Balance in account1: " + account1.getBalance());

    System.out.print("Enter the amount you want to depost: ");
    double depAmount = sc.nextDouble();
    account1.deposit(depAmount);
    System.out.println("Amount after deposit: " + account1.getBalance());

    System.out.print("Enter the amount you want to deposit: ");
    double wdamount = sc.nextDouble();
    account1.withdraw(wdamount);
    System.out.println("Amount After Withdraw: " + account1.getBalance());

    sc.close();
  }
}
