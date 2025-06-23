class Student {

  String name;
  String studentID;
  String department;

  public void displayInfo() {
    System.out.println("Student ID: " + studentID + "\nName: " + name + "\nDepartment: " + department);
  }
}

public class LabTask_01 {
  public static void main(String[] args) {

    Student student1 = new Student();
    student1.name = "Rizwan Shafiq";
    student1.studentID = "SP24-BCS-069";
    student1.department = "Computer Science";

    student1.displayInfo();
  }
}

