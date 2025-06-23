import java.util.*;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

// ================================
//     Interfaces To Implement
// ================================
interface Loanable {
  void checkOut(Patron patron);
  void checkIn();
  boolean isOverdue();
  void renew();
}

interface FineCalculatable {
  double calculateFine(int daysLate);
  double getFineRate();
  double getMaxFine();
}

interface Searchable {
  boolean searchByTitle(String title);
  boolean searchByAuthor(String author);
  boolean filterByAvailability();
}

interface Reportable {
  void generateOverdueReport();
  void generatePopularItemsReport();
  void generateUsageStatistics();
}

// ================================
//     Library Materials
// ================================
abstract class LibraryMaterial implements Loanable, FineCalculatable, Searchable {
  protected String title;
  protected String author;
  protected boolean isAvailable = true;
  protected boolean isChildrenFriendly = false;
  protected LocalDate dueDate = null;
  protected Patron checkedOutBy = null;
  protected Queue<Patron> reservationQueue = new LinkedList<>();
  protected LibraryManagement library;

  // Advanced Search fields
  protected int publicationYear;
  protected String language;
  protected String genre;
  protected String materialType; 

  public LibraryMaterial(String title, String author, boolean isChildrenFriendly, String materialType) {
    this.title = title;
    this.author = author;
    this.isChildrenFriendly = isChildrenFriendly;
    this.materialType = materialType;
  }

  public void setPublicationYear(int year) { this.publicationYear = year; }
  public void setLanguage(String lang) { this.language = lang; }
  public void setGenre(String genre) { this.genre = genre; }
  public void setMaterialType(String type) { this.materialType = type; }
  public void setLibraryReference(LibraryManagement lib) { this.library = lib; }

  public int getPublicationYear() { return publicationYear; }
  public String getLanguage() { return language; }
  public String getGenre() { return genre; }
  public String getMaterialType() { return materialType; }
  public String getTitle() { return title; }
  public String getAuthor() { return author; }

  public boolean isChildrenFriendly() { return isChildrenFriendly; }
  public void setChildrenFriendly(boolean value) { this.isChildrenFriendly = value; }

  public boolean searchByTitle(String search) {
    return title.toLowerCase().contains(search.toLowerCase());
  }

  public boolean searchByAuthor(String search) {
    return author.toLowerCase().contains(search.toLowerCase());
  }

  public boolean filterByAvailability() {
    return isAvailable;
  }

  public void placeHold(Patron patron) {
    if (!reservationQueue.contains(patron)) {
      reservationQueue.offer(patron);
      System.out.println(patron.name + " placed a hold on \"" + this.title + "\".");
    } else {
      System.out.println(patron.name + " already has a hold on \"" + this.title + "\".");
    }
  }

  @Override
  public void checkOut(Patron patron) {
    if (patron instanceof Child && !isChildrenFriendly) {
      System.out.println("This " + materialType + " \"" + title + "\" is not suitable for children. Checkout denied.");
      return;
    }
    if (!isAvailable) {
      System.out.println("This " + materialType + " is already checked out.");
      return;
    }
    if (patron.isSuspended()) {
      System.out.println("Account suspended: " + patron.name + ". Cannot check out.");
      return;
    }
    if (!patron.canBorrow()) {
      return;
    }
    if (library != null) {
      library.recordTransaction(this.title, patron, "Borrowed");
    }
    checkedOutBy = patron;
    isAvailable = false;
    dueDate = LocalDate.now().plusDays(patron.loanDuration);
    System.out.println(materialType+ " \"" + title + "\" checked out for " + patron.loanDuration + " days. Checked out by: " + patron.name + " (" + patron.getClass().getSimpleName() + ")");
  }

