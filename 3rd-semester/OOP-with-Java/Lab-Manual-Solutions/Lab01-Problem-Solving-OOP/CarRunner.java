class Car {
  // Data Members
  public String brand;
  public String model;
  public int year;

  // Methods
  public void displayCarInfo() {
    System.out.println("Car Brand: " + brand);
    System.out.println("Model: " + model);
    System.out.println("Year: " + year);
  }
}

public class CarRunner {
  public static void main(String[] args) {
    // Creating a Car Object
    Car car1 = new Car();
    car1.brand = "Toyota";
    car1.model = "Corolla";
    car1.year = 2022;

    // Displaying Car Information
    car1.displayCarInfo();
  }
}

