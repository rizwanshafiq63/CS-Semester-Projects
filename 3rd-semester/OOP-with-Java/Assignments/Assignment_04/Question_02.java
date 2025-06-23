/** Q2. Create an ATM System with Account as the Serializable class. Write ten objects of Account in a ﬁle. Now write func ons for withdraw, deposit, transfer and balance inquiry.
a. Each func on should ask for the account number on which speciﬁc opera on
should be made.
b. All changes in Account object should be eﬀec vely represented in the ﬁle. **/

import java.io.*;
import java.util.*;
import java.io.Serializable;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

class Account implements Serializable {
  private int accountNumber;
  private String holderName;
  private double balance;

  public Account(int accountNumber, String holderName, double balance) {
    this.accountNumber = accountNumber;
    this.holderName = holderName;
    this.balance = balance;
  }

  public int getAccountNumber() {
    return accountNumber;
  }

  public String getHolderName() {
    return holderName;
  }

  public double getBalance() {
    return balance;
  }

  public boolean deposit(double amount) {
    if (amount > 0) {
      balance += amount;
      return true;
    } else {
      System.out.println("Deposit amount must be positive.");
      return false;
    }
  }

  public boolean withdraw(double amount) {
    if (amount <= 0) {
      System.out.println("Withdrawal amount must be positive.");
      return false;
    }
    if (balance >= amount) {
      balance -= amount;
      return true;
    } else {
      System.out.println("Insufficient balance.");
      return false;
    }
  }

  public void display() {
    System.out.println("Account #: " + accountNumber);
    System.out.println("Name: " + holderName);
    System.out.println("Balance: $" + balance);
    System.out.println("---------------------------");
  }
}

// ATM System
public class Question_02 {
  static final String FILE_NAME = "accounts.ser";

  public static List<Account> loadAccounts() {
    List<Account> accounts = new ArrayList<>();
    try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(FILE_NAME))) {
      while (true) {
        try {
          Account acc = (Account) ois.readObject();
          accounts.add(acc);
        } catch (EOFException e) {
          break;
        }
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
    return accounts;
  }

  public static void saveAccounts(List<Account> accounts) {
    try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(FILE_NAME))) {
      for (Account acc : accounts) {
        oos.writeObject(acc);
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static Account findAccount(List<Account> accounts, int accNo) {
    for (Account acc : accounts) {
      if (acc.getAccountNumber() == accNo)
      return acc;
    }
    return null;
  }

  public static void withdraw() {
    Scanner sc = new Scanner(System.in);
    List<Account> accounts = loadAccounts();

    System.out.print("Enter Account Number: ");
    int accNo = sc.nextInt();

    Account acc = findAccount(accounts, accNo);
    if (acc != null) {
      System.out.print("Enter amount to withdraw: ");
      double amt = sc.nextDouble();
      if (acc.withdraw(amt)) {
        System.out.println("Withdrawal successful.");
      }
    } else {
      System.out.println("Account not found.");
    }

    saveAccounts(accounts);
  }

  public static void deposit() {
    Scanner sc = new Scanner(System.in);
    List<Account> accounts = loadAccounts();

    System.out.print("Enter Account Number: ");
    int accNo = sc.nextInt();

    Account acc = findAccount(accounts, accNo);
    if (acc != null) {
      System.out.print("Enter amount to deposit: ");
      double amt = sc.nextDouble();
      if (acc.deposit(amt)) {
        System.out.println("Deposit successful.");
      }
    } else {
      System.out.println("Account not found.");
    }

    saveAccounts(accounts);
  }

  public static void balanceInquiry() {
    Scanner sc = new Scanner(System.in);
    List<Account> accounts = loadAccounts();

    System.out.print("Enter Account Number: ");
    int accNo = sc.nextInt();

    Account acc = findAccount(accounts, accNo);
    if (acc != null) {
      acc.display();
    } else {
      System.out.println("Account not found.");
    }

  }

  public static void transfer() {
    Scanner sc = new Scanner(System.in);
    List<Account> accounts = loadAccounts();

    System.out.print("Enter Source Account Number: ");
    int fromAccNo = sc.nextInt();

    System.out.print("Enter Destination Account Number: ");
    int toAccNo = sc.nextInt();

    System.out.print("Enter amount to transfer: ");
    double amt = sc.nextDouble();

    Account fromAcc = findAccount(accounts, fromAccNo);
    Account toAcc = findAccount(accounts, toAccNo);

    if (fromAcc != null && toAcc != null) {
      if (fromAcc.withdraw(amt) && toAcc.deposit(amt)) {
        System.out.println("Transfer successful.");
      } else {
        System.out.println("Error in Transfer.");
      }
    } else {
      System.out.println("One or both accounts not found.");
    }

    saveAccounts(accounts);
  }

  public static void main(String[] args) {
    // Initialize accounts only once if file doesn't exist
    File file = new File(FILE_NAME);
    if (!file.exists()) {
      List<Account> initialAccounts = new ArrayList<>();
      for (int i = 0; i < 10; i++) {
        initialAccounts.add(new Account(1000 + i, "User" + (i + 1), 1000.0));
      }
      saveAccounts(initialAccounts);
      System.out.println("Initialized 10 default accounts.");
    }

    try (Scanner sc = new Scanner(System.in)) {
      while (true) {
        System.out.println("\n--- ATM MENU ---");
        System.out.println("1. Withdraw");
        System.out.println("2. Deposit");
        System.out.println("3. Transfer");
        System.out.println("4. Balance Inquiry");
        System.out.println("5. Exit");
        System.out.print("Choose: ");
        int choice = sc.nextInt();

        switch (choice) {
          case 1: withdraw(); break;
          case 2: deposit(); break;
          case 3: transfer(); break;
          case 4: balanceInquiry(); break;
          case 5: System.exit(0);
          default: System.out.println("Invalid choice.");
        }
      }
    }
  }
}

