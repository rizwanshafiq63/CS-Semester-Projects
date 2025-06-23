/** Q3. Create a Java applica on on to manage books for a library using permanent storage. The system should allow the following operatons:
a. Add New Book:
  i. Each Book should have a bookID, bookName and status.
b. Borrow Book.
  i. Borrow a book from the available books.
c. Save the new state of Book object.
d. Delete Book.
  i. Delete a book based on bookID.
  ii. Update the storage. **/

import java.io.*;
import java.util.*;
import java.io.Serializable;

class Book implements Serializable {
  private int bookID;
  private String bookName;
  private String status;

  public Book(int bookID, String bookName, String status) {
    this.bookID = bookID;
    this.bookName = bookName;
    this.status = status;
  }

  public int getBookID() {
    return bookID;
  }

  public String getBookName() {
    return bookName;
  }

  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }

  public void display() {
    System.out.println("Book ID: " + bookID);
    System.out.println("Book Name: " + bookName);
    System.out.println("Status: " + status);
    System.out.println("----------------------");
  }
}

// Library Manager
public class Question_03 {
  static final String FILE_NAME = "library_books.ser";

  public static List<Book> loadBooks() {
    List<Book> books = new ArrayList<>();
    try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(FILE_NAME))) {
      while (true) {
        try {
          Book b = (Book) ois.readObject();
          books.add(b);
        } catch (EOFException e) {
          break;
        }
      }
    } catch (Exception e) {
      // file might not exist yet — that’s okay
    }
    return books;
  }

  public static void saveBooks(List<Book> books) {
    try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(FILE_NAME))) {
      for (Book b : books) {
        oos.writeObject(b);
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static void addBook() {
    Scanner sc = new Scanner(System.in);
    List<Book> books = loadBooks();

    System.out.print("Enter Book ID: ");
    int id = sc.nextInt();
    sc.nextLine(); // consume newline
    System.out.print("Enter Book Name: ");
    String name = sc.nextLine();

    books.add(new Book(id, name, "Available"));
    saveBooks(books);
    System.out.println("Book added successfully.");
  }

  public static void borrowBook() {
    Scanner sc = new Scanner(System.in);
    List<Book> books = loadBooks();

    System.out.print("Enter Book ID to Borrow: ");
    int id = sc.nextInt();

    boolean found = false;
    for (Book b : books) {
      if (b.getBookID() == id && b.getStatus().equalsIgnoreCase("Available")) {
        b.setStatus("Borrowed");
        found = true;
        System.out.println("Book borrowed successfully.");
        break;
      }
    }

    if (!found) {
      System.out.println("Book not found or already borrowed.");
    }

    saveBooks(books);
  }

  public static void deleteBook() {
    Scanner sc = new Scanner(System.in);
    List<Book> books = loadBooks();

    System.out.print("Enter Book ID to Delete: ");
    int id = sc.nextInt();

    boolean removed = books.removeIf(b -> b.getBookID() == id);

    if (removed) {
      System.out.println("Book deleted successfully.");
    } else {
      System.out.println("Book not found.");
    }

    saveBooks(books);
  }

  public static void showAllBooks() {
    List<Book> books = loadBooks();
    if (books.isEmpty()) {
      System.out.println("No books in the library.");
    } else {
      for (Book b : books) {
        b.display();
      }
    }
  }

  public static void main(String[] args) {
    try (Scanner sc = new Scanner(System.in)) {
      while (true) {
        System.out.println("\n--- Library Menu ---");
        System.out.println("1. Add New Book");
        System.out.println("2. Borrow Book");
        System.out.println("3. Delete Book");
        System.out.println("4. Show All Books");
        System.out.println("5. Exit");
        System.out.print("Choose: ");
        int choice = sc.nextInt();

        switch (choice) {
          case 1: addBook(); break;
          case 2: borrowBook(); break;
          case 3: deleteBook(); break;
          case 4: showAllBooks(); break;
          case 5: System.exit(0);
          default: System.out.println("Invalid choice.");
        }
      }
    }
  }
}

