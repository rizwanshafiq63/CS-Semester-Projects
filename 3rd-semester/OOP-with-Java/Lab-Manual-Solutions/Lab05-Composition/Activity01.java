/* Composition is about expressing relationships between objects. Think about the example of a manager. A manager has the properties e.g Title and club dues. A manager has an employment record. And a manager has an educational record. The phrase "has a" implies a relationship where the manager owns, or at minimum, uses, another object. It is this "has a" relationship which is the basis for composition. This example can be programmed as follows: */

class studentRecord {
  private String degree;
  public studentRecord() {
  }
  public void setDegree(String deg) {
    degree = deg;
  }
  public String getDegree() {
    return degree;
  }
}
class employeeRecord {
  private int emp_id;
  private double salary;
  public employeeRecord() {
  }
  public void setEmp_id(int id) {
    emp_id = id;
  }
  public int getEmp_id() {
    return emp_id;
  }
  public void setSalary(int sal) {
    salary = sal;
  }
  public double getSalary() {
    return salary;
  }
}
class Manager {
  private String title;
  private double dues;
  private employeeRecord emp;
  private studentRecord stu;
  public Manager(String t, double d,
    employeeRecord e, studentRecord s) {
    title = t;
    dues = d;
    emp = e;
    stu = s;
  }
  public studentRecord getStu() {
    return stu;
  }
  public employeeRecord getEmp() {
    return emp;
  }
  public void display() {
    System.out.println("Title is : " + title);
    System.out.println("Dues are : " + dues);
    System.out.println("Emplyoyee record is as under:");
    System.out.println("EmployeeId is : " +emp.getEmp_id());
    System.out.println("EmployeeId is : " +emp.getSalary());
    System.out.println("Student record is as under: ");
    System.out.println("Degree is : " +stu.getDegree());
  }
}
public class Activity01 {
  public static void main(String args[]) {
    studentRecord student1 = new studentRecord();
    employeeRecord employee1 = new employeeRecord();
    Manager m1 = new Manager("financeManager", 5000, employee1, student1);
    m1.getStu().setDegree("MBA");
    m1.getEmp().setEmp_id(1);
    m1.getEmp().setSalary(25000);
    m1.display();
  }
}
