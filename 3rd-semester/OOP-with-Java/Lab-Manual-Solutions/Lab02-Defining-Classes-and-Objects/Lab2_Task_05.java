class Time {
  // Data members
  private int hr;
  private int min;
  private int sec;

  // Constructors
  public Time() {
    this.hr = 0; 
    this.min = 0; 
    this.sec = 0; 
  }
  public Time(int hr, int min, int sec) {
    // Checks to ensure valid time
    if (hr >= 0 && hr < 24) {
      this.hr = hr;
    } else { // Display 0 if invalid
      this.hr = 0; 
    }

    if (min >= 0 && min < 60) {
      this.min = min;
    } else {
      this.min = 0; 
    }

    if (sec >= 0 && sec < 60) {
      this.sec = sec;
    } else {
      this.sec = 0; 
    }
  }

  // Display Method
  public void display() {
    System.out.println("Time: " + hr + " hours " + min + " minutes " + sec + " seconds");
  }
}

public class Lab2_Task_05{
  public static void main(String[] args) {
    // Default case (No-Argument)
    Time time1 = new Time();
    time1.display(); 

    // Valid time case
    Time time2 = new Time(14, 30, 45);
    time2.display(); 

    // Invalid time case
    Time time3 = new Time(25, 61, 70);
    time3.display(); 
  }
}

