/* It is required to split a circular queue into two circular queues (say CQueue1 and CQueue 2) so that all the elements in odd positions are in one queue and those in even positions are in another queue as shown in the following figure. Write a C++ program to accomplish this. Assume that queue is maintained in an array. */

#include <iostream>
using namespace std;

const int MAX_SIZE = 100;

class CircularQueue {
private:
  int data[MAX_SIZE];
  int front, rear, size;
public:
  CircularQueue() { front = 0; rear = -1; size = 0; }
  bool isEmpty() { return size == 0; }
  bool isFull() { return size == MAX_SIZE; }
  void enqueue(int item) {
    if (isFull()) { cout << "Queue is full!" << endl; return; }
    rear = (rear + 1) % MAX_SIZE;
    data[rear] = item;
    size++;
  }
  int dequeue() {
    if (isEmpty()) { cout << "Queue is empty!" << endl; return -1; }
    int item = data[front];
    front = (front + 1) % MAX_SIZE;
    size--;
    return item;
  }
  void print() {
    if (isEmpty()) { cout << "Empty"; return; }
    cout << "[ ";
    int count = 0, index = front;
    while (count < size) {
      cout << data[index] << " ";
      index = (index + 1) % MAX_SIZE;
      count++;
    }
    cout << "]";
  }
  int getSize() { return size; }
  int getFront() { return front; }
  int getData(int index) { return data[index]; }
};

void splitCircularQueue(CircularQueue& original, CircularQueue& cqueue1, CircularQueue& cqueue2) {
  if (original.isEmpty()) {
    cout << "Original queue is empty, nothing to split" << endl;
    return;
  }
  int position = 1;
  int index = original.getFront();
  int totalElements = original.getSize();

  for (int i = 0; i < totalElements; i++) {
    int item = original.getData(index);
    if (position % 2 == 0) { // Even position
      cqueue1.enqueue(item);
    } else {
      cqueue2.enqueue(item);
    }
    position++;
    index = (index + 1) % MAX_SIZE;
  }
}

int main() {
  CircularQueue original;
  original.enqueue(10);
  original.enqueue(20);
  original.enqueue(30);
  original.enqueue(40);
  original.enqueue(50);
  original.enqueue(60);

  cout << "Original Queue: ";
  original.print();
  cout << endl;

  CircularQueue cqueue1, cqueue2;
  splitCircularQueue(original, cqueue1, cqueue2);

  cout << "CQueue1 (Even positions): ";
  cqueue1.print();
  cout << endl;

  cout << "CQueue2 (Odd positions): ";
  cqueue2.print();
  cout << endl;

  return 0;
}

