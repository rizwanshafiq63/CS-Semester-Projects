/* The program below represents an employee class which has two Date objects as data members. */

class Date {
  private int day;
  private int month;
  private int year;
  public Date(){}
  public Date(int theMonth, int theDay, int theYear) {
    day = checkday(theDay);
    month = checkmonth(theMonth);
    year = theYear;
  }
  private int checkmonth(int testMonth) {
    if (testMonth > 0 && testMonth <= 12) {
      return testMonth;
    } else {
      System.out.println("Invalid month" + testMonth + "set to 1");
      return 1;
    }
  }
  private int checkday(int testDay) {
    int daysofmonth[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}; //No of days in each month
    if (testDay > 0 && testDay <= daysofmonth[month]) {
      return testDay;
    } else if (month == 2 && testDay == 29 && (year % 400 == 0 || (year % 4 == 0 && year % 100 != 0))) { //check if it was a leap year
      return testDay;
    } else {
      System.out.println("Invalid date" + testDay + "set to 1");
    }
    return 1;
  }
  public void setDay(int day) {
    this.day = checkday(day);
  }
  public void setMonth(int month) {
    this.month = checkmonth(month);
  }
  public void setYear(int year) {
    this.year = year;
  }
  public int getDay() {
    return day;
  }
  public int getMonth() {
    return month;
  }
  public int getYear() {
    return year;
  }
  public void display() {
    System.out.println(day + " " + month + " " + year);
  }
}
class employee {
  private String name;
  private String fname;
  private Date birthdate;
  private Date hiredate;
  employee() {
  }
  employee(String name, String fname, Date birthdate, Date hiredate) {
    this.name = name;
    this.fname = fname;
    this.birthdate = birthdate;
    this.hiredate = hiredate;
  }
  public void setname(String name) {
    this.name = name;
  }
  public String getname() {
    return name;
  }
  public void setfname(String fname) {
    this.fname = fname;
  }
  public String getfname() {
    return fname;
  }
  public void setbirthdate(Date birthdate ) {
    this.birthdate = birthdate;
  }
  public Date getbirthdate() {
    return birthdate;
  }
  public void sethiredate(Date hiredate) {
    this.hiredate = hiredate;
  }
  public Date gethiredate() {
    return hiredate;
  }
  public void display() {
    System.out.println("Name: " + name + " Father Name: " + fname);
    birthdate.display();
    hiredate.display();
  }
}
public class Activity02 {
  public static void main(String[] args) {
     Date b = new Date();
    Date h = new Date();
  employee e1 = new employee("xxx", "yyyy",b, h);
    e1.getbirthdate().setDay(1);
    e1.getbirthdate().setMonth(12);
    e1.getbirthdate().setYear(1990);
    e1.gethiredate().setDay(5);
    e1.gethiredate().setMonth(6);
    e1.gethiredate().setYear(2016);
    e1.display();
  }
}

