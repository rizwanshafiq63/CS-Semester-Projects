/* An Example that shows How to create your own interface and implement it in abstract class. */

interface I1 {
  void methodI1(); // public static by default
}

interface I2 extends I1 {
  void methodI2(); // public static by default
}

class A1 {
  public String methodA1() {
    String strA1 = "I am in methodA1 of class A1";
    return strA1;
  }
  public String toString() {
    return "toString() method of class A1";
  }
}

class B1 extends A1 implements I2 {
  public void methodI1() {
    System.out.println("I am in methodI1 of class B1");
  }
  public void methodI2() {
    System.out.println("I am in methodI2 of class B1");
  }
}

class C1 implements I2 {
  public void methodI1() {
    System.out.println("I am in methodI1 of class C1");
  }
  public void methodI2() {
    System.out.println("I am in methodI2 of class C1");
  }
}

// Note that the class is declared as abstract as it does not satisfy the interface contract
abstract class D1 implements I2 {
  public void methodI1() {}
  // This class does not implement methodI2() hence declared abstract.
}

// Runner: InterFaceEx
public class Activity02 {
  public static void main(String[] args) {
    I1 i1 = new B1();
    i1.methodI1(); // OK as methodI1 is present in B1
    // i1.methodI2(); Compilation error as methodI2 not present in I1
    // Casting to convert the type of the reference from type I1 to typeI2 
  ((I2) i1).methodI2();
    I2 i2 = new B1();
    i2.methodI1(); // OK
    i2.methodI2(); // OK
    // Does not Compile as methodA1() not present in interface reference I1
    // String var = i1.methodA1();
    // Hence I1 requires a cast to invoke methodA1
    String var2 = ((A1) i1).methodA1(); System.out.println("var2 : " + var2);
    String var3 = ((B1) i1).methodA1(); System.out.println("var3 : " + var3);
    String var4 = i1.toString();
    System.out.println("var4 : " + var4);
    String var5 = i2.toString();
    System.out.println("var5 : " + var5);
    I1 i3 = new C1();
    String var6 = i3.toString();
    System.out.println("var6 : " + var6); // It prints the Object toString() method
    Object o1 = new B1();
    // o1.methodI1(); does not compile as Object class does not define
    // methodI1()
    // To solve the probelm we need to downcast o1 reference. We can do it
    // in the following 4 ways
  ((I1) o1).methodI1(); // 1
  ((I2) o1).methodI1(); // 2
  ((B1) o1).methodI1(); // 3
  /*
  *
  * B1 does not have any relationship with C1 except they are "siblings".
  *
  * Well, you can't cast siblings into one another.
  *
  */
  // ((C1)o1).methodI1(); Produces a ClassCastException
  }
}


