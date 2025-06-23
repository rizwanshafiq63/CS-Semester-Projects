/*  Create an Encapsulated class Account class with balance as data member. Create two constructors and methods to withdraw and deposit balance. In the runner create two accounts. The second account should be created with the same balance as first account. (Hint: use get function) */

class Account {
  private double balance;

  // Constructors
  public Account(){
    balance = 0.0;
  }
  public Account(double balance) {
    if (balance < 0) {
      throw new IllegalArgumentException("Balance cannot be negative.");
    }
    this.balance = balance;
  }

  // Copy Constructor
  public Account(Account anotherAccount) {
    this.balance = anotherAccount.getBalance();
  }

  // Deposit Method
  public void deposit(double amount) {
    if (amount > 0) {
      balance += amount;
      System.out.println("Amount Deposited: " + amount);
    } else {
      throw new IllegalArgumentException("Deposit amount must be positive.");
    }
  }

  // Withdraw Method
  public void withdraw(double amount) {
    if (amount > 0 && amount <= balance) {
      balance -= amount;
      System.out.println("Amount Withdraw: " + amount);
    } else {
      throw new IllegalArgumentException("Invalid withdrawal amount.");
    }
  }

  // Getter for balance
  public double getBalance() {
    return balance;
  }

  // Display Method
  public void displayBalance() {
    System.out.println("Current Balance: " + balance);
  }
}

public class Lab3_Task_02 {
  public static void main(String[] args) {
    try {
      Account account1 = new Account(1000);
      account1.displayBalance();

      account1.deposit(500);
      account1.withdraw(300);
      System.out.println("Updated Balance for Account 1:");
      account1.displayBalance();

      // Creating second account with the same balance as the first
      Account account2 = new Account(account1);
      System.out.println("Balance for Account 2:");
      account2.displayBalance();
    } catch (IllegalArgumentException e) {
      System.out.println("Error: " + e.getMessage());
    }
  }
}

