class Rectangle {
  public int length, width;
  public int calArea() {
    return (length * width);
  }
}
public class Activity_01 {
  public static void main(String args[]) {
    Rectangle myRectangle = new Rectangle();
    myRectangle.length = 10;
    myRectangle.width = 5;
    System.out.println(myRectangle.calArea());
  }
}


