/* Create a generic class with a type parameter that simulates drawing an item at random out of a box. This class could be used for simulating a random drawing. For example, the box might contain Strings representing names written on a slip of paper, or the box might contain Integers representing a random drawing for a lottery based on numeric lottery picks.
Create an add method that allows the user of the class to add an object of the specified type along with an isEmpty method that determines whether or not the box is empty. Finally, your class should have a drawItem method that randomly selects an object from the box and returns it. If the user attempts to drawn an item out of an empty box, return null . Write a main method that tests your class. */

import java.util.ArrayList;
import java.util.Random;

class Box<T> {
    private ArrayList<T> items;
    private Random rand;

    public Box() {
        items = new ArrayList<>();
        rand = new Random();
    }

    // Method to add an item
    public void add(T item) {
        items.add(item);
    }

    // Method to check if the box is empty
    public boolean isEmpty() {
        return items.isEmpty();
    }

    // Method to draw an item at random
    public T drawItem() {
        if (isEmpty()) {
            return null;
        }
        int index = rand.nextInt(items.size());
        return items.get(index);
    }
}

public class Lab10_Task_03 {
    public static void main(String[] args) {
        // Box of Strings
        Box<String> nameBox = new Box<>();
        nameBox.add("Alice");
        nameBox.add("Bob");
        nameBox.add("Charlie");
        nameBox.add("Diana");

        System.out.println("Drawing from name box:");
        for (int i = 0; i < 3; i++) {
            System.out.println("Drawn: " + nameBox.drawItem());
        }

        // Box of Integers
        Box<Integer> lotteryBox = new Box<>();
        lotteryBox.add(101);
        lotteryBox.add(202);
        lotteryBox.add(303);
        lotteryBox.add(404);

        System.out.println("\nDrawing from lottery box:");
        for (int i = 0; i < 3; i++) {
            System.out.println("Drawn number: " + lotteryBox.drawItem());
        }

        // Drawing from an empty box
        Box<Double> emptyBox = new Box<>();
        System.out.println("\nDrawing from empty box: " + emptyBox.drawItem());  // should return null
    }
}

