/* Write a base class Computer that contains data members of wordsize(in bits), memorysize (in megabytes), storagesize (in megabytes) and speed (in megahertz). Derive a Laptop class that is a kind of computer but also specifies the object’s length, width, height, and weight. Member functions for both classes should include a default constructor, a constructor to inialize all components and a function to display data members. */

// Base Class
class Computer {
  protected int wordSize, memorySize, storageSize, speed;

  // Default constructor
  public Computer() {}
  // Parameterized constructor
  public Computer(int wordSize, int memorySize, int storageSize, int speed) {
    setWordSize(wordSize);
    setMemorySize(memorySize);
    setStorageSize(storageSize);
    setSpeed(speed);
  }

  // Getters
  public int getWordSize() {
    return wordSize;
  }
  public int getMemorySize() {
    return memorySize;
  }
  public int getStorageSize() {
    return storageSize;
  }
  public int getSpeed() {
    return speed;
  }

  // Setters with validation
  public void setWordSize(int wordSize) {
    if (wordSize > 0)
      this.wordSize = wordSize;
    else
      System.out.println("Invalid word size!");
  }
  public void setMemorySize(int memorySize) {
    if (memorySize > 0)
      this.memorySize = memorySize;
    else
      System.out.println("Invalid memory size!");
  }
  public void setStorageSize(int storageSize) {
    if (storageSize > 0)
      this.storageSize = storageSize;
    else
      System.out.println("Invalid storage size!");
  }
  public void setSpeed(int speed) {
    if (speed > 0)
      this.speed = speed;
    else
      System.out.println("Invalid speed!");
  }

  // Display function
  public void display() {
    System.out.println("Word Size: " + wordSize + " bits");
    System.out.println("Memory Size: " + memorySize + " MB");
    System.out.println("Storage Size: " + storageSize + " MB");
    System.out.println("Speed: " + speed + " MHz");
  }
}

// Subclass Laptop
class Laptop extends Computer {
  protected double length, width, height, weight;

  // Default constructor
  public Laptop() {}
  // Parameterized constructor
  public Laptop(int wordSize, int memorySize, int storageSize, int speed, double length, double width, double height, double weight) {
    super(wordSize, memorySize, storageSize, speed);
    setLength(length);
    setWidth(width);
    setHeight(height);
    setWeight(weight);
  }

  // Getters
  public double getLength() {
    return length;
  }
  public double getWidth() {
    return width;
  }
  public double getHeight() {
    return height;
  }
  public double getWeight() {
    return weight;
  }

  // Setters with validation
  public void setLength(double length) {
    if (length > 0)
      this.length = length;
    else
      System.out.println("Invalid length!");
  }
  public void setWidth(double width) {
    if (width > 0)
      this.width = width;
    else
      System.out.println("Invalid width!");
  }
  public void setHeight(double height) {
    if (height > 0)
      this.height = height;
    else
      System.out.println("Invalid height!");
  }
  public void setWeight(double weight) {
    if (weight > 0)
      this.weight = weight;
    else
      System.out.println("Invalid weight!");
  }

  // Display function (overrides Computer's display)
  @Override
  public void display() {
    super.display();
    System.out.println("Length: " + length + " inches");
    System.out.println("Width: " + width + " inches");
    System.out.println("Height: " + height + " inches");
    System.out.println("Weight: " + weight + " kg");
  }
}

// Runner Class
public class Lab6_Task_03 {
  public static void main(String[] args) {
    Computer c1 = new Computer();
    c1.setWordSize(64);
    c1.setMemorySize(16000);
    c1.setStorageSize(512000);
    c1.setSpeed(3200);

    Laptop l1 = new Laptop(64, 16000, 512000, 3200, 13.3, 9.0, 0.6, 1.5);

    System.out.println("Computer Specifications:");
    c1.display();

    System.out.println("\nLaptop Specifications:");
    l1.display();
  }
}

