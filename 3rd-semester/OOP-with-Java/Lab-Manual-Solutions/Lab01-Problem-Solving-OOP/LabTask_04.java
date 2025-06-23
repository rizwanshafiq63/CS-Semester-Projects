class Rectangle {

  public int length;
  public int width;

  public void display() {
    System.out.println("Length: " + length);
    System.out.println("Width: " + width);
  }

  public int calculateArea() {
    return length * width;
  }
}

public class LabTask_04 {
  public static void main(String[] args) {
    Rectangle rect1 = new Rectangle();
    rect1.length = 10;
    rect1.width = 5;

    rect1.display();

    System.out.println("Area: " + rect1.calculateArea());
  }
}

