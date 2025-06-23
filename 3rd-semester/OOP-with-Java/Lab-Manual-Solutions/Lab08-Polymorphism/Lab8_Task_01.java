/* Package-delivery services, offer a number of different shipping options, each with specific costs associated.
Create an inheritance hierarchy to represent various types of packages. Use Package as the super class of the hierarchy, then include classes TwoDayPackage and OvernightPackage that derive from Package.
Super class Package should include data members representing the name and address for both the sender and the recipient of the package, in addition to data members that store the weight (in ounces) and cost per ounce to ship the package. Package's constructor should initialize these data members. Ensure that the weight and cost per ounce contain positive values. 
Package should provide a public member function calculateCost() that returns a double indicating the cost associated with shipping the package. Package's calculateCost() function should determine the cost by multiplying the weight by the cost per ounce.
Derived class TwoDayPackage should inherit the functionality of base class Package, but also include a data member that represents a flat fee that the shipping company charges for two-day-delivery service. TwoDayPackage'sconstructor should receive a value to initialize this data member. TwoDayPackage should redefine member function calculateCost() so that it computes the shipping cost by adding the flat fee to the cost calculated by base class Package's calculateCost() function.
Class OvernightPackage should inherit from class Package and contain an additional data member representing an additionalfee charged for overnight-delivery service. OvernightPackage should redefine member function calculateCost() so that it computes the shipping cost by adding the additionalfee to the cost calculated by base class Package's calculateCost() function.
Write a test program that creates objects of each type of Package and tests member function calculateCost() using polymorphism. */

class Package {
  protected String senderName;
  protected String senderAddress;
  protected String recipientName;
  protected String recipientAddress;
  protected Double weight; // In Ounces
  protected Double costPerOunce;

  Package(String senderName, String senderAddress, String recipientName, String recipientAddress, Double weight, Double costPerOunce){
    this.senderName = senderName;
    this.senderAddress = senderAddress;
    this.recipientName = recipientName;
    this.recipientAddress = recipientAddress;
    this.weight = setWeight(weight); // In Ounces
    this.costPerOunce = setCostPerOunce(costPerOunce);
  }

  private Double setWeight(Double w) {
    if (w >= 0) {
      return w;
    } else {
      System.out.println("Weight can't be negative. Setting weight to '1.0'...");
      return 1.0;
    }
  }
  private Double setCostPerOunce(Double c) {
    if (c >= 0) {
      return c;
    } else {
      System.out.println("Cost Per Ounce can't be negatice. Setting cost to '1.0'...");
      return 1.0;
    }
  }
  public Double calculateCost(){
    return weight * costPerOunce;
  }
  public void displayDetails() {
    System.out.println("Sender: " + senderName + ", " + senderAddress);
    System.out.println("Recipient: " + recipientName + ", " + recipientAddress);
    System.out.println("Weight: " + weight + " oz, Cost per ounce: $" + costPerOunce);
  }
}

class TwoDayPackage extends Package {
  private Double flatFee;

  TwoDayPackage(String sn, String sa, String rn, String ra, Double w, Double cpo, Double flatFee) {
    super(sn, sa, rn, ra, w, cpo);
    this.flatFee = flatFee;
  }
  
  @Override
  public Double calculateCost(){
    return flatFee + super.calculateCost();
  }
}

class OvernightPackage extends Package {
    private Double additionalFee;

  OvernightPackage(String sn, String sa, String rn, String ra, Double w, Double cpo, Double additionalFee) {
    super(sn, sa, rn, ra, w, cpo);
    this.additionalFee = additionalFee;
  }
  
  @Override
  public Double calculateCost(){
    return additionalFee + super.calculateCost();
  }
}

public class Lab8_Task_01 {
  public static void main(String[] args) {
    Package[] packages = new Package[3];

    packages[0] = new Package("Ali", "Lahore", "Sara", "Islamabad", 10.0, 2.5);
    packages[1] = new TwoDayPackage("Ahsan", "Karachi", "Fahad", "Rawalpindi", 10.0, 2.5, 5.0);
    packages[2] = new OvernightPackage("Usman", "Multan", "Zara", "Peshawar", 10.0, 2.5, 1.5);

    for (int i = 0; i < packages.length; i++) {
      System.out.println("\n--- Package " + (i + 1) + " ---");
      packages[i].displayDetails();
      System.out.println("Total Shipping Cost: $" + packages[i].calculateCost());
    }
  }
}