  @Override
  public void checkIn() {
    if (library != null && checkedOutBy != null) {
      library.recordTransaction(this.title, checkedOutBy, "Returned");
    }
    // Calculate fine and add to patron balance if overdue
    if (isOverdue() && checkedOutBy != null) {
      double originalFine = calculateFine(0);
      double adjustedFine = checkedOutBy.getFine(originalFine);
      checkedOutBy.addFine(adjustedFine);
      System.out.println(checkedOutBy.name + " fined $" + adjustedFine + " for overdue \"" + title + "\".");
    }
    isAvailable = true;
    dueDate = null;
    checkedOutBy = null;
    System.out.println(materialType + " \"" + title+ "\" returned.");
    if (!reservationQueue.isEmpty()) {
      Patron next = reservationQueue.poll();
      System.out.println("Notification: \"" + title + "\" is now available for " + next.name + ". They have 48 hours to pick it up.");
    }
  }

  @Override
  public boolean isOverdue() {
    return dueDate != null && LocalDate.now().isAfter(dueDate);
  }

  @Override
  public void renew() {
    if (dueDate != null) {
      dueDate = dueDate.plusDays(21);
      System.out.println(materialType + " \"" + title+ "\" renewed. New due date: " + dueDate);
      if (library != null && checkedOutBy != null) {
        library.recordTransaction(this.title, checkedOutBy, "Renewed");
      }
    } else {
      System.out.println("Cannot renew: " + materialType + " \"" + title + "\" was not checked out.");
    }
  }

  @Override
  public double calculateFine(int ignored) {
    if (dueDate == null || !isOverdue()) return 0.0;
    // long daysLate = ignored;
    long daysLate = ChronoUnit.DAYS.between(dueDate, LocalDate.now());
    double fine = getFineRate() * daysLate;
    return Math.min(fine, getMaxFine());
  }

  public abstract double getFineRate();
  public abstract double getMaxFine();
  public abstract void display();
}

// ----------------------------------------

class Book extends LibraryMaterial {
  private String ISBN, publisher;
  private int edition;

  public Book(String title, String author, boolean isChildrenFriendly, String ISBN, String publisher, int edition) {
    super(title, author, isChildrenFriendly, "Book");
    this.ISBN = ISBN;
    this.publisher = publisher;
    this.edition = edition;
  }

  public boolean searchByISBN(String isbn) {
    return ISBN != null && ISBN.equalsIgnoreCase(isbn);
  }

  public double getFineRate() { return 0.25; }
  public double getMaxFine() { return 10.0; }

  public void display() {
    System.out.println("========== BOOK ==========");
    System.out.println("Title           : " + title);
    System.out.println("Author          : " + author);
    System.out.println("ISBN            : " + ISBN);
    System.out.println("Publisher       : " + publisher);
    System.out.println("Edition         : " + edition);
    System.out.print("Available       : " + (isAvailable ? "Yes" : "No"));
    if (!isAvailable && checkedOutBy != null) {
      System.out.println(" (Checked out by: " + checkedOutBy.name + " (" + checkedOutBy.getClass().getSimpleName() + "))");
    } else {
      System.out.println();
    }
    System.out.println();
  }
}

// ----------------------------------------

class EBook extends LibraryMaterial {
  private String downloadLink;
  private String[] compatibleDevices;

  public EBook(String title, String author, boolean isChildrenFriendly, String downloadLink, String[] compatibleDevices) {
    super(title, author, isChildrenFriendly, "Ebook");
    this.downloadLink = downloadLink;// Pay fine
library.payFine("Ali", 2.5);
    this.compatibleDevices = compatibleDevices;
  }

  @Override
  public boolean isOverdue() {
    return false; // EBooks never overdue
  }

  @Override
  public void renew() {
    System.out.println("E-Books \"" + title+ "\" don't need renewal.");
  }

  public double getFineRate() { return 0.0; }
  public double getMaxFine() { return 0.0; }

  public void display() {
    System.out.println("========= E-BOOK =========");
    System.out.println("Title           : " + title);
    System.out.println("Author          : " + author);
    System.out.println("Download Link   : " + downloadLink);
    System.out.println("Devices         : " + String.join(", ", compatibleDevices));
    System.out.print("Available       : " + (isAvailable ? "Yes" : "No"));
    if (!isAvailable && checkedOutBy != null) {
      System.out.println(" (Checked out by: " + checkedOutBy.name + " (" + checkedOutBy.getClass().getSimpleName() + "))");
    } else {
      System.out.println();
    }
    System.out.println();
  }
}

