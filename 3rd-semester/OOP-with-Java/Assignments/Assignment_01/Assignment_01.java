/* Rewrite the code using object-oriented approach. */

import java.util.Scanner;

class Student {
  private String name;
  private int marks;

  public Student() {
    this.name = null;
    this.marks = 0;
  }
  public Student(String name, int marks) {
    this.name = name;
    this.marks = marks;
  }

  public String getName() {
    return name;
  }

  public String getGrade() {
    if (marks >= 90) {
      return "A";
    } else if (marks >= 80) {
      return "B";
    } else if (marks >= 70) {
      return "C";
    } else if (marks >= 60) {
      return "D";
    } else {
      return "F";
    }
  }

  public void display() {
    System.out.println("Name: " + name + " | Grade: " + getGrade());
    System.out.println("**************************");
  }
}

public class StudentGradeCalculator {
  public static void main(String[] args) {
    Scanner input = new Scanner(System.in);

    // Input for Student 1
    System.out.println("Enter details for Student 1:");
    System.out.print("Enter Name: ");
    String name1 = input.next();
    System.out.print("Enter Marks: ");
    int marks1 = input.nextInt();

    // Input for Student 2
    System.out.println("Enter details for Student 2:");
    System.out.print("Enter Name: ");
    String name2 = input.next();
    System.out.print("Enter Marks: ");
    int marks2 = input.nextInt();

    // Creating student objects
    Student student1 = new Student(name1, marks1);
    Student student2 = new Student(name2, marks2);

    // Displaying results
    student1.display();
    student2.display();

    input.close();
  }
}

