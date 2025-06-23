/* The following example shows the declaration of class Circle. It has one data members radius. The data member is declared private and access is provided by declaring set and get methods. */

class Circle{
  private int radius; // Data Member
  
  // Constructors
  public Circle() {
    radius = 7;
  }
  public Circle(int radius) {
    this.radius = radius;
  }

  // Setter
  public void setRadius(int radius) {
    this.radius = radius;
  }

  // Getter
  public int getRadius() {
    return radius;
  }

  // Display Method
  public void display() {
    System.out.println("radius = " + radius);
  }

  // Calculation Method
  public double CalculateCircumference() {
    double cir = Math.PI * radius * radius;
    return cir;
  }
}
public class Activity1 {
  public static void main(String args[]) {
    Circle c1 = new Circle();
    c1.setRadius(5);
    System.out.println("Circumference of Circle 1 is: " + c1.CalculateCircumference());
    int r = c1.getRadius();
    Circle c2 = new Circle(r);
    c2.setRadius(10);
    System.out.println("Circumference of Circle 2 is: " + c2.CalculateCircumference());
  }
}
