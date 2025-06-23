/* Implement the following hierarchy 
 <interface>Payble-|-> Employee -> SalariedEmployee
                   |-> Invoice
Payable:  double getPaymenyAmount(); 
Invoice:  private String partNumber;
          private String partDescription;
          private int quantity;
          private double pricePerItem;
Employee: private String firstName;
          private String lastName;
          private String socialSecurityNumber;
SalariedEmployee: private double weeklySalary;
In the runner, call the getPaymentAmount() method polymorphically. */

interface Payable {
  double getPaymentAmount();
}

class Invoice implements Payable {
  private String partNumber;
  private String partDescription;
  private int quantity;
  private double pricePerItem;

  public Invoice(String partNumber, String partDescription, int quantity, double pricePerItem) {
    this.partNumber = partNumber;
    this.partDescription = partDescription;
    this.quantity = quantity;
    this.pricePerItem = pricePerItem;
  }

  @Override
  public double getPaymentAmount() {
    return quantity * pricePerItem;
  }

  @Override
  public String toString() {
    return "Invoice: " + partDescription + " (" + partNumber + ")";
  }
}

abstract class Employee implements Payable {
  private String firstName;
  private String lastName;
  private String socialSecurityNumber;

  public Employee(String firstName, String lastName, String ssn) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.socialSecurityNumber = ssn;
  }

  @Override
  public abstract double getPaymentAmount();

  @Override
  public String toString() {
    return "Employee: " + firstName + " " + lastName + ", SSN: " + socialSecurityNumber;
  }
}

class SalariedEmployee extends Employee {
  private double weeklySalary;

  public SalariedEmployee(String firstName, String lastName, String ssn, double weeklySalary) {
    super(firstName, lastName, ssn);
    this.weeklySalary = weeklySalary;
  }

  @Override
  public double getPaymentAmount() {
    return weeklySalary;
  }
}

public class Lab9_Task_02 {
  public static void main(String[] args) {
    Payable[] payables = new Payable[2];

    payables[0] = new Invoice("1234", "Laptop Battery", 3, 2500.0);
    payables[1] = new SalariedEmployee("Ali", "Khan", "111-22-3333", 12000.0);

    for (Payable p : payables) {
      System.out.println(p);
      System.out.println("Payment Due: " + p.getPaymentAmount());
      System.out.println("-----------------------------");
    }
  }
}

