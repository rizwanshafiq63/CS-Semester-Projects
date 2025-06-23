/* Imagine a publishing company that markets both book and audio-cassette versions of its works. Create a class publication that stores the title and price of a publication. From this class derive two classes:
i. book, which adds a page count and
ii. tape, which adds a playing time in minutes.
Each of these three classes should have set() and get() functions and a display() function to display its data. Write a main() program to test the book and tape class by creating instances of them, asking the user to fill in their data and then displaying the data with display(). */

import java.util.Scanner;

// Base Class
class Publication {
  protected String title;
  protected double price;

  public Publication() {}

  public Publication(String title, double price) {
    this.title = title;
    this.price = price;
  }

  public void set(String title, double price) {
    this.title = title;
    this.price = price;
  }

  public String getTitle() {
    return title;
  }

  public double getPrice() {
    return price;
  }

  public void display() {
    System.out.println("Title: " + title + ", Price: " + price);
  }
}

// Subclass Book
class Book extends Publication {
  protected int pageCount;

  public Book() {}

  public Book(String title, double price, int pageCount) {
    super(title, price);
    this.pageCount = pageCount;
  }

  public void set(String title, double price, int pageCount) {
    super.set(title, price);
    this.pageCount = pageCount;
  }

  @Override
  public void display() {
    super.display();
    System.out.println("Page Count: " + pageCount);
  }
}

// Subclass Tape
class Tape extends Publication {
  protected int playingTime;

  public Tape() {}

  public Tape(String title, double price, int playingTime) {
    super(title, price);
    this.playingTime = playingTime;
  }

  public void set(String title, double price, int playingTime) {
    super.set(title, price);
    this.playingTime = playingTime;
  }

  @Override
  public void display() {
    super.display();
    System.out.println("Playing Time (minutes): " + playingTime);
  }
}

// Runner Class
public class Lab6_Task_02 {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);

    Book book = new Book();
    System.out.println("Enter Book Title, Price, and Page Count:");
    book.set(sc.nextLine(), sc.nextDouble(), sc.nextInt());
    sc.nextLine(); 

    Tape tape = new Tape();
    System.out.println("Enter Tape Title, Price, and Playing Time (minutes):");
    tape.set(sc.nextLine(), sc.nextDouble(), sc.nextInt());

    System.out.println("\nBook Details:");
    book.display();

    System.out.println("\nTape Details:");
    tape.display();

    sc.close();
  }
}

