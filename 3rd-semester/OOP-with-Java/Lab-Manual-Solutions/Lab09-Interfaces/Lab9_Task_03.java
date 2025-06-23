/* Below is the skeleton for a class named “InventoryItem” . Each inventory item has a name and a unique ID number:
class InventoryItem {
  private String name;
  private int uniqueItemID;
}
Flesh out the class with appropriate accessors, constructors, and mutatators. This class will implement the following interface:
Public interface compare {
  boolean compareObjects(Object o);
} */

interface Compare {
  boolean compareObjects(Object o);
}

class InventoryItem implements Compare {
  private String name;
  private int uniqueItemID;

  // Constructor
  public InventoryItem(String name, int uniqueItemID) {
    this.name = name;
    this.uniqueItemID = uniqueItemID;
  }

  // Getters and Setters
  public String getName() {
    return name;
  }
  public int getUniqueItemID() {
    return uniqueItemID;
  }
  public void setName(String name) {
    this.name = name;
  }
  public void setUniqueItemID(int uniqueItemID) {
    this.uniqueItemID = uniqueItemID;
  }

  // Implement compareObjects method
  @Override
  public boolean compareObjects(Object o) {
    if (o instanceof InventoryItem) {
      InventoryItem other = (InventoryItem) o;
      return this.uniqueItemID == other.uniqueItemID;
    }
    return false;
  }

  @Override
  public String toString() {
    return "Item Name: " + name + ", ID: " + uniqueItemID;
  }
}

public class Lab9_Task_03 {
  public static void main(String[] args) {
    InventoryItem item1 = new InventoryItem("Wireless Mouse", 101);
    InventoryItem item2 = new InventoryItem("Gaming Mouse", 101);
    InventoryItem item3 = new InventoryItem("Keyboard", 102);

    System.out.println(item1);
    System.out.println(item2);
    System.out.println(item3);

    System.out.println("item1 equals item2? " + item1.compareObjects(item2));
    System.out.println("item1 equals item3? " + item1.compareObjects(item3));
  }
}


