/* Below is a code skeleton for an interface called “Enumeration” and a class called "NameCollection". Enumeration provides an interface to sequentially iterate through some type of collection. In this case, the collection will be the class NameCollection that simply stores a collection of names using an array of strings.
interface Enumeration {
  public boolean hasNext(int index); // return true if a value exists in the next index
  public Object getNext(int index); // returns the next element in the collection as an Object
}
//NameCollection implements a collection of names using a simple array.
class NameCollection {
  String[] names = new String[100];
}
Create constructor and abstract methods of interface in the class NameCollection. Then write a main method that creates a NamesCollection object with a sample array of strings, and then iterates through the enumeration outputting each name using the getNext() method. */

interface Enumeration {
  public boolean hasNext(int index);
  public Object getNext(int index);  
}

class NameCollection implements Enumeration {
  String[] names = new String[100];
  private int size = 0; // Number of names added

  // Constructor 
  public NameCollection(String[] inputNames) {
    for (int i = 0; i < inputNames.length && i < names.length; i++) {
      names[i] = inputNames[i];
      size++;
    }
  }

  // Return true if next index contains a name
  @Override
  public boolean hasNext(int index) {
    return index + 1 < size;
  }

  // Return name at next index
  @Override
  public Object getNext(int index) {
    if (hasNext(index)) {
      return names[index + 1];
    }
    return null;
  }

  // Return size for iteration convenience
  public int getSize() {
    return size;
  }

}

public class Lab9_Task_04 {
  public static void main(String[] args) {
    String[] sampleNames = {"Ali", "Sara", "Usman", "Ayesha"};
    NameCollection collection = new NameCollection(sampleNames);

    System.out.println("Iterating through names using Enumeration methods:");
    for (int i = -1; i < collection.getSize() - 1; i++) {
      if (collection.hasNext(i)) {
        System.out.println(collection.getNext(i));
      }
    }
  }
}

