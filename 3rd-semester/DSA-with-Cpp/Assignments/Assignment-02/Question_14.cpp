/* Can a queue be represented by a circular linked list with only one pointer pointing to the tail of the queue. Write C++ functions for add and delete operations on such a queue. */

#include <iostream>
using namespace std;

class Node {
public:
  int data;
  Node* next;
  Node(int value) { data = value; next = nullptr; }
};

class Queue {
private:
  Node* tail;
public:
  Queue() { tail = nullptr; }

  void enqueue(int item) {
    Node* newNode = new Node(item);
    if (!tail) { // Queue is empty
      tail = newNode;
      tail->next = tail;
    } else {
      newNode->next = tail->next;
      tail->next = newNode;
      tail = newNode;
    }
  }

  int dequeue() {
    if (!tail) {
      cout << "Queue is empty" << endl;
      return -1;
    }
    if (tail->next == tail) {
      int item = tail->data;
      delete tail;
      tail = nullptr;
      return item;
    } else {
      Node* front = tail->next;
      int item = front->data;
      tail->next = front->next;
      delete front;
      return item;
    }
  }

  void print() {
    if (!tail) {
      cout << "Queue: Empty" << endl;
      return;
    }
    cout << "Queue: ";
    Node* current = tail->next;
    do {
      cout << current->data << " ";
      current = current->next;
    } while (current != tail->next);
    cout << endl;
  }
};

int main() {
  Queue q;
  q.enqueue(10); q.enqueue(20); q.enqueue(30);
  cout << "After adding 10, 20, 30:" << endl;
  q.print();
  cout << "Deleted: " << q.dequeue() << endl;
  q.print();
  cout << "Deleted: " << q.dequeue() << endl;
  q.print();
  return 0;
}

