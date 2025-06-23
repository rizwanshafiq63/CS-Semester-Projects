/* Suppose you operate several hot dog stands distributed throughout town. Define an Encapsulated class named HotDogStand that has an instance variable for the hot dog stand’s ID number and an instance variable for how many hot dogs the stand has sold that day. Create a constructor that allows a user of the class to initialize both values. Also create a method named justSold that increments by one the number of hot dogs the stand has sold. The idea is that this method will be invoked each time the stand sells a hot dog so that you can track the total number of hot dogs sold by the stand.
Write a main method to test your class with at least three hot dog stands that each sell a variety of hot dogs. Use get function to display the hot dogs sold for each object. */

class HotDogStand {
  private int standID;
  private int hotDogsSold;

  // Constructors
  public HotDogStand() {
    this.standID = 0;
    this.hotDogsSold = 0;
  }
  public HotDogStand(int standID, int hotDogsSold) {
    if (standID < 0) {
      throw new IllegalArgumentException("Stand ID cannot be negative.");
    }
    if (hotDogsSold < 0) {
      throw new IllegalArgumentException("Hot dogs sold cannot be negative.");
    }
    this.standID = standID;
    this.hotDogsSold = hotDogsSold;
  }

  // Method to increment a hot dog sale by 1
  public void justSold() {
    hotDogsSold++;
  }

  // Getter for stand ID
  public int getStandID() {
    return standID;
  }

  // Getter for hot dogs sold
  public int getHotDogsSold() {
    return hotDogsSold;
  }
}

public class Lab3_Task_04 {
  public static void main(String[] args) {
    try {
      HotDogStand stand1 = new HotDogStand(1, 0);
      HotDogStand stand2 = new HotDogStand(2, 0);
      HotDogStand stand3 = new HotDogStand(3, 0);

      // Imaginary sales
      stand1.justSold();
      stand1.justSold();
      stand2.justSold();
      stand2.justSold();
      stand2.justSold();
      stand3.justSold();

      // Display sales results
      System.out.println("Hot Dog Stand " + stand1.getStandID() + " sold: " + stand1.getHotDogsSold() + " hot dogs.");
      System.out.println("Hot Dog Stand " + stand2.getStandID() + " sold: " + stand2.getHotDogsSold() + " hot dogs.");
      System.out.println("Hot Dog Stand " + stand3.getStandID() + " sold: " + stand3.getHotDogsSold() + " hot dogs.");
    } catch (IllegalArgumentException e) {
      System.out.println("Error: " + e.getMessage());
    }
  }
}

