/* Create an Encapsulated class Student with following characteristics:
Data Members:
  String Name
  Int [] Result_array[5] // Result array contains the marks for 5 subjects
Methods:
  Student ( String, int[]) // argument Constructor
  Average () // it calculates and returns the average based on the marks in the array.
Runner:
  Create two objects of type Student and call the Average method.
  Compare the Average of both Students and display which student has higher average. Create a third student with name as object 1 and result array as object 2 */

class Student {
  private String name;
  private int[] resultArray = new int[5];

  // Constructors
  public Student() {
    this.name = "Unknown";
    for (int i = 0; i < 5; i++) {
      this.resultArray[i] = 0;
    }
  }
  public Student(String name, int[] resultArray) {
    if (name == null || name.trim().isEmpty()) {
      throw new IllegalArgumentException("Name cannot be empty.");
    }
    if (resultArray.length != this.resultArray.length) {
      throw new IllegalArgumentException("Invalid number of subjects.");
    }
    for (int i = 0; i < resultArray.length; i++) {
      if (resultArray[i] < 0 || resultArray[i] > 100) {
        throw new IllegalArgumentException("Marks should be between 0 and 100.");
      }
      this.resultArray[i] = resultArray[i];
    }
    this.name = name;
  }

  // Method to calculate average
  public double average() {
    int sum = 0;
    for (int i = 0; i < 5; i++) {
      sum += resultArray[i];
    }
    return (double) sum / 5;
  }

  // Getter for name
  public String getName() {
    return name;
  }

  // Getter for result array
  public int[] getResultArray() {
    int[] copy = new int[5];
    for (int i = 0; i < 5; i++) {
      copy[i] = resultArray[i];
    }
    return copy;
  }
}

public class Lab3_Task_03 {
  public static void main(String[] args) {
    int[] marks1 = {85, 90, 78, 88, 92};
    int[] marks2 = {80, 85, 79, 91, 87};

    Student student1 = new Student("Rizwan", marks1);
    Student student2 = new Student("Zainab", marks2);
  
    double avg1 = student1.average();
    double avg2 = student2.average();

    System.out.println(student1.getName() + "'s average: " + avg1);
    System.out.println(student2.getName() + "'s average: " + avg2);

    if (avg1 > avg2) {
      System.out.println(student1.getName() + " has a higher average.");
    } else if (avg2 > avg1) {
      System.out.println(student2.getName() + " has a higher average.");
    } else {
      System.out.println("Both students have the same average.");
    }

    // Creating third student with name of student1 and result array of student2
    Student student3 = new Student(student1.getName(), student2.getResultArray());
    System.out.println("Student 3 Name: " + student3.getName());
    System.out.println("Student 3 Average: " + student3.average());
  }
}

