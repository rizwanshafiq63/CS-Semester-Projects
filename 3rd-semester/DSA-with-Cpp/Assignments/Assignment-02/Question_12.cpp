#include <iostream>
using namespace std;

const int MAX_SIZE = 100;

// Custom Queue class
class Queue {
public: 
  struct Pair { int item; int stackID; };
private:
  Pair data[MAX_SIZE];
  int front, rear, size;
public:
  Queue() { front = 0; rear = -1; size = 0; }
  bool isEmpty() { return size == 0; }
  bool isFull() { return size == MAX_SIZE; }
  void enqueue(int item, int stackID) {
    if (isFull()) { cout << "Queue overflow!" << endl; return; }
    rear = (rear + 1) % MAX_SIZE;
    data[rear] = {item, stackID};
    size++;
  }
  Pair dequeue() {
    if (isEmpty()) { cout << "Queue underflow!" << endl; return {-1, 0}; }
    Pair p = data[front];
    front = (front + 1) % MAX_SIZE;
    size--;
    return p;
  }
  void print() {
    if (isEmpty()) { cout << "Queue: Empty" << endl; return; }
    cout << "Queue: ";
    int count = 0, index = front;
    while (count < size) {
      cout << "(" << data[index].item << "," << data[index].stackID << ") ";
      index = (index + 1) % MAX_SIZE;
      count++;
    }
    cout << endl;
  }
};

// Double Stack in Queue class
class DoubleStackInQueue {
private:
  Queue q;
public:
  void pushStack1(int item) {
    q.enqueue(item, 1);
  }

  int popStack1() {
    if (q.isEmpty()) {
      cout << "Queue is empty, cannot pop Stack 1" << endl;
      return -1;
    }
    Queue temp;
    int count1 = 0;
    // Count Stack 1 elements
    while (!q.isEmpty()) {
      Queue::Pair p = q.dequeue(); // Now accessible
      if (p.stackID == 1) count1++;
      temp.enqueue(p.item, p.stackID);
    }
    if (count1 == 0) {
      cout << "Stack 1 is empty" << endl;
      while (!temp.isEmpty()) {
        Queue::Pair p = temp.dequeue();
        q.enqueue(p.item, p.stackID);
      }
      return -1;
    }
    // Move to last Stack 1 element
    for (int i = 0; i < count1 - 1; i++) {
      Queue::Pair p = temp.dequeue();
      if (p.stackID == 1) temp.enqueue(p.item, p.stackID);
      else q.enqueue(p.item, p.stackID);
    }
    Queue::Pair last = temp.dequeue();
    while (!temp.isEmpty()) {
      Queue::Pair p = temp.dequeue();
      q.enqueue(p.item, p.stackID);
    }
    return last.item;
  }

  void pushStack2(int item) {
    q.enqueue(item, 2);
  }

  int popStack2() {
    if (q.isEmpty()) {
      cout << "Queue is empty, cannot pop Stack 2" << endl;
      return -1;
    }
    Queue temp;
    int count2 = 0;
    // Count Stack 2 elements
    while (!q.isEmpty()) {
      Queue::Pair p = q.dequeue();
      if (p.stackID == 2) count2++;
      temp.enqueue(p.item, p.stackID);
    }
    if (count2 == 0) {
      cout << "Stack 2 is empty" << endl;
      while (!temp.isEmpty()) {
        Queue::Pair p = temp.dequeue();
        q.enqueue(p.item, p.stackID);
      }
      return -1;
    }
    // Move to last Stack 2 element
    for (int i = 0; i < count2 - 1; i++) {
      Queue::Pair p = temp.dequeue();
      if (p.stackID == 2) temp.enqueue(p.item, p.stackID);
      else q.enqueue(p.item, p.stackID);
    }
    Queue::Pair last = temp.dequeue();
    while (!temp.isEmpty()) {
      Queue::Pair p = temp.dequeue();
      q.enqueue(p.item, p.stackID);
    }
    return last.item;
  }

  void print() {
    q.print();
  }
};

// Main function to test
int main() {
  DoubleStackInQueue dsq;

  // Test Stack 1
  dsq.pushStack1(1);
  dsq.pushStack1(2);
  dsq.pushStack1(3);
  cout << "After pushing 1, 2, 3 to Stack 1:" << endl;
  dsq.print();

  // Test Stack 2
  dsq.pushStack2(4);
  dsq.pushStack2(5);
  cout << "After pushing 4, 5 to Stack 2:" << endl;
  dsq.print();

  // Pop from Stack 1
  cout << "Popped from Stack 1: " << dsq.popStack1() << endl;
  dsq.print();

  // Pop from Stack 2
  cout << "Popped from Stack 2: " << dsq.popStack2() << endl;
  dsq.print();

  // More pushes and pops
  dsq.pushStack1(6);
  dsq.pushStack2(7);
  cout << "After pushing 6 to Stack 1, 7 to Stack 2:" << endl;
  dsq.print();
  cout << "Popped from Stack 1: " << dsq.popStack1() << endl;
  dsq.print();

  return 0;
}

