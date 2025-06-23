/* Declare a Interface, RegisterForExams that contains single method register, implements the interface in two different classes (a) Student (b) Employee. Write down a Test Application to test the overridden method. */

interface RegisterForExams {
  public void register();
}

class Employee implements RegisterForExams{
  private String name;
  private String date;
  private int salary;
  public Employee() {
    name = null;
    date = null;
    salary = 0;
  }
  public Employee(String name,String date,int salary) {
    this.name = name;
    this.date = date;
    this.salary = salary;
  }
  @Override
  public void register() {
    System.out.println("Employee is registered: " + "\n-> Name: " + name + "\n-> Salary: " + salary + "\n-> Date: " + date);
  }
}

class Student implements RegisterForExams{
  private String name;
  private int age;
  private double gpa;
  public Student() {
    name = null;
    age = 0;
    gpa = 0;
  }
  public Student(String name,int age,double gpa) {
    this.name = name;
    this.age = age;
    this.gpa = gpa;
  }
  @Override
  public void register() {
    System.out.println("Student is registered: \n-> Student Name: " + name + "\n-> Age: " +age + "\n-> GPA: " + gpa);
  }
}

// Runner
public class Activity01 {
  public static void main(String[] args) {
    Employee e = new Employee("Ahmed","11-02-2001",20000);
    Student s = new Student("Ali",22,3.5);
    e.register();
    s.register();
  } 
}


