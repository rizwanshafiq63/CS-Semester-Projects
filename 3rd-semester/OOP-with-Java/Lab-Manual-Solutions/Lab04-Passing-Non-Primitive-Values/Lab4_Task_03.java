class Fraction {
  private int numerator;
  private int denominator;

  // Constructors
  public Fraction() {
    this.numerator = 0;
    this.denominator = 1; // Division by zero gives error
  }
  public Fraction(int numerator, int denominator) {
    if (denominator == 0) {
      throw new IllegalArgumentException("Denominator cannot be zero");
    }
    this.numerator = numerator;
    this.denominator = denominator;
  }

  // Setter methods
  public void setNumerator(int numerator) {
    this.numerator = numerator;
  }
  public void setDenominator(int denominator) {
    if (denominator == 0) {
      throw new IllegalArgumentException("Denominator cannot be zero");
    }
    this.denominator = denominator;
  }

  // Getter methods
  public int getNumerator() {
    return numerator;
  }
  public int getDenominator() {
    return denominator;
  }

  // Display method
  public void display() {
    System.out.println(numerator + "/" + denominator);
  }

  // Equals method
  public boolean equals(Fraction other) {
    return this.numerator * other.denominator == this.denominator * other.numerator;
  }
}

// Runner class
public class Lab4_Task_03 {
  public static void main(String[] args) {
    // Creating fraction objects
    Fraction f1 = new Fraction(12, 2);
    Fraction f2 = new Fraction(60, 10);

    // Displaying fractions
    System.out.print("Fraction 1: ");
    f1.display();
    System.out.print("Fraction 2: ");
    f2.display();

    // Check if fractions are equal
    if (f1.equals(f2)) {
      System.out.println("The fractions are identical.");
    } else {
      System.out.println("The fractions are not identical.");
    }
  }
}

