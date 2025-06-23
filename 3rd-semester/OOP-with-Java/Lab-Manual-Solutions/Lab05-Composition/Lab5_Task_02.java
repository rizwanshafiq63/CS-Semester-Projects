/* Create a class Book that contains an author of type Person (Note: Use the Person class created in the first exercise). Other data members are bookName and publisher. Modify the address of the author in runner class. */

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

// Book class
class Book {
  private String bookName;
  private String publisher;
  private Person author; // HAS-A relationship (Every Book has an auther)

  // Constructors
  public Book() {
  }
  public Book(String bookName, String publisher, Person author) {
    this.bookName = bookName;
    this.publisher = publisher;
    this.author = author;
  }

  // Setters
  public void setBookName(String bookName) {
    this.bookName = bookName; 
  }
  public void setPublisher(String publisher) { 
    this.publisher = publisher; 
  }
  public void setAuthor(Person author) { 
    this.author = author; 
  }

  // Getters
  public String getBookName() { 
    return bookName;
  }
  public String getPublisher() { 
    return publisher;
  }
  public Person getAuthor() {
    return author;
  }

  // Displaying Book Info
  public void displayBookInfo() {
    System.out.println("Book Name : " + bookName);
    System.out.println("Publisher : " + publisher);
    author.displayPersonInfo(); // Display author's info
  }
}

// Main class (Runner)
public class Lab5_Task_02 {
  public static void main(String[] args) {
    Address authorAddress = new Address("22-B", "19-A", "Boston", "02101");
    Person author = new Person("Colleen Hoover", authorAddress);
   Book book = new Book("It Ends with Us", "ABC Publishing Company", author);
    // Display Book and Author Info
    System.out.println("--- Original Book and Author Info ---");
    book.displayBookInfo();

    // Modify Author's Address
    book.getAuthor().getAddress().setCity("New York");
    authorAddress.setPostalCode("10001");

    // Display Updated Info
    System.out.println("\n--- Updated Author Address ---");
    book.displayBookInfo();
  }
}

