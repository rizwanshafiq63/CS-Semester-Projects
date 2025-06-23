// Best Introduction to circular queue (Slides Method)

#include <iostream>
using namespace std;
template <class T> // Its beneficial to use template class as we can use the same class for different data types

class Q {
private:
  T *p; // Pointer to the array
  int Front;
  int Rear;
  int QueueSize;

public:
  Q() { // Default constructor
    QueueSize=5;
    p=new T[QueueSize];
    Front=Rear=-1;
  }
  Q(int s) { // Parameterized constructor
    QueueSize=s;
    p=new T[QueueSize];
    Front=Rear=-1;
  }

  bool IsEmpty() {
    if (Front==-1) 
      return true;
    else 
      return false;
  }
  bool IsFull() {
    if (((Rear+1)%QueueSize)==Front)
      return true;
    else
      return false;
  }

  void Enqueue(T x) {
    if (IsFull()) {
      cout<<"Overflow"<<endl;
    } else {
      if (IsEmpty()) {
        Front=Rear=0;
      } else {
        Rear=(Rear+1)%QueueSize;
      }
      p[Rear]=x;
    }
  }

  T Dequeue( ) {
    if (IsEmpty()) {
      cout<<"Underflow"<<endl;
    // Return appropriate default values
    if constexpr (is_same<T, int>::value) return -1;
    if constexpr (is_same<T, char>::value) return '0';
    if constexpr (is_same<T, string>::value) return string("0");  // Use string constructor
    // if constexpr ensures the condition is checked at compile-time, avoiding unnecessary runtime overhead.
    return T();  // Return default constructed value for other types
    } else {
      T ReturnValue=p[Front];
      if (Front==Rear)    //only one element in the queue
        Front=Rear=-1;
      else
        Front=(Front+1) % QueueSize;
      return ReturnValue;
    }
  }

  void Display() {
    if (IsEmpty()) {
      cout<<"Queue is Empty"<<endl;
    } else {
      int i=Front;
      do {
        cout<<p[i]<<" ";
        i=(i+1)%QueueSize;
      } while (i!=Rear+1%QueueSize);
      cout<<p[Rear]<<endl;
    }
  }
};

int main() {
  Q <int> q1;
  Q <char> q2;
  Q <string> q3;
  q1.Enqueue(4);
  q1.Enqueue(7);
  q1.Enqueue(9);
  cout<<"\n Dequeued value is: "<<q1.Dequeue();
  q2.Enqueue('A');
  q2.Enqueue('B');
  q2.Enqueue('C');
  cout<<"\n Dequeued value is: "<<q2.Dequeue();
  q3.Enqueue("I");
  q3.Enqueue("Love");
  q3.Enqueue("Programming");
  cout<<"\n Dequeued value is: "<<q3.Dequeue();
  cout<<"\n Dequeued value is: "<<q3.Dequeue();
  cout<<"\n Dequeued value is: "<<q3.Dequeue();
  return 0;
}

// Output
// Dequeued value is: 4
// Dequeued value is: A
// Dequeued value is: I
// Dequeued value is: Love
// Dequeued value is: Programming

// Time Complexity: O(1)
// Space Complexity: O(n)
// Where n is the size of the queue.

