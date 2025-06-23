/* Create an Address class, which contains street#, house#, city and code. Create another class Person that contains an address of type Address. Give appropriate get and set functions for both classes. Test class person in main. */

// Address class
class Address {
  private String streetNo; // Street No. can be 13-B
  private String houseNo; // House No. can be 132/B
  private String city;
  private String postalCode;

  // Constructors
  public Address() {
  }
  public Address(String streetNo, String houseNo, String city, String postalCode) {
    this.streetNo = streetNo;
    this.houseNo = houseNo;
    this.city = city;
    this.postalCode = postalCode;
  }

  // Setters
  public void setStreetNo(String streetNo) {
    this.streetNo = streetNo;
  }
  public void setHouseNo(String houseNo) {
    this.houseNo = houseNo;
  }
  public void setCity(String city) {
    this.city = city;
  }
  public void setPostalCode(String postalCode) {
    this.postalCode = postalCode;
  }

  // Getters
  public String getStreetNo() {
    return streetNo;
  }
  public String getHouseNo() {
    return houseNo;
  }
  public String getCity() {
    return city;
  }
  public String getPostalCode() {
    return postalCode;
  }

  // Method to display Address details
  public void displayAddress() {
    System.out.println("Street #: " + streetNo);
    System.out.println("House #: " + houseNo);
    System.out.println("City    : " + city);
    System.out.println("Code    : " + postalCode);
  }
}

// Person class
class Person {
  private String name;
  private Address address; // HAS-A relationship

  // Constructors
  public Person() {
  }
  public Person(String name, Address address) {
    this.name = name;
    this.address = address;
  }

  // Setters
  public void setName(String name) {
    this.name = name;
  }
  public void setAddress(Address address) {
    this.address = address;
  }

  // Getters
  public String getName() {
    return name;
  }
  public Address getAddress() {
    return address;
  }

  // Method to display 
  public void displayPersonInfo() {
    System.out.println("Name    : " + name);
    address.displayAddress();
  }
}

// Main Class
public class Lab5_Task_01 {
  public static void main(String[] args) {
    Address a1 = new Address("08", "06", "Bahawalpur", "63100");
    Person rizwan = new Person("Muhammad Rizwan Shafiq", a1);
    // Display Person Information
    rizwan.displayPersonInfo();

    // Updating Address
    rizwan.setName("Bob Smith");
    rizwan.getAddress().setCity("Islamabad");
    rizwan.getAddress().setPostalCode("77001");

    // Displaying updated information
    System.out.println("\n--- Updated Person Info ---");
    rizwan.displayPersonInfo();
  }
}

