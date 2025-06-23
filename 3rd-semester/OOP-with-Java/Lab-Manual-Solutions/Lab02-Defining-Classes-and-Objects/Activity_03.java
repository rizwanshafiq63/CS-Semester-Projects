class Point {
  private int x;
  private int y;

  //Constructors
  public Point() { //no argument constructor
    x = 1;
    y = 2;
  }
  public Point(int a, int b) {
    x = a;
    y = b;
  }

  //Setters
  public void setX(int a) {
    x = a;
  }
  public void setY(int b) {
    y = b;
  }

  public void display() {
    System.out.println("x coordinate = " + x + " y coordinate = " + y);
  }
  public void movePoint(int a, int b) {
    x += a;
    y += b;
    System.out.println("x coordinate after moving = " + x + " y coordinate after moving = " + y);
  }
}

public class Activity_03 {
  public static void main(String args[]) {
    Point p1 = new Point();
    p1.movePoint(2, 3);
    p1.display();
    Point p2 = new Point();
    p2.movePoint(2, 3);
    p2.display();
  }
}
