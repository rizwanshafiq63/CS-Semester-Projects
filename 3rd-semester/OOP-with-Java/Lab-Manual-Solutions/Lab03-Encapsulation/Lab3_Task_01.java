/* Create an Encapsulated class Marks with three data members to store three marks. Create set and get methods for all data members. Test the class in runner */

class Marks {
  private int mark1; // Data Members
  private int mark2;
  private int mark3;

  // Constructors (Validation Applied through a pvt method)
  public Marks(int mark1, int mark2, int mark3) {
    this.mark1 = validateMark(mark1);
    this.mark2 = validateMark(mark2);
    this.mark3 = validateMark(mark3);
  }

  // Validation method
  private int validateMark(int mark) {
    if (mark < 0 || mark > 100) {
      throw new IllegalArgumentException("Marks entered must be between 0 and 100.");
    }
    return mark;
  }

  // Setters
  public void setMark1(int mark1) {
    this.mark1 = validateMark(mark1);
  }

  public void setMark2(int mark2) {
    this.mark2 = validateMark(mark2);
  }

  public void setMark3(int mark3) {
    this.mark3 = validateMark(mark3);
  }

  // Getters
  public int getMark1() {
    return mark1;
  }

  public int getMark2() {
    return mark2;
  }

  public int getMark3() {
    return mark3;
  }

  // Display Method
  public void displayMarks() {
    System.out.println("Marks: " + mark1 + ", " + mark2 + ", " + mark3);
  }
}

public class Lab3_Task_01 {
  public static void main(String[] args) {
    Marks studentMarks = new Marks(85, 90, 78);
    studentMarks.displayMarks();

    // Modifying marks using setters
    studentMarks.setMark1(88);
    studentMarks.setMark2(92);
    studentMarks.setMark3(80);

    System.out.println("Updated Marks:");
    studentMarks.displayMarks();
  }
}

