
// Base class: Student
abstract class Student {
  protected String name;
  protected String studentId;

  public Student(String name, String studentId) {
    this.name = name;
    this.studentId = studentId;
  }

  public String getName() {
    return name;
  }

  abstract public double calculateGrade();
}

// Subclasses of Student class
class UndergraduateStudent extends Student {
  private double[] quizScores;

  public UndergraduateStudent(String name, String studentId, double[] quizScores) {
    super(name, studentId);
    if (areScoresValid(quizScores)) {
      this.quizScores = quizScores;
    } else {
      System.out.println("Error: Invalid quiz scores provided for student " + name + ". Scores must be > 0 and <= 100.");
      this.quizScores = new double[0]; 
    }
  }

  private boolean areScoresValid(double[] scores) {
    for (double score : scores) {
      if (score <= 0 || score > 100)
        return false;
    }
    return true;
  }

  @Override
  public double calculateGrade() {
    if (quizScores.length == 0) {
      System.out.println("No valid quiz scores available for " + name + ".");
      return 0.0;
    }
    double total = 0;
    for (double score : quizScores) {
      total += score;
    }
    return total / quizScores.length;
  }
}

class GraduateStudent extends Student {
  private double thesisScore;

  public GraduateStudent(String name, String studentId, double thesisScore) {
    super(name, studentId);
    this.thesisScore = thesisScore;
  }

  @Override
  public double calculateGrade() {
    if (thesisScore >= 85) return 4.0;
    else if (thesisScore >= 75) return 3.5;
    else if (thesisScore >= 65) return 3.0;
    else return 2.5;
    // return thesisScore; // Simplified
  }
}

class ExchangeStudent extends Student {
  private boolean passed;

  public ExchangeStudent(String name, String studentId, boolean passed) {
    super(name, studentId);
    this.passed = passed;
  }

  @Override
  public double calculateGrade() {
    return passed ? 1.0 : 0.0; // 1.0 = Pass, 0.0 = Fail
  }
}

// Base class: Material
abstract class Material {
  protected String title;

  public Material(String title) {
    this.title = title;
  }

  abstract public void displayContent();
}

// Subclasses of Material class
class Textbook extends Material {
  public Textbook(String title) {
    super(title);
  }

  @Override
  public void displayContent() {
    System.out.println("Textbook: " + title);
  }
}

class VideoLecture extends Material {
  public VideoLecture(String title) {
    super(title);
  }

  @Override
  public void displayContent() {
    System.out.println("Streaming video lecture: " + title);
  }
}

class Assignment extends Material {
  String deadline;

  public Assignment(String title, String deadline) {
    super(title);
    this.deadline = deadline;
  }

  @Override
  public void displayContent() {
    System.out.println("Assignment: " + title + " | Deadline: " + deadline);
  }
}

// Class representing a module within a course
class Module {
  private String title;
  private Material[] materials;
  private int materialCount;

  public Module(String title) {
    this.title = title;
    this.materials = new Material[10]; // assuming max 10 materials per module
    this.materialCount = 0;
  }

  public void addMaterial(Material material) {
    if (materialCount < materials.length) {
      materials[materialCount++] = material;
    }
  }

  public void displayAllContent() {
    System.out.println("\nModule: " + title);
    System.out.println("-> Materials: ");
    for (int i = 0; i < materialCount; i++) {
      System.out.print("    " + (i + 1) + ". ");
      materials[i].displayContent();
    }
  }
}

// Class representing a course
class Course {
  private String name;
  private Module[] modules;
  private int moduleCount;
  private Enrollment[] enrollments;
  private int enrollmentCount;

  public Course(String name) {
    this.name = name;
    this.modules = new Module[5]; // assuming max 5 modules per course
    this.moduleCount = 0;
    this.enrollments = new Enrollment[50]; // assuming max 50 students per course
    this.enrollmentCount = 0;
  }

  public void addModule(Module m) {
    if (moduleCount < modules.length) {
      modules[moduleCount++] = m;
    }
  }

  public void enrollStudent(Student student) {
    if (enrollmentCount < enrollments.length) {
      enrollments[enrollmentCount++] = new Enrollment(student, this);
    }
  }

  public void showAllEnrolledStudents() {
    System.out.println("\n====================================");
    System.out.println("\tEnrolled Students    \nCourse: " + name);
    System.out.println("====================================");
    for (int i = 0; i < enrollmentCount; i++) {
      System.out.println(" " + (i + 1) + ". " +  enrollments[i].getStudent().getName());
    }
  }

  public void calculateGradesForAll() {
    System.out.println("\n====================================");
    System.out.println("\tGrade Calculation Report");
    System.out.println("====================================");
    for (int i = 0; i < enrollmentCount; i++) {
      Student s = enrollments[i].getStudent();
      double grade = s.calculateGrade();
      String gradeText;
      if (s instanceof ExchangeStudent) {
        gradeText = (grade == 1.0) ? "Grade: Pass" : "Grade: Fail";
      } else if (s instanceof GraduateStudent) {
        gradeText = String.format("Grade(CGPA): %.2f", grade);
      } else if (s instanceof UndergraduateStudent) {
        gradeText = String.format("Grade(Percentage): %.2f", grade);
      } else {
        gradeText = "Grade: Unknown Type";
      }
      System.out.println(" " + (i + 1) + ". " + s.getName() + " [" + s.getClass().getSimpleName() + "] -> " + gradeText);
    }
  }

  public void displayCourseContent() {
    System.out.println("\n====================================");
    System.out.println("\tContent Overview    \nCourse: " + name);
    System.out.println("====================================");
    for (int i = 0; i < moduleCount; i++) {
      modules[i].displayAllContent();
    }
  }
}

// Class representing enrollment of a student in a course
class Enrollment {
  private Student student;
  private Course course;
  private String enrollmentDate;
  private double grade;

  public Enrollment(Student student, Course course) {
    this.student = student;
    this.course = course;
    this.enrollmentDate = java.time.LocalDate.now().toString();
    this.grade = 0.0;
  }

  public Student getStudent() {
    return student;
  }

  public Course getCourse() {
    return course;
  }

  public String getEnrollmentDate() {
    return enrollmentDate;
  }

  public double getGrade() {
    return grade;
  }

  public void setGrade(double grade) {
    this.grade = grade;
  }
}

// Main class to test the system
public class Question_01 {
  public static void main(String[] args) {
    Course oop = new Course("Object Oriented Programming");

    Module mod1 = new Module("Inheritance");
    mod1.addMaterial(new VideoLecture("Intro to Inheritance"));
    mod1.addMaterial(new Assignment("Inheritance Task", "2025-05-10"));

    Module mod2 = new Module("Polymorphism");
    mod2.addMaterial(new Textbook("Polymorphism Explained"));

    oop.addModule(mod1);
    oop.addModule(mod2);

    Student grad = new GraduateStudent("Ali", "G001", 88.5);
    Student exch = new ExchangeStudent("Sara", "E001", true);

    double[] quizMarks = {80.0, 85.0, 78.0};
    Student undergrad = new UndergraduateStudent("Ahmed", "U001", quizMarks);

    oop.enrollStudent(grad);
    oop.enrollStudent(exch);
    oop.enrollStudent(undergrad);

    // Displaying Output
    oop.displayCourseContent();
    oop.showAllEnrolledStudents();
    oop.calculateGradesForAll();
  }
}



