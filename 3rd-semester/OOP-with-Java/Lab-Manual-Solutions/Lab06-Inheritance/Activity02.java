/* This example demonstrates another scenario of inheritance. The super class can be extended by more than one class. */

class Employee {
  protected String name;
  protected String phone;
  protected String address;
  protected int allowance;
  public Employee(String name, String phone, String address, int allowance) {
    System.out.println("Constructor of Parent Employee");
    this.name = name; this.phone = phone; this.address = address;
    this.allowance = allowance;
  }
}

class Regular extends Employee {
  private int basicPay;
  public Regular(String name, String phone, String address, int allowance, int basicPay) {
    super(name, phone, address, allowance);
    System.out.println("Constructor of Child-01: Regular");
    this.basicPay = basicPay;
  }
  public void Display(){
    System.out.println("Name: " +name+ "Phone Number: " +phone+ "Address: " +address+ "Allowance: " +allowance+ "Basic Pay: " +basicPay);
  }
}

class Adhoc extends Employee {
  private int numberOfWorkingDays;
  private int wage;
  public Adhoc(String name, String phone, String address, int allowance, int numberOfWorkingDays, int wage) {
    super(name, phone, address, allowance);
    System.out.println("Constructor of Child-01: Adhoc");
    this.numberOfWorkingDays = numberOfWorkingDays;
    this.wage = wage;
  }
  public void Display() {
    System.out.println("Name: " +name+ "Phone Number: " +phone+ "Address: " +address+ "Allowance: " +allowance+ "Number Of Working Days: " +numberOfWorkingDays+ "Wage: " +wage);
  }
}

public class Activity02 {
  public static void main(String []args){
    Regular regularObj = new
    Regular("Ahmed","090078601","Islamabad",15000,60000);
    regularObj.Display();
    Adhoc adhocObj = new
    Adhoc("Ali","03333333333","Rawalpindi",500,23,1500);
    adhocObj.Display();
  }
}