// ----------------------------------------

class Audiobook extends LibraryMaterial {
  private String narrator;
  private int playbackLength; // minutes

  public Audiobook(String title, String author, boolean isChildrenFriendly, String narrator, int playbackLength) {
    super(title, author, isChildrenFriendly, "Audiobook");
    this.narrator = narrator;
    this.playbackLength = playbackLength;
  }

  public double getFineRate() { return 0.50; }
  public double getMaxFine() { return 15.0; }

  public void display() {
    System.out.println("======= AUDIOBOOK =======");
    System.out.println("Title           : " + title);
    System.out.println("Author          : " + author);
    System.out.println("Narrator        : " + narrator);
    System.out.println("Length          : " + playbackLength + " minutes");
    System.out.print("Available       : " + (isAvailable ? "Yes" : "No"));
    if (!isAvailable && checkedOutBy != null) {
      System.out.println(" (Checked out by: " + checkedOutBy.name + " (" + checkedOutBy.getClass().getSimpleName() + "))");
    } else {
      System.out.println();
    }
    System.out.println();
  }
}

// ----------------------------------------

class DVD extends LibraryMaterial {
  private String director;
  private String[] actors;
  private int runtime;
  private String[] subtitleOptions;

  public DVD(String title, String author, boolean isChildrenFriendly, String director, String[] actors, int runtime, String[] subtitleOptions) {
    super(title, author, isChildrenFriendly, "DVD");
    this.director = director;
    this.actors = actors;
    this.runtime = runtime;
    this.subtitleOptions = subtitleOptions;
  }

  public double getFineRate() { return 1.0; }
  public double getMaxFine() { return 20.0; }

  public void display() {
    System.out.println("========== DVD ==========");
    System.out.println("Title           : " + title);
    System.out.println("Author          : " + author);
    System.out.println("Actors          : " + String.join(", ", actors));
    System.out.println("Director        : " + director);
    System.out.println("Runtime         : " + runtime + " minutes");
    System.out.println("Subtitles       : " + String.join(", ", subtitleOptions));
    System.out.print("Available       : " + (isAvailable ? "Yes" : "No"));
    if (!isAvailable && checkedOutBy != null) {
      System.out.println(" (Checked out by: " + checkedOutBy.name + " (" + checkedOutBy.getClass().getSimpleName() + "))");
    } else {
      System.out.println();
    }
    System.out.println();
  }
}

// ================================
//     Patron Types
// ================================
abstract class Patron {
  protected String name;
  protected int borrowLimit;
  protected int loanDuration;
  protected boolean suspended = false;
  protected double fineBalance = 0.0;

  public Patron(String name) {
    this.name = name;
  }

  public boolean isSuspended() {
    return suspended;
  }
  public void suspendAccount() {
    suspended = true;
  }

  public double getFineBalance() {
    return fineBalance;
  }

  public void addFine(double amount) {
    fineBalance += amount;
  }

  public void payFine(double amount) {
    if (amount > fineBalance) {
      System.out.println(name + " paid more than owed. Setting balance to 0.");
      fineBalance = 0;
    } else {
      fineBalance -= amount;
      System.out.println(name + " paid $" + amount + ". Remaining fine: $" + fineBalance);
    }
  }

  // check to block patrons with excessive fines
  public boolean canBorrow() {
    if (fineBalance > 10) { // imaginary assumed value
      System.out.println("Account blocked due to unpaid fines: " + name);
      return false;
    }
    return true;
  }

  public abstract double getFine(double originalFine);
}

class Student extends Patron {
  public Student(String name) {
    super(name);
    this.borrowLimit = 10;
    this.loanDuration = 21;
  }

  @Override
  public double getFine(double originalFine) {
    return originalFine;
  }
}

class Faculty extends Patron {
  public Faculty(String name) {
    super(name);
    this.borrowLimit = 20;
    this.loanDuration = 42;
  }

  @Override
  public double getFine(double originalFine) {
    return originalFine * 0.5;
  }
}

