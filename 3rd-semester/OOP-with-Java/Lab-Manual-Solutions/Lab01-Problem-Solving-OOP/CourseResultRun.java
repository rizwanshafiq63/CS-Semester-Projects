class CourseResult {

  public String studentname;
  public String coursename;
  public String grade;

  public void display() {
    System.out.println("Student Name is:" +
      studentname + "\nCourse Name is:" + coursename
      + "\nGrade is:" + grade);
  }
}
public class CourseResultRun {
  public static void main(String[] args) {

    CourseResult c1 = new CourseResult();
    c1.studentname = "Rehmooz";
    c1.coursename = "OOP";
    c1.grade = "A";
    c1.display();
    CourseResult c2 = new CourseResult();
    c2.studentname = "Parnia";
    c2.coursename = "ICT";
    c2.grade = "B+";
    c2.display();
  }
}

