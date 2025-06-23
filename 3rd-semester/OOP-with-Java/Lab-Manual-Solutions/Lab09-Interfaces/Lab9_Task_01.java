/* Public interface Shape { double getArea(); }
Create two classes Circle and Rectangle. Both must implement the interface Shape.
Note: You can assume appropriate data members for circle and rectangle */


interface Shape {
  double getArea();
}

class Circle implements Shape {
  private double radius;

  public Circle(double radius) {
    this.radius = validateRadius(radius);
  }

  private double validateRadius(double r) {
    if (r > 0) {
      return r;
    } else {
      System.out.println("Radius can't be nagative. Setting radius to '1.0'...");
      return 1.0;
    }
  }

  @Override
  public double getArea() {
    return Math.PI * radius * radius;
  }
}

class Rectangle implements Shape {
  private double length;
  private double width;

  public Rectangle(double length, double width) {
    this.length = validateLength(length);
    this.width = validateWidth(width);
  }

  private double validateLength(double l) {
    if (l > 0) {
      return l;
    } else {
      System.out.println("Length can't be nagative. Setting radius to '1.0'...");
      return 1.0;
    }
  }

  private double validateWidth(double w) {
    if (w > 0) {
      return w;
    } else {
      System.out.println("Width can't be nagative. Setting radius to '1.0'...");
      return 1.0;
    }
  }

  @Override
  public double getArea() {
    return length * width;
  }
}

public class Lab9_Task_01 {
  public static void main(String[] args) {
    Shape circle = new Circle(5.0);
    Shape rectangle = new Rectangle(4.0, 6.0);

    System.out.println("Area of Circle: " + circle.getArea());
    System.out.println("Area of Rectangle: " + rectangle.getArea());
  }
}


