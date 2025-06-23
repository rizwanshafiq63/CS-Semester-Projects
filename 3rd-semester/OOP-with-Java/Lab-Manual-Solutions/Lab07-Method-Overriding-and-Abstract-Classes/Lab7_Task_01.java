/* Create a class named Movie that can be used with your video rental business. The Movie class should track the Motion Picture Association of America (MPAA) rating (e.g., Rated G, PG-13, R), ID Number, and movie title with appropriate accessor and mutator methods. Also create an equals() method that overrides Object’s equals() method, where two movies are equal if their ID number is identical. Next, create three additional classes named Action , Comedy , and Drama that are derived from Movie. Finally, create an overridden method named calcLateFees that takes as input the number of days a movie is late and returns the late fee for that movie. The default late fee is $2/day. Action movies have a late fee of $3/day, comedies are $2.50/day, and dramas are $2/day. Test your classes from a main method. */

// Base class Movie
class Movie {
  private String title;
  private String mpaaRating;
  private int idNumber;

  public Movie(String title, String mpaaRating, int idNumber) {
    this.title = title;
    this.mpaaRating = mpaaRating;
    this.idNumber = idNumber;
  }

  //Getters and Setters
  public String getTitle() {
    return title;
  }
  public String getMpaaRating() {
    return mpaaRating;
  }   
  public int getIdNumber() {
    return idNumber;
  }
  public void setTitle(String title) {
    this.title = title;
  }   
  public void setMpaaRating(String mpaaRating) {
    this.mpaaRating = mpaaRating;
  }
  public void setIdNumber(int idNumber) {
    this.idNumber = idNumber;
  }

  public boolean equals(Movie obj) {
    return this.idNumber == obj.idNumber;
  }

  public double calcLateFees(int daysLate) {
    return daysLate * 2.0; // Default late fee
  }
}

// Action movie class
class Action extends Movie {
  public Action(String title, String mpaaRating, int idNumber) {
    super(title, mpaaRating, idNumber);
  }

  @Override
  public double calcLateFees(int daysLate) {
    return daysLate * 3.0; // $3 per day
  }
}

// Comedy movie class
class Comedy extends Movie {
  public Comedy(String title, String mpaaRating, int idNumber) {
    super(title, mpaaRating, idNumber);
  }

  @Override
  public double calcLateFees(int daysLate) {
    return daysLate * 2.5; // $2.50 per day
  }
}

// Drama movie class
class Drama extends Movie {
  public Drama(String title, String mpaaRating, int idNumber) {
    super(title, mpaaRating, idNumber);
  }

  @Override
  public double calcLateFees(int daysLate) {
    return daysLate * 2.0; // $2 per day
  }
}

// Testing the classes
public class Lab7_Task_01 {
  public static void main(String[] args) {
    Movie actionMovie = new Action("Mad Max", "R", 101);
    Movie comedyMovie = new Comedy("The Mask", "PG-13", 102);
    Movie dramaMovie = new Drama("The Godfather", "R", 103);

    System.out.println("Late fee for action movie (5 days late): $" + actionMovie.calcLateFees(5));
    System.out.println("Late fee for comedy movie (5 days late): $" + comedyMovie.calcLateFees(5));
    System.out.println("Late fee for drama movie (5 days late): $" + dramaMovie.calcLateFees(5));

    // Testing equality
    Movie anotherActionMovie = new Action("Mad Max: Fury Road", "R", 101);
    System.out.println("Are the two action movies equal? " + actionMovie.equals(anotherActionMovie));
  }
}

