#include <cstdarg>
#include <iostream>
using namespace std;

// Activity 01: Implementing an Array based FIFO Queue.
class Que {
private:
  int size; // default capacity of queue
  int *q; // array that holds queue elements
  int front; // index of front of queue
  int rear; // index of rear of queue
public:
  Que() { //default constructor
    size = 10; //default size
    q = new int[size]; // run time size allocation
    front=-1; // initially front and rear are at -1
    rear=-1;
  }
  Que(int x) { //overloaded constructor
    size = x; //user given size
    q = new int[size]; // run time size allocation
    front=-1; // initially front and rear are at -1
    rear=-1;
  }

  bool is_empty() {
    if (rear==-1)
      return true;
    else
      return false;
  }
  bool is_full() {
    if (rear==size-1)
      return true;
    else
      return false ;
  }
  void display() {
    if(is_empty()) {
      cout<<"\n Queue is empty….";
    } else {
      for(int i=front; i<=rear; i++) {
        cout<<"\n Value at index "<<i<< " is: "<<q[i];
      }
    }
  }
  void Enqueue(int x) {
    if (is_full()) {
      cout<<"No space ";
    } else {
      if(is_empty()) {
        front=rear=0;
      } else {
        rear++;
      }
      q[rear] = x;
    }
  }
  int Dequeue() {
    if (is_empty()) {
      cout<<"Queue is already empty";
      return -1;
    } else {
      int returnValue = q[front];
      if(front==rear) {
        front=rear=-1;
      } else {
        front++;
      }
      return returnValue;
    }
  }

  // Acticity 02: Writing the shift left method for dequeue operation.
  int DeQue() {
    int temp;
    if(!is_empty()) {
      temp = q[front];
      if(front == rear)
        front = rear = -1; //make the queue empty
      else
        shift_left(front, rear);
      rear--;
    } else {
      cout<<"\nSorry! Que is Empty ";
      temp = -1;
    }
    return temp;
  }
  void shift_left(int front, int rear) {
    int x=front;
    while(x+1!=rear) {
      q[x]= q[x+1];
    }
  }
};

int main () {
  Que q1;//Default constructor: object of que class with default size
  Que q2(5);//Overloaded constructor: object of que class (q2) with size 5
  Que q3(15);
  q1.Enqueue(5);
  q2.Enqueue(7);
  q3.Enqueue(6);
  int x= q2.Dequeue();
  cout<<"Dequeued element from q3 is: "<<x;
  return 0;
}

