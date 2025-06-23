/* Write a generic class, MyMathClass , with a type parameter T where T is a numeric object type (e.g., Integer, Double, or any class that extends java.lang.Number ). Add a method named standardDeviation that takes an ArrayList of type T and returns as a double the standard deviation of the values in the ArrayList . Use the doubleValue () method in the Number class to retrieve the value of each number as a double. Refer to Programming Project 6.5 for a definition of computing the standard deviation. Test your method with suitable data. Your program should generate a compile-time error if your standard deviation method is invoked on an ArrayList that is defined for nonnumeric elements (e.g., Strings ). */

import java.util.ArrayList;

class MyMathClass<T extends Number> {
    // Method to calculate standard deviation
    public double standardDeviation(ArrayList<T> data) {
        if (data.isEmpty()) return 0.0;

        double sum = 0.0;
        for (T value : data) {
            sum += value.doubleValue();
        }

        double mean = sum / data.size();

        double squaredDiffs = 0.0;
        for (T value : data) {
            double diff = value.doubleValue() - mean;
            squaredDiffs += diff * diff;
        }

        return Math.sqrt(squaredDiffs / data.size());
    }
}

public class Lab10_Task_02 {
    public static void main(String[] args) {
        ArrayList<Integer> intList = new ArrayList<>();
        intList.add(10);
        intList.add(12);
        intList.add(23);
        intList.add(23);
        intList.add(16);
        intList.add(23);
        intList.add(21);
        intList.add(16);

        MyMathClass<Integer> intMath = new MyMathClass<>();
        System.out.println("Standard Deviation (Integers): " + intMath.standardDeviation(intList));

        ArrayList<Double> doubleList = new ArrayList<>();
        doubleList.add(10.5);
        doubleList.add(12.0);
        doubleList.add(23.3);
        doubleList.add(16.2);

        MyMathClass<Double> doubleMath = new MyMathClass<>();
        System.out.println("Standard Deviation (Doubles): " + doubleMath.standardDeviation(doubleList));

        // Uncommenting the below lines will cause a compile-time error
        // ArrayList<String> stringList = new ArrayList<>();
        // stringList.add("One");
        // stringList.add("Two");
        // MyMathClass<String> stringMath = new MyMathClass<>(); // ❌ Compile-time error
        // System.out.println("Standard Deviation (Strings): " + stringMath.standardDeviation(stringList));
    }
}

