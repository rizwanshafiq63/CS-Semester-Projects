import java.util.Scanner;

class CarPart {

  private String modelNumber;
  private String partNumber;
  private String cost;

  public void setparameter(String x, String y, String z) {
    modelNumber = x;
    partNumber = y;
    cost = z;
  }

  public void display() {
    System.out.println("Model Number: " + modelNumber + "\nPart Number: " + partNumber+ "\nCost: " + cost);
  }
}
public class CarPartRunner {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    CarPart car1 = new CarPart();
    System.out.println("What is Model Number?");
    System.out.println("What is Part Number?");
    System.out.println("What is Cost?");
    String x = sc.nextLine();
    String y = sc.nextLine();
    String z = sc.nextLine();
    car1.setparameter(x, y, z);
    car1.display();
    sc.close();
  }
}

