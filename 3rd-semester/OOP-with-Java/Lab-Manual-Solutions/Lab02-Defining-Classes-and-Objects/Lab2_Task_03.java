class Distance {
  // Data members
  private int feet;
  private int inches;

  //Constructors
  public Distance() {
    feet = 0;
    inches = 0;
  }
  public Distance(int myFeet, int myInches) {
    if (myFeet >= 0 && myInches >= 0 && myInches < 12) {
      feet = myFeet;
      inches = myInches;
    } else {
      System.out.println("Invalid values! Feet cannot be negative and Inches must be between 0 and 11.");
      feet = 0;
      inches = 0;  // Set default values
    }
  }

  // Display Method
  public void display() {
    System.out.println("Distance: " + feet + " feet " + inches + " inches");
  }

  //Setter and Getter
  public void setFeet(int myFeet){
    feet = myFeet;
  }
  public void setInches(int myInches){
    inches = myInches;
  }
  public int getFeet(){
    return feet;
  }
  public int getInches(){
    return inches;
  }
}

public class Lab2_Task_03 {
  public static void main(String[] args) {
    Distance distance1 = new Distance(); //This uses No-Argument Constructor
    distance1.display();

    Distance distance2 = new Distance(5, 8);
    distance2.display();

    Distance distance3 = new Distance();
    distance3.setFeet(5);
    distance3.display();
  }
}

