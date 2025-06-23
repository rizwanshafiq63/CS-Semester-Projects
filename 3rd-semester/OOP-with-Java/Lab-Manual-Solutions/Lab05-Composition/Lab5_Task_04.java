/* Create a class named Pizza that stores information about a single pizza. It should contain the following:
Private instance variables to store the size of the pizza (either small, medium, or large), the number of cheese toppings, the number of pepperoni toppings, and the number of ham toppings.
Constructor(s) that set all of the instance variables.
Public methods to get and set the instance variables.
A public method named calcCost( ) that returns a double that is the cost of the pizza. Pizza cost is determined by:
Small: $10 + $2 per topping Medium: $12 + $2 per topping Large: $14 + $2 per topping
public method named getDescription( ) that returns a String containing the pizza size, quantity of each topping.
Write test code to create several pizzas and output their descriptions. For example, a large pizza with one cheese, one pepperoni and two ham toppings should cost a total of $22. Now Create a PizzaOrder class that allows up to three pizzas to be saved in an order. Each pizza saved should be a Pizza object. Create a method calcTotal() that returns the cost of order. In the runner order two pizzas and return the total cost. */

// Pizza class
class Pizza {
  // Private instance variables
  private String size; // small, medium, large
  private int cheeseToppings;
  private int pepperoniToppings;
  private int hamToppings;

  // Parameterized Constructor
  public Pizza(String size, int cheeseToppings, int pepperoniToppings, int hamToppings) {
    if (validateSize(size)) {
      this.size = size.toLowerCase();
    } else {
      System.out.println("Invalid size provided! Defaulting to 'small'.");
      this.size = "small";
    }
    this.cheeseToppings = cheeseToppings;
    this.pepperoniToppings = pepperoniToppings;
    this.hamToppings = hamToppings;
  }

  // Private method to validate size
  private boolean validateSize(String size) {
    size = size.toLowerCase();
    return size.equals("small") || size.equals("medium") || size.equals("large");
  }

  // Getters
  public String getSize() {
    return size;
  }
  public int getCheeseToppings() {
    return cheeseToppings;
  }
  public int getPepperoniToppings() {
    return pepperoniToppings;
  }
  public int getHamToppings() {
    return hamToppings;
  }

  // Setters
  public void setSize(String size) {
    if (validateSize(size)) {
      this.size = size.toLowerCase();
    } else {
      System.out.println("Invalid size provided! Size not changed.");
    }
  }
  public void setCheeseToppings(int cheeseToppings) {
    this.cheeseToppings = cheeseToppings;
  }
  public void setPepperoniToppings(int pepperoniToppings) {
    this.pepperoniToppings = pepperoniToppings;
  }
  public void setHamToppings(int hamToppings) {
    this.hamToppings = hamToppings;
  }

  // Calculate cost of pizza
  public double calcCost() {
    double basePrice;
    if (size.equals("small")) {
      basePrice = 10;
    } else if (size.equals("medium")) {
      basePrice = 12;
    } else { //large
      basePrice = 14;
    }
    int totalToppings = cheeseToppings + pepperoniToppings + hamToppings;
    return basePrice + (2 * totalToppings);
  }

  // Return pizza description
  public String getDescription() {
    return "Pizza Size: " +size+ ", Cheese Toppings: " +cheeseToppings+ ", Pepperoni Toppings: " +pepperoniToppings+ ", Ham Toppings: " +hamToppings+ ", Total Cost: $" +calcCost();
  }
}

// PizzaOrder class
class PizzaOrder {
  private Pizza[] pizzas; // Array to store pizzas (up to 3)
  private int count; // To keep track of number of pizzas added

  // Constructor
  public PizzaOrder() {
    pizzas = new Pizza[3];
    count = 0;
  }

  // Method to add pizza to order
  public void addPizza(Pizza pizza) {
    if (count < 3) {
      pizzas[count] = pizza;
      count++;
    } else {
      System.out.println("Cannot add more than 3 pizzas to the order.");
    }
  }

  // Method to calculate total cost of order
  public double calcTotal() {
    double total = 0;
    for (int i = 0; i < count; i++) {
      total += pizzas[i].calcCost();
    }
    return total;
  }

  // Display order details
  public void displayOrderDetails() {
    System.out.println("\n---------------------------\n--- Pizza Order Details ---\n---------------------------");
    for (int i = 0; i < count; i++) {
      System.out.println((i + 1) + ". " + pizzas[i].getDescription());
    }
    System.out.printf("---------------------------\nTotal Order Cost: $%.2f\n---------------------------", calcTotal());
  }
}

// Main class (Runner)
public class Lab5_Task_04 {
  public static void main(String[] args) {
    // Creating PizzaOrder object
    PizzaOrder order = new PizzaOrder();
    
    // Creating Pizza objects
    Pizza pizza1 = new Pizza("large", 1, 1, 2);
    Pizza pizza2 = new Pizza("small", 2, 2, 1);
    pizza2.setSize("medium");

    // Add pizzas to order
    order.addPizza(pizza1);
    order.addPizza(pizza2);

    // Display order details and total cost
    order.displayOrderDetails();
  }
}

