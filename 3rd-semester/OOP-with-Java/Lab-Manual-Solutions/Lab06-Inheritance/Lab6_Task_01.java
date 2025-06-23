/*(The Person, Student, Employee, Faculty, and Staff classes)
Design a class named Person and its two subclasses named Student and Employee. Design two more classes; Faculty and Staff and extend them from Employee. The detail of classes is as under:
A person has a name, address, phone number, and email address.
A student has a status (String)
An employee has an office, salary, and date hired. Use the Date class to create an object for date hired.
A faculty member has office hours and a rank.
A staff member has a title.
Create display method in each class*/

// Base Class
class Person {
  protected String name, address, phone, email;

  public Person(String name, String address, String phone, String email) {
    this.name = name;
    this.address = address;
    this.phone = phone;
    this.email = email;
  }

  public void display() {
    System.out.println("Name: " + name + ", Address: " + address + ", Phone: " + phone + ", Email: " + email);
  }
}

// Subclass Student
class Student extends Person {
  protected String status;

  public Student(String name, String address, String phone, String email, String status) {
    super(name, address, phone, email);
    this.status = status;
  }

  @Override
  public void display() {
    super.display();
    System.out.println("Status: " + status);
  }
}

// Subclass Employee
class Employee extends Person {
  protected String office;
  protected double salary;
  protected String dateHired;

  public Employee(String name, String address, String phone, String email, String office, double salary, String dateHired) {
    super(name, address, phone, email);
    this.office = office;
    this.salary = checkSalary(salary);
    this.dateHired = dateHired;
  }

  private double checkSalary(double sal) {
    if (salary < 0) {
      return 0;
    } else {
      return sal;
    }
  }

  @Override
  public void display() {
    super.display();
    System.out.println("Office: " + office + ", Salary: " + salary + ", Date Hired: " + dateHired);
  }
}

// Faculty extends Employee
class Faculty extends Employee {
  protected String officeHours, rank;

  public Faculty(String name, String address, String phone, String email, String office, double salary, String dateHired, String officeHours, String rank) {
    super(name, address, phone, email, office, salary, dateHired);
    this.officeHours = officeHours;
    this.rank = rank;
  }

  @Override
  public void display() {
    super.display();
    System.out.println("Office Hours: " + officeHours + ", Rank: " + rank);
  }
}

// Staff extends Employee
class Staff extends Employee {
  protected String title;

  public Staff(String name, String address, String phone, String email, String office, double salary, String dateHired, String title) {
    super(name, address, phone, email, office, salary, dateHired);
    this.title = title;
  }

  @Override
  public void display() {
    super.display();
    System.out.println("Title: " + title);
  }
}

// Runner Class
public class Lab6_Task_01 {
  public static void main(String[] args) {
    Student s = new Student("Ali", "Islamabad", "12345", "ali@mail.com", "Sophomore");
    Faculty f = new Faculty("Ahmed", "Lahore", "67890", "ahmed@mail.com", "Office 101", 50000, "2020-01-01", "9AM-1PM", "Professor");
    Staff st = new Staff("Sara", "Karachi", "54321", "sara@mail.com", "Admin Block", 30000, "2021-06-15", "Manager");

    System.out.println("Student Info:");
    s.display();
    System.out.println("\nFaculty Info:");
    f.display();
    System.out.println("\nStaff Info:");
    st.display();
  }
}

