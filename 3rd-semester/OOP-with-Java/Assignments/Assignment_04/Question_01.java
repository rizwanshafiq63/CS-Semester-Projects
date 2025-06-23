/** Q1. Create a class Book that has name(String), publisher (String) and an author (Person).
a. Write ﬁve objects of Book Class in a ﬁle named “BookStore”.
b. Write a func on that displays all Books present in ﬁle “BookStore”.
c. Write a func on that asks the user for the name of a Book and searches the record against that book in the ﬁle “BookStore”. **/

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Scanner;

class Person implements Serializable {
  private String name;

  public Person(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }
}

class Book implements Serializable {
  private String name;
  private String publisher;
  private Person author;

  public Book(String name, String publisher, Person author) {
    this.name = name;
    this.publisher = publisher;
    this.author = author;
  }

  public String getName() {
    return name;
  }

  public String getPublisher() {
    return publisher;
  }

  public Person getAuthor() {
    return author;
  }

  public void display() {
    System.out.println("Book Name: " + name);
    System.out.println("Publisher: " + publisher);
    System.out.println("Author: " + author.getName());
    System.out.println("------------------------");
  }
}

public class Question_01 {
  public static void writeBooksToFile(Book[] books) {
    try {
      ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("BookStore.ser"));
      for (Book b : books) {
        oos.writeObject(b);
      }
      oos.close();
      System.out.println("Books written to BookStore.ser successfully.");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static void displayAllBooks() {
    try {
      ObjectInputStream ois = new ObjectInputStream(new FileInputStream("BookStore.ser"));
      while (true) {
        try {
          Book book = (Book) ois.readObject();
          book.display();
        } catch (Exception e) {
          break; // End of file
        }
      }
      ois.close();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static void searchBookByName() {
    Scanner sc = new Scanner(System.in);
    System.out.print("Enter Book Name to Search: ");
    String searchName = sc.nextLine();

    boolean found = false;

    try {
      ObjectInputStream ois = new ObjectInputStream(new FileInputStream("BookStore.ser"));

      while (true) {
        try {
          Book book = (Book) ois.readObject();
          if (book.getName().equalsIgnoreCase(searchName)) {
            System.out.println("Book Found:");
            book.display();
            found = true;
            break;
          }
        } catch (Exception e) {
          break;
        }
      }

      ois.close();

      if (!found) {
        System.out.println("Book not found in the store.");
      }

    } catch (Exception e) {
      e.printStackTrace();
    }

    sc.close();
  }

  public static void main(String[] args) {
    Book[] books = new Book[5];

    books[0] = new Book("OOP Concepts", "Oxford", new Person("John Smith"));
    books[1] = new Book("Java Mastery", "Pearson", new Person("Alice Johnson"));
    books[2] = new Book("Clean Code", "Prentice Hall", new Person("Robert Martin"));
    books[3] = new Book("Data Structures", "McGraw Hill", new Person("Sarah Allen"));
    books[4] = new Book("Algorithms", "MIT Press", new Person("Thomas Cormen"));

    writeBooksToFile(books);
    displayAllBooks();
    searchBookByName();
  }
}


