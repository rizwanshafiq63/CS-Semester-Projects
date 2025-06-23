/* Design a class Point with two data members x-cord and y-cord. This class should have an arguments constructor, setters, getters and a display function. Now create another class ―Line‖, which contains two Points ―startPoint‖ and ―endPoint‖. It should have a function that finds the length of the line.
Hint: formula is: sqrt((x2-x1)2 + (y2-y1)2)
Create two line objects in runner and display the length of each line. */

// Point class
class Point {
  private double xCord;
  private double yCord;

  // Parameterized Constructor
  public Point(double xCord, double yCord) {
    this.xCord = xCord;
    this.yCord = yCord;
  }

  // Setters
  public void setXCord(double xCord) { 
    this.xCord = xCord;
  }
  public void setYCord(double yCord) {
    this.yCord = yCord;
  }

  // Getters
  public double getXCord() {
    return xCord;
  }
  public double getYCord() {
    return yCord;
  }

  // Display Point
  public void displayPoint() {
    System.out.println("(" + xCord + ", " + yCord + ")");
  }
}

// Line class
class Line {
  private Point startPoint;
  private Point endPoint;

  // Parameterized Constructor
  public Line(Point startPoint, Point endPoint) {
    this.startPoint = startPoint;
    this.endPoint = endPoint;
  }

  // Setters
  public void setStartPoint(Point startPoint) {
    this.startPoint = startPoint;
  }
  public void setEndPoint(Point endPoint) {
    this.endPoint = endPoint;
  }

  // Getters
  public Point getStartPoint() {
    return startPoint;
  }
  public Point getEndPoint() {
    return endPoint;
  }

  // Method to calculate length of the line
  public double calculateLength() {
    double x1 = startPoint.getXCord();
    double y1 = startPoint.getYCord();
    double x2 = endPoint.getXCord();
    double y2 = endPoint.getYCord();

    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
  }

  // Display Line Info
  public void displayLineInfo() {
    System.out.print("Start Point: ");
    startPoint.displayPoint();
    System.out.print("End Point: ");
    endPoint.displayPoint();
    System.out.printf("Length of Line: %.2f\n", calculateLength());
  }
}

// Main class (Runner)
public class Lab5_Task_03 {
  public static void main(String[] args) {
    // Created first line from (1, 2) to (4, 6)
    Point p1 = new Point(1, 2);
    Point p2 = new Point(4, 6);
    Line line1 = new Line(p1, p2);

    // Created second line from (3, 5) to (7, 9)
    Point p3 = new Point(3, 5);
    Point p4 = new Point(7, 9);
    Line line2 = new Line(p3, p4);

    // Display information of line 1
    System.out.println("--- Line 1 Information ---");
    line1.displayLineInfo();

    // Display information of line 2
    System.out.println("\n--- Line 2 Information ---");
    line2.displayLineInfo();
  }
}

