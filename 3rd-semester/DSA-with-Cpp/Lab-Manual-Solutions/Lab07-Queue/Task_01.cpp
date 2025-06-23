/* Implement the methods developed in Activity 1 for Dynmaic Queue i.e. Linked Implementation of the Queue. */

#include <iostream>
using namespace std;

struct Node {
  int data;
  Node* next;
};

class Queue {
private:
  Node* front;
  Node* rear;

public:
  Queue() {
    front = rear = nullptr;
  }

  bool is_empty() {
    return front == nullptr;
  }

  void Enqueue(int value) {
    Node* newNode = new Node{value, nullptr};
    if (rear == nullptr) {
      front = rear = newNode;
    } else {
      rear->next = newNode;
      rear = newNode;
    }
    cout << "Enqueued: " << value << endl;
  }

  int Dequeue() {
    if (is_empty()) {
      cout << "Queue is empty! Cannot dequeue.\n";
      return -1;
    }
    Node* temp = front;
    int removedValue = temp->data;
    front = front->next;
    if (front == nullptr) {
      rear = nullptr;
    }
    delete temp;
    cout << "Dequeued: " << removedValue << endl;
    return removedValue;
  }

  void display() {
    if (is_empty()) {
      cout << "Queue is empty.\n";
      return;
    }
    Node* temp = front;
    cout << "Queue elements: ";
    while (temp != nullptr) {
      cout << temp->data << " ";
      temp = temp->next;
    }
    cout << endl;
  }

  ~Queue() { // Destructor
    while (!is_empty()) {
      Dequeue();
    }
  }
};

int main() {
  Queue q;
  int choice, value;

  while (true) {
    cout << "\n--- Menu ---\n";
    cout << "1. Enqueue (Insert)\n";
    cout << "2. Dequeue (Remove)\n";
    cout << "3. Display Queue\n";
    cout << "4. Exit\n";
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        cout << "Enter value to enqueue: ";
        cin >> value;
        q.Enqueue(value);
        break;

      case 2:
        q.Dequeue();
        break;

      case 3:
        q.display();
        break;

      case 4:
        cout << "Exiting program...\n";
        return 0;

      default:
        cout << "Invalid choice! Please enter a number between 1 and 4.\n";
    }
  }
}