class SeniorCitizen extends Patron {
  public SeniorCitizen(String name) {
    super(name);
    this.borrowLimit = 15;
    this.loanDuration = 21;
  }

  @Override
  public double getFine(double originalFine) {
    return originalFine * 0.5;
  }
}

class Child extends Patron {
  public Child(String name) {
    super(name);
    this.borrowLimit = 5;
    this.loanDuration = 14;
  }

  @Override
  public double getFine(double originalFine) {
    return 0.0;
  }
}

// ================================
//     Other Classes
// ================================
class LibraryReportSystem implements Reportable {
  private List<LibraryMaterial> materials = new ArrayList<>();
  private Map<String, Integer> borrowCount = new HashMap<>();

  public void addMaterial(LibraryMaterial material) {
    materials.add(material);
    borrowCount.putIfAbsent(material.title, 0);
  }

  public void recordBorrow(String title) {
    borrowCount.put(title, borrowCount.getOrDefault(title, 0) + 1);
  }

  public void generateOverdueReport() {
    System.out.println("\n--- Overdue Report ---");
    for (LibraryMaterial m : materials) {
      if (!m.filterByAvailability() && m.isOverdue()){
        System.out.println("Overdue: " + m.title + " by " + m.author);
      }
    }
  }

  public void generatePopularItemsReport() {
    System.out.println("\n--- Popular Items Report ---");
    borrowCount.entrySet()
      .stream()
      .sorted((a, b) -> b.getValue() - a.getValue())
      .limit(5)
      .forEach(entry -> {
        System.out.println(entry.getKey() + " borrowed " + entry.getValue() + " times");
      });
  }

  public void generateUsageStatistics() {
    System.out.println("\n--- Usage Statistics ---");
    System.out.println("Total items in system: " + materials.size());
    long borrowed = materials.stream().filter(m -> !m.isAvailable).count();
    System.out.println("Currently borrowed: " + borrowed);
    System.out.println("Available: " + (materials.size() - borrowed));
  }
}

class Transaction {
  String materialTitle;
  String patronName;
  String patronType;
  LocalDate date;
  String action; // "Borrowed" or "Returned"

  public Transaction(String materialTitle, String patronName, String patronType, LocalDate date, String action) {
    this.materialTitle = materialTitle;
    this.patronName = patronName;
    this.patronType = patronType;
    this.date = date;
    this.action = action;
  }

  @Override
  public String toString() {
    return "[" + date + "] " + patronName + " (" + patronType + ") " + action + " \"" + materialTitle + "\"";
  }
}

// ================================
//     Library Management Class
// ================================
class LibraryManagement {
  private List<LibraryMaterial> materials = new ArrayList<>();
  private List<Patron> patrons = new ArrayList<>();
  private List<Transaction> transactionHistory = new ArrayList<>();
  private LibraryReportSystem reportSystem = new LibraryReportSystem();

  public void addMaterial(LibraryMaterial m) {
    m.setLibraryReference(this);
    materials.add(m);
    reportSystem.addMaterial(m);
  }
  public void addPatron(Patron p) {
    patrons.add(p);
  }

  public LibraryMaterial findMaterial(String title) {
    for (LibraryMaterial m : materials) {
      if (m.searchByTitle(title)) return m;
    }
    return null;
  }
  public Patron findPatron(String name) {
    for (Patron p : patrons) {
      if (p.name.equalsIgnoreCase(name)) return p;
    }
    return null;
  }
  public void displayAvailableMaterials() {
    for (LibraryMaterial m : materials) {
      if (m.filterByAvailability()) System.out.println(m.title);
    }
  }

  // ======= Fine Payments =======
  public void payFine(String patronName, double amount) {
    Patron patron = findPatron(patronName);
    if (patron == null) {
      System.out.println("Patron not found.");
      return;
    }
    patron.payFine(amount);
  }

  // ======= Transaction History ======
  public void recordTransaction(String title, Patron patron, String action) {
    transactionHistory.add(new Transaction( title, patron.name, patron.getClass().getSimpleName(), LocalDate.now(), action));
    if (action.equals("Borrowed")) {
      reportSystem.recordBorrow(title); // keeping track of borrow for popularity
    }
  }
  public void showTransactionHistory() {
    System.out.println("\n--- Transaction History ---");
    if (transactionHistory.isEmpty()) {
      System.out.println("No transactions recorded yet.");
    } else {
      for (Transaction t : transactionHistory) {
        System.out.println(t);
      }
    }
  }

