// Implement the Deque in Linked List

#include <iostream>
using namespace std;

struct Node { // Used Doubly Linked List
  int data;
  Node* next;
  Node* prev;
};

class Deque {
private:
  Node* front;
  Node* rear;

public:
  Deque() {
    front = rear = nullptr;
  }

  bool is_empty() {
    return front == nullptr;
  }

  void insert_front(int value) {
    Node* newNode = new Node{value, front, nullptr};
    if (is_empty()) {
      front = rear = newNode;
    } else {
      front->prev = newNode;
      front = newNode;
    }
    cout << "Inserted at Front: " << value << endl;
  }

  void insert_rear(int value) {
    Node* newNode = new Node{value, nullptr, rear};
    if (is_empty()) {
      front = rear = newNode;
    } else {
      rear->next = newNode;
      rear = newNode;
    }
    cout << "Inserted at Rear: " << value << endl;
  }

  int delete_front() {
    if (is_empty()) {
      cout << "Deque is empty! Cannot delete from front.\n";
      return -1;
    }
    Node* temp = front;
    int removedValue = temp->data;
    front = front->next;
    if (front == nullptr) { // if there was only one element, then moving front to its next will make it nullptr
      rear = nullptr; // So we make rear also nullptr
    } else {
      front->prev = nullptr;
    }
    delete temp;
    cout << "Deleted from Front: " << removedValue << endl;
    return removedValue;
  }

  int delete_rear() {
    if (is_empty()) {
      cout << "Deque is empty! Cannot delete from rear.\n";
      return -1;
    }
    Node* temp = rear;
    int removedValue = temp->data;
    rear = rear->prev;
    if (rear == nullptr) { // if there was only one element, then moving rear to its previous will make it nullptr
      front = nullptr; // So we make front also nullptr
    } else {
      rear->next = nullptr;
    }
    delete temp;
    cout << "Deleted from Rear: " << removedValue << endl;
    return removedValue;
  }

  void display() {
    if (is_empty()) {
      cout << "Deque is empty.\n";
      return;
    }
    Node* temp = front;
    cout << "Deque elements: ";
    while (temp != nullptr) {
      cout << temp->data << " ";
      temp = temp->next;
    }
    cout << endl;
  }

  ~Deque() { // Destructor to delete all nodes
    while (!is_empty()) {
      delete_front();
    }
  }
};

int main() {
  Deque dq;
  int choice, value;

  while (true) {
    cout << "\n--- Menu ---\n";
    cout << "1. Insert at Front\n";
    cout << "2. Insert at Rear\n";
    cout << "3. Delete from Front\n";
    cout << "4. Delete from Rear\n";
    cout << "5. Display Queue\n";
    cout << "6. Exit\n";
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        cout << "Enter value to insert at front: ";
        cin >> value;
        dq.insert_front(value);
        break;

      case 2:
        cout << "Enter value to insert at rear: ";
        cin >> value;
        dq.insert_rear(value);
        break;

      case 3:
        dq.delete_front();
        break;

      case 4:
        dq.delete_rear();
        break;

      case 5:
        dq.display();
        break;

      case 6:
        cout << "Exiting program...\n";
        return 0;

      default:
        cout << "Invalid choice! Please enter a number between 1 and 6.\n";
    }
  }
}

