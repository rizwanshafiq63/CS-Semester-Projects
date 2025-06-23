/* This example will explain the method to specify the derived class. It explains the syntax for writing the constructor of derived class. */

class person {
  protected String name;
  protected String id;
  protected String phone;

  public person() {
    System.out.println("No-Argument constructor of Parent class(person)");
    name = null; 
    id = null;
    phone = null;
  }
  public person(String a , String b , String c) { 
    System.out.println("Argument constructor of Parent class(person)");
    name = a;
    id = b;
    phone = c;
  }

  public void setName(String a){ name = a ;}
  public void setId(String j){id = j ;}
  public void setPhone(String a) { phone = a ;}

  public String getName() {return name ;}
  public String getid() {return id ;}
  public String getPhone() {return phone ;}
  public void display( ) {
    System.out.println("display of Parent class");
    System.out.println("Name : " +name+ "\nID : " +id+ "\nPhone : " +phone ) ;
  }
}

class student extends person {
  private String rollNo;
  private int marks;

  public student() {
    super();
    System.out.println("No-Argument Constructor of Child class(student)");
    rollNo = null;
    marks = 0;
  }
  public student(String name, String id, String phone, String rollNo, int marks) {
    super(name,id,phone);
    System.out.println("Argument Constructor of Child class(person)");
    this.rollNo = rollNo; 
    this.marks = checkMarks(marks);
  }

  public void setRollNo(String a){ rollNo = a;}
  public void setMarks(int a ){ marks = checkMarks(a);}

  private int checkMarks(int marks) {
    if (marks > 0 && marks < 100) {
      return marks;
    } else {
      return 0;
    }
  }

  public String getRollNo() { return rollNo;}
  public int getMarks() {return marks;}
  
  public void display( ) {
    super.display();
    System.out.println("Method Overloading: Display of derived class");
    System.out.println("Roll # : " +rollNo+ "\nMarks : " +marks);
  }
}

public class Activity01 {
  public static void main(String []args) {
    student s1 = new student ();
    student s = new student ("Rizwan", "s-09", "0309", "SP24-BCS-069",500);
    s.setPhone("030932488"); //setting variables of parent class using the child class
    s.display();
  } 
}

