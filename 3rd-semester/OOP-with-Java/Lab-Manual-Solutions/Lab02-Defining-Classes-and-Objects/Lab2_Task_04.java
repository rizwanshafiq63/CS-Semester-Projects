class Marks {
  // Data members
  private int mark1;
  private int mark2;
  private int mark3;

  // Constructors
  public Marks() {
    mark1 = 0; 
    mark2 = 0; 
    mark3 = 0; 
  }
  public Marks(int m1, int m2, int m3) {
    if (isValidMark(m1) && isValidMark(m2) && isValidMark(m3)) {
      mark1 = m1;
      mark2 = m2;
      mark3 = m3;
    } else {
      System.out.println("Invalid marks! Each mark should be between 0 and 100. Setting marks to default (0).");
      mark1 = 0;
      mark2 = 0;
      mark3 = 0;
    }
  }

  // Validation method for marks
  private boolean isValidMark(int mark) {
    return mark >= 0 && mark <= 100;
  }

  //Calculation Method 
  public int calculateSum() {
    return mark1 + mark2 + mark3; 
  }

  // Getter and Setter
  public int getMark1() {
    return mark1;
  }
  public void setMark1(int m1) {
    if (isValidMark(m1)) {
      mark1 = m1;
    } else {
      System.out.println("Invalid mark! Each mark should be between 0 and 100.");
    }
  }
  public int getMark2() {
    return mark2;
  }
  public void setMark2(int m2) {
    if (isValidMark(m2)) {
      mark2 = m2;
    } else {
      System.out.println("Invalid mark! Each mark should be between 0 and 100.");
    }
  }
  public int getMark3() {
    return mark3;
  }
  public void setMark3(int m3) {
    if (isValidMark(m3)) {
      mark3 = m3;
    } else {
      System.out.println("Invalid mark! Each mark should be between 0 and 100.");
    }
  }
}

public class Lab2_Task_04 {
  public static void main(String[] args) {
    Marks marks1 = new Marks();
    System.out.println("Sum of marks (default): " + marks1.calculateSum());

    Marks marks2 = new Marks(85, 90, 78);
    System.out.println("Sum of marks (custom): " + marks2.calculateSum());

    // Using setter methods to change marks
    marks1.setMark1(75);
    marks1.setMark2(88);
    System.out.println("Sum of marks (changes made with set method): " + marks1.calculateSum());
  }
}