  // ======= Reservation System =======
  public void placeHold(LibraryMaterial material, Patron patron) {
    if (material != null && patron != null) {
      material.placeHold(patron);
    } else {
      System.out.println("Material or Patron not found.");
    }
  }

  // ======= Overdue Notifications =======
  public void sendOverdueNotifications() {
    System.out.println("\n--- Overdue Notifications ---");

    for (LibraryMaterial m : materials) {
      if (!m.isAvailable && m.dueDate != null && m.checkedOutBy != null) {
        long daysUntilDue = ChronoUnit.DAYS.between(LocalDate.now(), m.dueDate);
        long daysOverdue = ChronoUnit.DAYS.between(m.dueDate, LocalDate.now());
        Patron patron = m.checkedOutBy;

        if (daysUntilDue == 3) {
          System.out.println("Reminder: \"" + m.title + "\" is due in 3 days for " + patron.name);
        } else if (daysOverdue == 1) {
          System.out.println("Overdue Notice: \"" + m.title + "\" is 1 day overdue for " + patron.name);
        } else if (daysOverdue == 14) {
          patron.suspendAccount();
          System.out.println("Account Suspended: " + patron.name + " for 14-day overdue item \"" + m.title + "\".");
        } else if (daysOverdue >= 30) {
          System.out.println("Collections Referral: \"" + m.title + "\" is 30+ days overdue for " + patron.name);
        }
      }
    }
  }


  // ======= Reports =======
  public void generateReports() {
    reportSystem.generateOverdueReport();
    reportSystem.generatePopularItemsReport();
    reportSystem.generateUsageStatistics();
  }

  // ======= Basic Search =======
  public void searchByTitle(String title) {
    System.out.println("Searching by title: " + title);
    for (LibraryMaterial m : materials) {
      if (m.searchByTitle(title)) {
        m.display();
      }
    }
  }
  public void searchByAuthor(String author) {
    System.out.println("Searching by author: " + author);
    for (LibraryMaterial m : materials) {
      if (m.searchByAuthor(author)) m.display();
    }
  }
  public void searchByISBN(String isbn) {
    System.out.println("Searching by ISBN: " + isbn);
    for (LibraryMaterial m : materials) {
      if (m instanceof Book) {
        Book b = (Book) m;
        if (b.searchByISBN(isbn)) {
          b.display();
        }
      }
    }
  }
  // ======= Advanced Filter =======
  // Filter by material type
  public void filterByType(String type) {
    System.out.println("Materials of type: " + type);
    for (LibraryMaterial m : materials) {
      if (m.getMaterialType().equalsIgnoreCase(type)) {
        m.display();
      }
    }
  }
  // Filter by publication year range
  public void filterByYearRange(int start, int end) {
    System.out.println("Materials from " + start + " to " + end);
    for (LibraryMaterial m : materials) {
      if (m.getPublicationYear() >= start && m.getPublicationYear() <= end) {
        m.display();
      }
    }
  }
  // Filter by language
  public void filterByLanguage(String lang) {
    System.out.println("Materials in language: " + lang);
    for (LibraryMaterial m : materials) {
      if (m.getLanguage().equalsIgnoreCase(lang)) {
        m.display();
      }
    }
  }
  // Filter by genre/category
  public void filterByGenre(String genre) {
    System.out.println("Materials in genre: " + genre);
    for (LibraryMaterial m : materials) {
      if (m.getGenre().equalsIgnoreCase(genre)) {
        m.display();
      }
    }
  }

}

