class Circle {
  //Data Member
  private double radius;

  //Constructors
  public Circle(){ //No-Argument Constructor
    radius = 0.0;
  }
  public Circle(double myRadius){ //One-Argument
    if (myRadius > 0) {
      radius = myRadius;
    } else {
      System.out.println("Invalid radius! Setting radius to 0.0.");
      radius = 0.0;  // Default value
    }
  }

  //Getter Method
  public double getRadius(){
    return radius;
  }

  //Calculation Methods
  public double calCircumference() {
    return 2 * Math.PI * radius;
  }

}

public class Lab2_Task_01{
  public static void main(String[] args) {
    Circle circle1 = new Circle();
    System.out.println("Radius of circle1: " + circle1.getRadius());
    System.out.println("Circumference of circle1: " + circle1.calCircumference());
    Circle circle2 = new Circle(6.0);
    System.out.println("Circumference of circle2: " + circle2.calCircumference());
  }
}
