/* Create an abstract class “Person”, with data member “name”. Create set and get methods, and an abstract Boolean method “isOutstanding()”.
Derive two classes Student and Professor. Student class has data member CGPA.
Professor Class has data member numberOfPublications. Provide setters and getters and implementation of abstract function in both classes.
In student class isOutstanding() will return true if CGPA is greater than 3.5. In the Professor class isOutstanding() will return true, if numberOfPublications> 50.
In the main class create an array of Person class and call isOutstanding() function for student and professor. isOutstanding() for professor should be called after setting the publication count to 100.*/

abstract class Person {
  protected String name;

  Person() {}
  Person(String name) {
    this.name = name;
  }
  public void setName(String name) {
    this.name = name;
  }
  public String getName() {
    return name;
  }
  abstract public Boolean isOutStanding();
}

class Student extends Person {
  private Double cgpa;

  public Student() {
    super();
  }
  public Student(String name, Double cgpa){
    super(name);
    this.cgpa = validateCGPA(cgpa);
  }

  private Double validateCGPA(Double cgpa){
    if (cgpa >= 0.0) {
      return cgpa;
    } else {
      System.out.println("\nCGPA can't be nagative! Setting CGPA to '0.0'...");
      return 0.0;
    }
  }
  public void setCgpa(Double cgpa) {
    this.cgpa = validateCGPA(cgpa);
  }
  public Double getCgpa() {
    return cgpa;
  }
  @Override
  public Boolean isOutStanding() {
    if (this.cgpa > 3.5) {
      return true;
    } else {
      return false;
    }
  }
}

class Professor extends Person {
  private int numberOfPublications;

  public Professor() {
    super();
  }
  public Professor(String name, int numberOfPublications){
    super(name);
    this.numberOfPublications = validatePublications(numberOfPublications);
  }

  private int validatePublications(int publications){
    if (publications >= 0) {
      return publications;
    } else {
      System.out.println("\nNo. of publications can't be nagative! Setting no. of publications to '0'...");
      return 0;
    }
  }
  public void setNumberOfPublications(int numberOfPublications) {
    this.numberOfPublications = validatePublications(numberOfPublications);
  }
  public int getNumberOfPublications() {
    return numberOfPublications;
  }
  @Override
  public Boolean isOutStanding() {
    if (this.numberOfPublications > 50) {
      return true;
    } else {
      return false;
    }
  }
}

public class Lab8_Task_02 {
  public static void main(String[] args) {
    Person[] people = new Person[2];

    Student student = new Student();
    student.setName("Ahsan");
    student.setCgpa(3.9);

    Professor professor = new Professor("Dr. Rizwan", 100);

    people[0] = student;
    people[1] = professor;

    for (Person p : people) {
      System.out.println("Name: " + p.getName());
      System.out.println("Is Outstanding? " + p.isOutStanding());
      System.out.println();
    }
  }
}


