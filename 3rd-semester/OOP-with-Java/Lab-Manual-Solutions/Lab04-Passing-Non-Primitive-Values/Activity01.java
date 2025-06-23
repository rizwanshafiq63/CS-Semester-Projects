// Passing object as parameter and change value of its data member.

class ObjectPass {
  public int value;
  public static void increment(ObjectPass a) {
    a.value++;
  }
}
public class Activity01 {
  public static void main(String[] args) {
    ObjectPass p = new ObjectPass();
    p.value = 5;
    System.out.println("Before calling: " + p.value); // output is 5
    ObjectPass.increment(p);
    System.out.println("After calling: " + p.value); // output is 6
  }
}

