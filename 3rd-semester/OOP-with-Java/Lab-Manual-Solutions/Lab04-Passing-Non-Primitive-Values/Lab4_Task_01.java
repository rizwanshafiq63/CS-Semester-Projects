/* Create a class ― Distance‖ with two constructors (no argument, and two argument), two data members ( feet and inches) . Create setter, getter and display method. Create a method that adds two Distance Objects and returns the added Distance Object. */

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
  public void setFeet(int feet){
    if (feet < 0) {
      System.out.println("Feet cannot be negative.");
      feet = 0; // Set default value
    }
    this.feet = feet;
  }
  public void setInches(int inches){
    if (inches < 0 || inches >= 12) {
      System.out.println("Inches must be between 0 and 11.");
      inches = 0; // Set default value
    }
    this.inches = inches;
  }
  public int getFeet(){
    return feet;
  }
  public int getInches(){
    return inches;
  }

  public Distance Add(Distance b) {
    Distance new_dis = new Distance(this.feet + b.feet, this.inches + b.inches);
    if(new_dis.inches >= 12) {
      new_dis.inches -= 12;
      new_dis.feet++;
    }
    return new_dis;
  }
}

public class Lab4_Task_01 {
  public static void main(String[] args) {
    Distance distance1 = new Distance(); //This uses No-Argument Constructor
    distance1.display();

    Distance distance2 = new Distance(5, 8);
    distance2.display();

    Distance distance3 = new Distance();
    distance3 = distance1.Add(distance2);
    distance3.display();
  }
}

