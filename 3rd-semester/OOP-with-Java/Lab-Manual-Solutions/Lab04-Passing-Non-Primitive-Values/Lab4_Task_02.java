class Book {
  private String author;
  private String[] chapterNames;
  private int chapterCount;

  // Constructors
  public Book() {
    this.author = "Unknown";
    this.chapterNames = new String[0]; // Initialize empty array
    this.chapterCount = 0;
  }
  public Book(String author, String[] chapterNames) {
    if (author == null || author.trim().isEmpty()) {
      throw new IllegalArgumentException("Author name cannot be empty.");
    }
    if (chapterNames.length > 100) {
      throw new IllegalArgumentException("A book can have at most 100 chapters.");
    }
    this.author = author;
    this.chapterNames = new String[chapterNames.length];
    for (int i = 0; i < chapterNames.length; i++) {
      this.chapterNames[i] = chapterNames[i]; 
    }
    this.chapterCount = chapterNames.length;
  }

  // Setter methods
  public void setAuthor(String author) {
    if (author == null || author.trim().isEmpty()) {
      throw new IllegalArgumentException("Author name cannot be empty.");
    }
    this.author = author;
  }

  public void setChapterNames(String[] chapterNames) {
    if (chapterNames.length > 100) {
      throw new IllegalArgumentException("A book can have at most 100 chapters.");
    }
    this.chapterNames = new String[chapterNames.length];
    for (int i = 0; i < chapterNames.length; i++) {
      this.chapterNames[i] = chapterNames[i]; 
    }
    this.chapterCount = chapterNames.length;
  }

  // Getter methods
  public String getAuthor() {
    return author;
  }

  public String[] getChapterNames() {
    String[] copy = new String[chapterNames.length];
    for (int i = 0; i < chapterNames.length; i++) {
      copy[i] = chapterNames[i]; 
    }
    return copy;
  }

  public int getChapterCount() {
    return chapterCount;
  }

  // Compare two books based on the author
  public static boolean compareBooks(Book b1, Book b2) {
    return b1.author.equalsIgnoreCase(b2.author);
  }

  // Compare two books based on the number of chapters
  public static Book compareChapterNames(Book b1, Book b2) {
    if (b1.chapterCount > b2.chapterCount) {
      return b1;
    } else if (b2.chapterCount > b1.chapterCount) {
      return b2;
    } else {
      return null; // when both books have same number of chapters
    }
  }
}

public class Lab4_Task_02 {
  public static void main(String[] args) {
    String[] twistedLoveChapters = { "Enemies to Lovers", "Fake Dating", "Billionaire Romance", "Slow Burn"};
    String[] harryPotterChapters = { "The Boy Who Lived", "The Vanishing Glass", "The Letters from No One", "The Keeper of the Keys" };


    // Creating first book object using no-argument constructor and setters
    Book twistedLove = new Book();
    twistedLove.setAuthor("Ana Huang"); 
    twistedLove.setChapterNames(twistedLoveChapters);

    // Creating second book object using parameterized constructor
    Book harryPotter = new Book("J.K. Rowling", harryPotterChapters);

    // Comparing authors
    if (Book.compareBooks(twistedLove, harryPotter)) {
      System.out.println("Twisted Love and Harry Potter have the same author.");
    } else {
      System.out.println("Twisted Love and Harry Potter have different authors.");
    }

    // Finding which book has more chapters
    Book largerBook = Book.compareChapterNames(twistedLove, harryPotter);
    if (largerBook != null) {
      System.out.println("The book with more chapters is authored by: " + largerBook.getAuthor());
    } else {
      System.out.println("Both books have the same number of chapters.");
    }
  }
}


