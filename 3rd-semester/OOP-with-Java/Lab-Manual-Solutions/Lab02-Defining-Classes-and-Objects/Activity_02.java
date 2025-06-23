class Rectangle {
  public int length, width;
  public Rectangle() {
    length = 5;
    width = 2;
  }
  public Rectangle(int myLen, int myWidth) {
    length = myLen;
    width = myWidth;
  }
  public int calArea() {
    return (length * width);
  }
}

public class Activity_02 {
  public static void main(String[] args) {
    Rectangle myRect = new Rectangle();
    System.out.println(myRect.calArea());
    Rectangle myRect1 = new Rectangle(10, 20);
    System.out.println(myRect1.calArea());
  }
}
