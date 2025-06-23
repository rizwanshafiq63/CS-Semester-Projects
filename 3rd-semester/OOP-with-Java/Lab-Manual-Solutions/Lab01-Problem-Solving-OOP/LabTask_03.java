class Car{

  String brand;
  String model;
  int year;

  public void displayInfo() {
    System.out.println("Car Brand: " + brand);
    System.out.println("Model: " + model);
    System.out.println("Year: " + year);
  }
}

public class LabTask_03 {
  public static void main(String[] args) {

    Car Car1 = new Car();
    Car1.brand = "Toyota";
    Car1.model = "Corolla";
    Car1.year = 2022;

    Car1.displayInfo();
  }
}

