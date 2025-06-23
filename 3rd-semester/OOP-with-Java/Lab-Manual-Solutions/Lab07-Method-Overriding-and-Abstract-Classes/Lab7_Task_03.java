/* Create an abstract class that stores data about the shapes e.g. Number of Lines in a Shape, Pen Color, Fill Color and an abstract method draw. Implement the method draw for Circle, Square and Triangle subclasses, the better approach is to draw these figures on screen, if you can’t then just use a display message in the draw function. */

// Abstract class Shape
abstract class Shape {
  protected int numberOfLines;
  protected String penColor;
  protected String fillColor;

  public Shape(int numberOfLines, String penColor, String fillColor) {
    this.numberOfLines = numberOfLines;
    this.penColor = penColor;
    this.fillColor = fillColor;
  }

  // Abstract method to be implemented by subclasses
  public abstract void draw();
}

// Circle class extending Shape
class Circle extends Shape {
  public Circle(String penColor, String fillColor) {
    super(0, penColor, fillColor); // Circles have no straight lines
  }

  @Override
  public void draw() {
    System.out.println("Drawing a Circle with Pen Color: " + penColor + " and Fill Color: " + fillColor);
  }
}

// Square class extending Shape
class Square extends Shape {
  public Square(String penColor, String fillColor) {
    super(4, penColor, fillColor);
  }

  @Override
  public void draw() {
    System.out.println("Drawing a Square with Pen Color: " + penColor + " and Fill Color: " + fillColor);
  }
}

// Triangle class extending Shape
class Triangle extends Shape {
  public Triangle(String penColor, String fillColor) {
    super(3, penColor, fillColor);
  }

  @Override
  public void draw() {
    System.out.println("Drawing a Triangle with Pen Color: " + penColor + " and Fill Color: " + fillColor);
  }
}

// Testing the implementation
public class Lab7_Task_03 {
  public static void main(String[] args) {
    Shape circle = new Circle("Red", "Blue");
    Shape square = new Square("Black", "Green");
    Shape triangle = new Triangle("Yellow", "Pink");

    circle.draw();
    square.draw();
    triangle.draw();
  }
}
