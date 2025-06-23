/* Create a class hierarchy that performs conversions from one system of units to another. Your program should perform the following conversions, i. Liters to Gallons, ii. Fahrenheit to Celsius and iii. Feet to Meters
The Super class convert declares two variables, val1 and val2, which hold the initial and converted values, respectively. It contains an abstract function “compute()”.
The function that will actually perform the conversion, compute() must be defined by the classes derived from convert. The specific nature of compute() will be determined by what type of conversion is taking place.
Three classes will be derived from convert to perform conversions of Liters to Gallons (l_to_g), Fahrenheit to Celsius (f_to_c) and Feet to Meters (f_to_m), respectively. Each derived class implements compute() in its own way to perform the desired conversion.
Test these classes from main() to demonstrate that even though the actual conversion differs between l_to_g, f_to_c, and f_to_m, the interface remains constant. */

abstract class Convert {
  protected Double val1; // initial value
  protected Double val2; // converted value

  public Convert(double val1) {
    this.val1 = val1;
  }

  public abstract void compute();

  public void display() {
    System.out.println("Input: " + val1);
    System.out.println("Converted: " + val2);
  }
}


class LToG extends Convert {
  public LToG(double liters) {
    super(liters);
  }

  @Override
  public void compute() {
    val2 = val1 * 0.264172; // 1 liter = 0.264172 gallons
  }
}

class FToC extends Convert {
  public FToC(double fahrenheit) {
    super(fahrenheit);
  }

  @Override
  public void compute() {
    val2 = (val1 - 32) * 5 / 9; // F to C formula
  }
}

class FToM extends Convert {
  public FToM(double feet) {
    super(feet);
  }

  @Override
  public void compute() {
    val2 = val1 * 0.3048; // 1 foot = 0.3048 meters
  }
}

class Lab8_Task_03 {
  public static void main(String[] args) {
    Convert[] conversions = new Convert[3];

    conversions[0] = new LToG(10);      // 10 liters to gallons
    conversions[1] = new FToC(98.6);    // 98.6°F to °C
    conversions[2] = new FToM(6);       // 6 feet to meters

    for (Convert c : conversions) {
      c.compute();
      c.display();
      System.out.println();
    }
  }
}


