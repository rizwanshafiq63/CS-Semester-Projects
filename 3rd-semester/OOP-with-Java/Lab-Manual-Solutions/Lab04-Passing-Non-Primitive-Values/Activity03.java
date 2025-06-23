// The following activity demonstrates the creation of a method that accepts two objects.

class Point {
  private int X;
  private int Y;
  public Point() {
    X = 5;
    Y = 6;
  }
  public Point(int a, int c) {
    X = a;
    Y = c;
  }
  public void setX(int a) {
    X = a;
  }
  public void setY(int c) {
    Y = c;
  }
  public int getX() {
    return X;
  }
  public int getY() {
    return Y;
  }
  public Point Add(Point Pa, Point Pb) {
    Point p_new = new Point(X + Pa.X + Pb.X, Y + Pa.Y + Pb.Y);
    return p_new;
  }
  public void display() {
    System.out.println(X);
    System.out.println(Y);
  }
}
public class Activity03 {
  public static void main(String[] args) {
    Point p1 = new Point(10, 20);
    Point p2 = new Point(30, 40);
    Point p3 = new Point();
    Point p4 = p1.Add(p2, p3);
    p4.display();
  }
}

