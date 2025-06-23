/* The following example shows the declaration of class Point. It has two data members that represent the x and y coordinate of a point. Both data member are declared private and access is provided by declaring set and get methods for both data members. */

class Point {
  private int x; //Data Members
  private int y;

  // Constructors
  public Point() {
    x = 0;
    y = 0;
  }
  public Point(int a, int b) {
    x = a;
    y = b;
  }

  // Setters
  public void setX(int a) {
    x = a;
  }
  public void setY(int b) {
    y = b;
  }

  // Getters
  public int getX() {
    return x;
  }
  public int getY() {
    return y;
  }

  // Display Method
  public void display() {
    System.out.println("x coordinate = " + x
      + " y coordinate = " + y);
  }

  // Method to move points
  public void movePoint(int a, int b) {
    x = x + a;
    y = y + b;
  }
}

public class Activity3 {
  public static void main(String[] args) {
    Point p1 = new Point();
    p1.setX(7);
    p1.setY(5);
    p1.display();
    Point p2 = new Point(7, 6);
    p2.movePoint(5, 4);
    p2.display();
  }
}
