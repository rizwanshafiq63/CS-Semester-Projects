/* The following example shows the declaration of class Rectangle. It has two data members that represent the length and width of rectangle. Both data member are declared private and access is provided by declaring set and get methods for both data members. */

class Rectangle {
  private int length, width; // Data Members
  
  // Constructors
  public Rectangle() {
    length = 5;
    width = 2;
  }
  public Rectangle(int length, int width) {
    this.length = length;
    this.width = width;
  }

  // Setters
  public void setLength(int length) {
    this.length = length;
  }
  public void setWidth(int width) {
    this.width = width;
  }

  // Getters
  public int getLength() {
    return length;
  }
  public int getWidth() {
    return width;
  }

  // Method to calculate Area
  public int area() {
    return (length * width);
  }
}
public class Activity2 {
  public static void main() {
    Rectangle rect = new Rectangle();
    rect.setLength(5);
    rect.setWidth(15);
    System.out.println("Area of Rectangle is: " + rect.area());
    System.out.println("Width of Rectangle is: " + rect.getWidth());
  }
}
