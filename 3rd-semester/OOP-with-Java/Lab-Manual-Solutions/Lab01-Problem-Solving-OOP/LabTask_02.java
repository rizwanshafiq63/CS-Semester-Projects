class Time {

  int hours;
  int minutes;
  int seconds;

  public void display() {
    System.out.println("Time: " + hours + ":" + minutes + ":" + seconds);
  }
}

public class LabTask_02 {
  public static void main(String[] args) {

    Time time1 = new Time();
    time1.hours = 10;
    time1.minutes = 30;
    time1.seconds = 45;

    time1.display();
  }
}