// ================================
//     Runner Class
// ================================
public class Question_02 {
  public static void main(String[] args) {
    // Create patrons
    Student student = new Student("Ali");
    Faculty faculty = new Faculty("Dr. Aisha");
    SeniorCitizen senior = new SeniorCitizen("Mr. Ahmed");
    Child child = new Child("Sara");

    // Create materials
    Book book1 = new Book("Java Programming", "Daniel Liang", false, "978-0-13", "Pearson", 11);
    book1.setPublicationYear(2021);
    book1.setLanguage("English");
    book1.setGenre("Education");

    DVD dvd1 = new DVD("History Documentary", "National Geo", false, "John Doe", new String[]{"Actor1", "Actor2"}, 90, new String[]{"English", "Spanish"});
    dvd1.setPublicationYear(2019);
    dvd1.setLanguage("English");
    dvd1.setGenre("Documentary");

    EBook ebook1 = new EBook("OOP Design Patterns", "Gamma", false, "download.com/oop", new String[]{"PC", "Tablet"});
    ebook1.setPublicationYear(2022);
    ebook1.setLanguage("English");
    ebook1.setGenre("Technology");

    Audiobook audio1 = new Audiobook("Sherlock Holmes", "Conan Doyle", true, "David Tennant", 480);
    audio1.setPublicationYear(2020);
    audio1.setLanguage("English");
    audio1.setGenre("Mystery");

    Book childrenBook = new Book("Fairy Tales", "Grimm", true, "111-222", "ClassicPub", 1);
    childrenBook.setPublicationYear(2018);
    childrenBook.setLanguage("English");
    childrenBook.setGenre("Children");

    // Add materials to library system
    LibraryManagement library = new LibraryManagement();
    library.addMaterial(book1);
    library.addMaterial(dvd1);
    library.addMaterial(ebook1);
    library.addMaterial(audio1);
    library.addMaterial(childrenBook);

    // Add patrons
    library.addPatron(student);
    library.addPatron(faculty);
    library.addPatron(senior);
    library.addPatron(child);

    // Borrowing
    System.out.println("\n--- Borrowing Materials ---");
    book1.checkOut(student);
    dvd1.checkOut(faculty);
    ebook1.checkOut(senior);
    audio1.checkOut(senior);
    childrenBook.checkOut(child); // Allowed
    book1.checkOut(child);        // Should be denied (not child-friendly)

    // Simulate Overdue: manually made some items late here
    book1.dueDate = LocalDate.now().minusDays(5);     // 5 days late
    dvd1.dueDate = LocalDate.now().minusDays(3);      // 3 days late
    audio1.dueDate = LocalDate.now().minusDays(7);    // 7 days late

    System.out.println("\n--- Fine Calculation ---");
    System.out.println("Student pays: " + student.getFine(book1.calculateFine(0)));   // $1.25
    System.out.println("Faculty pays: " + faculty.getFine(dvd1.calculateFine(0)));    // $1.5 with 50% off
    System.out.println("Senior pays: " + senior.getFine(audio1.calculateFine(0)));    // $1.75 with 50% off
    System.out.println("Child pays: " + child.getFine(childrenBook.calculateFine(0))); // $0 (always)
    
    // Pay fine
    library.payFine("Ali", 2.5);

    // Renew
    System.out.println("\n--- Renew Materials ---");
    book1.renew();
    audio1.renew();
    ebook1.renew();

    // Place holds on checked-out item
    library.placeHold(book1, faculty);
    library.placeHold(book1, student);
    // Return materials
    System.out.println("\n--- Returning ---");
    book1.checkIn();
    audio1.checkIn();
    childrenBook.checkIn();

    // Search & Filter
    System.out.println("\n--- Searching & Filtering ---");
    library.searchByAuthor("Gamma");
    library.filterByType("Book");
    library.filterByLanguage("English");
    library.filterByYearRange(2019, 2023);
    library.filterByGenre("Mystery");

    // Simulate overdue for notifications
    book1.dueDate = LocalDate.now().plusDays(3);
    dvd1.dueDate = LocalDate.now().minusDays(1);
    audio1.dueDate = LocalDate.now().minusDays(14);
    ebook1.dueDate = LocalDate.now().minusDays(30);
    // Send overdue notifications
    library.sendOverdueNotifications();

    // Generate Reports
    library.generateReports();

    // Show transaction history
    library.showTransactionHistory();
  }
}


