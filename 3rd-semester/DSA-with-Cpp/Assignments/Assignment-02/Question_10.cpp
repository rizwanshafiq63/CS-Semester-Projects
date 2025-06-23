/* i. How would you implement a queue of stacks?
ii. How would you implement a stack of queues?
iii. How would you implement a queue of queues?
  a. Draw a diagram of how each of these data structures might look.
  b. Write algorithms/ routines to implement the appropriate operations of each of these data structures */

#include <iostream>
using namespace std;

const int MAX_SIZE = 100; // Max size for stacks and queues

// Custom Stack class (array-based)
class Stack {
private:
  int data[MAX_SIZE];
  int top;
public:
  Stack() { top = -1; }
  bool isEmpty() { return top == -1; }
  bool isFull() { return top == MAX_SIZE - 1; }
  void push(int item) {
    if (isFull()) { cout << "Stack overflow!" << endl; return; }
    data[++top] = item;
  }
  int pop() {
    if (isEmpty()) { cout << "Stack underflow!" << endl; return -1; }
    return data[top--];
  }
  int peek() {
    if (isEmpty()) return -1;
    return data[top];
  }
  void print() { 
    if (isEmpty()) { cout << "Empty"; return; }
    for (int i = top; i >= 0; i--) {
      cout << data[i] << " ";
    }
  }
};

// Custom Queue class (array-based with circular indices)
class Queue {
private:
  int data[MAX_SIZE];
  int front, rear, size;
public:
  Queue() { front = 0; rear = -1; size = 0; }
  bool isEmpty() { return size == 0; }
  bool isFull() { return size == MAX_SIZE; }
  void enqueue(int item) {
    if (isFull()) { cout << "Queue overflow!" << endl; return; }
    rear = (rear + 1) % MAX_SIZE;
    data[rear] = item;
    size++;
  }
  int dequeue() {
    if (isEmpty()) { cout << "Queue underflow!" << endl; return -1; }
    int item = data[front];
    front = (front + 1) % MAX_SIZE;
    size--;
    return item;
  }
  int getFront() {
    if (isEmpty()) return -1;
    return data[front];
  }
  void print() { 
    if (isEmpty()) { cout << "Empty"; return; }
    int count = 0, index = front;
    while (count < size) {
      cout << data[index] << " ";
      index = (index + 1) % MAX_SIZE;
      count++;
    }
  }
};

// i. Queue of Stacks
class QueueOfStacks {
private:
  Stack data[MAX_SIZE]; // Array of stacks
  int front, rear, size;
public:
  QueueOfStacks() { front = 0; rear = -1; size = 0; }
  void enqueue(Stack s) {
    if (size == MAX_SIZE) { cout << "Queue of Stacks full!" << endl; return; }
    rear = (rear + 1) % MAX_SIZE;
    data[rear] = s;
    size++;
  }
  Stack dequeue() {
    if (size == 0) { cout << "Queue of Stacks empty!" << endl; return Stack(); }
    Stack s = data[front];
    front = (front + 1) % MAX_SIZE;
    size--;
    return s;
  }
  void pushToFront(int item) {
    if (size == 0) return;
    data[front].push(item);
  }
  void print() {
    if (size == 0) { cout << "Queue of Stacks empty" << endl; return; }
    int count = 0, index = front;
    while (count < size) {
      cout << "[ ";
      data[index].print();
      cout << "] ";
      index = (index + 1) % MAX_SIZE;
      count++;
    }
    cout << endl;
  }
};

// ii. Stack of Queues
class StackOfQueues {
private:
  Queue data[MAX_SIZE]; // Array of queues
  int top;
public:
  StackOfQueues() { top = -1; }
  void push(Queue q) {
    if (top == MAX_SIZE - 1) { cout << "Stack of Queues full!" << endl; return; }
    data[++top] = q;
  }
  Queue pop() {
    if (top == -1) { cout << "Stack of Queues empty!" << endl; return Queue(); }
    return data[top--];
  }
  void enqueueToTop(int item) {
    if (top == -1) return;
    data[top].enqueue(item);
  }
  void print() {
    if (top == -1) { cout << "Stack of Queues empty" << endl; return; }
    for (int i = top; i >= 0; i--) {
      cout << "[ ";
      data[i].print();
      cout << "] ";
    }
    cout << endl;
  }
};

// iii. Queue of Queues
class QueueOfQueues {
private:
  Queue data[MAX_SIZE]; // Array of queues
  int front, rear, size;
public:
  QueueOfQueues() { front = 0; rear = -1; size = 0; }
  void enqueue(Queue q) {
    if (size == MAX_SIZE) { cout << "Queue of Queues full!" << endl; return; }
    rear = (rear + 1) % MAX_SIZE;
    data[rear] = q;
    size++;
  }
  Queue dequeue() {
    if (size == 0) { cout << "Queue of Queues empty!" << endl; return Queue(); }
    Queue q = data[front];
    front = (front + 1) % MAX_SIZE;
    size--;
    return q;
  }
  void enqueueToFront(int item) {
    if (size == 0) return;
    data[front].enqueue(item);
  }
  void print() {
    if (size == 0) { cout << "Queue of Queues empty" << endl; return; }
    int count = 0, index = front;
    while (count < size) {
      cout << "[ ";
      data[index].print();
      cout << "] ";
      index = (index + 1) % MAX_SIZE;
      count++;
    }
    cout << endl;
  }
};

// Main function to test
int main() {
  // Test Queue of Stacks
  QueueOfStacks qos;
  Stack s1, s2;
  s1.push(1); s1.push(2); // [2 1]
  s2.push(3);             // [3]
  qos.enqueue(s1);
  qos.enqueue(s2);
  cout << "Queue of Stacks: ";
  qos.print();
  qos.pushToFront(4);
  cout << "After push to front: ";
  qos.print();

  // Test Stack of Queues
  StackOfQueues soq;
  Queue q1, q2;
  q1.enqueue(1); q1.enqueue(2); // [1 2]
  q2.enqueue(3);                // [3]
  soq.push(q1);
  soq.push(q2);
  cout << "\nStack of Queues: ";
  soq.print();
  soq.enqueueToTop(4);
  cout << "After enqueue to top: ";
  soq.print();

  // Test Queue of Queues
  QueueOfQueues qoq;
  Queue q3, q4;
  q3.enqueue(1); q3.enqueue(2); // [1 2]
  q4.enqueue(3);                // [3]
  qoq.enqueue(q3);
  qoq.enqueue(q4);
  cout << "\nQueue of Queues: ";
  qoq.print();
  qoq.enqueueToFront(4);
  cout << "After enqueue to front: ";
  qoq.print();

  return 0;
}

