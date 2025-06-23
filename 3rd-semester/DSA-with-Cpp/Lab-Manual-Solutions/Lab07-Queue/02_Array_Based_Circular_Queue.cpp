/* Implement an Array based circular Queue that is generic in nature (use template classes), apply proper checks of Queue Full and Queue Empty before Enque and DeQue operations. */

#include <iostream>
using namespace std;
template <class T> // Its beneficial to use template class as we can use the same class for different data types

class Q {
private:
  T Data[10]; // Array of 10 elements
  int front;
  int rear;
  int count; // To keep track of the number of elements in the Q

public:
  Q() { front = rear = count =0;}
  bool isEmpty() { return (count == 0); }
  bool isFull() { return (count == 10); }
  void enQue(T);
  T deQue();
  void display();
};

template <class T>
void Q <T> :: enQue(T x) {
  if (!isFull()) {
    Data[rear] = x;
    rear++;
    rear = rear % 10;
    count++;
  } else {
    cout<<"\nSorry Q is Full ";
  }
}
template <class T>
T Q<T> ::deQue() {
  T temp;
  if(!isEmpty()) {
    temp = Data[front];
    front++;
    front = front%10;
    count--;
  } else {
    cout<<"\nSorry Q is Empty ";
    temp = -1;
  }
  return temp;
}

template <class T>
void Q<T> ::display() {
  int i;
  if(!isEmpty()) {
    for(i=front; i<=rear; i++) {
      cout<<Data[i]<<" ";
    }
  } else {
    cout<<"\nSorry Q is Empty ";
  }
}

int main() {
  Q <int> q1;
  Q <char> q2;
  Q <string> q3;
  q1.enQue(4);
  q1.enQue(7);
  q1.enQue(9);
  cout<<"\n Dequeued value is: "<<q1.deQue();
  q2.enQue('A');
  q2.enQue('B');
  q2.enQue('C');
  cout<<"\n Dequeued value is: "<<q2.deQue();
  q3.enQue("I");
  q3.enQue("Love");
  q3.enQue("Programming");
  cout<<"\n Dequeued value is: "<<q3.deQue();
  cout<<"\n Dequeued value is: "<<q3.deQue();
  cout<<"\n Dequeued value is: "<<q3.deQue();
}

