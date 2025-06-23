/* Write a program that declares two classes. The parent class is called Simple that has two data members num1 and num2 to store two numbers. It also has four member functions.
The add() function adds two numbers and displays the result. The sub() function subtracts two numbers and displays the result.
The mul() function multiplies two numbers and displays the result. The div() function divides two numbers and displays the result.
The child class is called VerifiedSimple that overrides all four functions. Each function in the child class checks the value of data members. It calls the corresponding member function in the parent class if the values are greater than 0. Otherwise it displays error message. */

// Parent class Simple
class Simple {
  protected int num1, num2;

  public Simple(int num1, int num2) {
    this.num1 = num1;
    this.num2 = num2;
  }
  
  // Member functions
  public void add() {
    System.out.println("Addition: " + (num1 + num2));
  }
  public void sub() {
    System.out.println("Subtraction: " + (num1 - num2));
  }
  public void mul() {
    System.out.println("Multiplication: " + (num1 * num2));
  }
  public void div() {
    if (num2 != 0) {
      System.out.println("Division: " + ((double) num1 / num2));
    } else {
      System.out.println("Error: Division by zero is not allowed.");
    }
  }
}

// Child class VerifiedSimple
class VerifiedSimple extends Simple {
  public VerifiedSimple(int num1, int num2) {
    super(num1, num2);
  }

  @Override
  public void add() {
    if (num1 > 0 && num2 > 0) {
      super.add();
    } else {
      System.out.println("Error: Both numbers must be greater than zero for addition.");
    }
  }

  @Override
  public void sub() {
    if (num1 > 0 && num2 > 0) {
      super.sub();
    } else {
      System.out.println("Error: Both numbers must be greater than zero for subtraction.");
    }
  }

  @Override
  public void mul() {
    if (num1 > 0 && num2 > 0) {
      super.mul();
    } else {
      System.out.println("Error: Both numbers must be greater than zero for multiplication.");
    }
  }

  @Override
  public void div() {
    if (num1 > 0 && num2 > 0) {
      super.div();
    } else {
      System.out.println("Error: Both numbers must be greater than zero for division.");
    }
  }
}

// Testing the classes
public class Lab7_Task_02 {
  public static void main(String[] args) {
    System.out.println("Testing Simple class:");
    Simple s = new Simple(10, 5);
    s.add();
    s.sub();
    s.mul();
    s.div();

    System.out.println("\nTesting VerifiedSimple class:");
    VerifiedSimple vs1 = new VerifiedSimple(10, 5);
    vs1.add();
    vs1.sub();
    vs1.mul();
    vs1.div();

    System.out.println("\nTesting VerifiedSimple with negative values:");
    VerifiedSimple vs2 = new VerifiedSimple(-10, 5);
    vs2.add();
    vs2.sub();
    vs2.mul();
    vs2.div();
  }
}

