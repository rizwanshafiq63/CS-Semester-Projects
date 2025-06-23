/* A DEQUE is a data structure consisting of a list of items, on which the following operations are possible:
PUSH ( X,D) : Insert item X on the front end of DEQUE D.
POP(D) : Remove the front item from DEQUE D and return it.
Inject(X, D) : Insert item X on the rear end of DEQUE D.
Eject(D) : Remove the rear item from DEQUE D and return it.
Write C++ program (complete program) that support the above DEQUE operations. */

#include <iostream>
using namespace std;
#define SIZE 20

class DEQUE {
  int items[SIZE], front, rear; 
public:
  DEQUE();
  void PUSH(int x);    // Insert at front
  int POP();           // Remove from front and return
  void Inject(int x);  // Insert at rear
  int Eject();         // Remove from rear and return
  void show();         // Display the deque
};

// Constructor
DEQUE::DEQUE() {
  front = -1;
  rear = -1;
}

// Insert at front (PUSH)
void DEQUE::PUSH(int x) {
  if (front == -1) { // Empty deque
    front = 0;
    items[++rear] = x;
    cout << "\nPushed item at front: " << x;
  } else if (front > 0) { // Space at front
    items[--front] = x;
    cout << "\nPushed item at front: " << x;
  } else {
    cout << "\nInsertion not possible, overflow at front!!!";
  }
}

// Remove from front (POP)
int DEQUE::POP() {
  if (front == -1) {
    cout << "\nDeletion not possible: DEQUE is empty";
    return -1;
  } else {
    int item = items[front];
    if (front == rear) { // Last element
      front = rear = -1;
    } else {
      front = front + 1;
    }
    cout << "\nPopped item from front: " << item;
    return item;
  }
}

// Insert at rear (Inject)
void DEQUE::Inject(int x) {
  if (rear >= SIZE - 1) {
    cout << "\nInsertion not possible, overflow at rear!!!!";
  } else {
    if (front == -1) { // Empty deque
      front++;
      rear++;
    } else {
      rear = rear + 1;
    }
    items[rear] = x;
    cout << "\nInjected item at rear: " << x;
  }
}

// Remove from rear (Eject)
int DEQUE::Eject() {
  if (front == -1) {
    cout << "\nDeletion not possible: DEQUE is empty";
    return -1;
  } else {
    int item = items[rear];
    if (front == rear) { // Last element
      front = rear = -1;
    } else {
      rear = rear - 1;
    }
    cout << "\nEjected item from rear: " << item;
    return item;
  }
}

// Display the deque
void DEQUE::show() {
  if (front == -1) {
    cout << "\nDEQUE is empty";
  } else {
    cout << "\nDEQUE: ";
    for (int i = front; i <= rear; i++) {
      cout << items[i] << " ";
    }
  }
}

int main() {
  DEQUE d;
  int choice, x;

  do {
    cout << "\n\n1. PUSH (Insert at front)";
    cout << "\n2. POP (Remove from front)";
    cout << "\n3. Inject (Insert at rear)";
    cout << "\n4. Eject (Remove from rear)";
    cout << "\n5. Show";
    cout << "\n6. Exit";
    cout << "\nEnter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        cout << "Enter item to push at front: ";
        cin >> x;
        d.PUSH(x);
        break;
      case 2:
        d.POP();
        break;
      case 3:
        cout << "Enter item to inject at rear: ";
        cin >> x;
        d.Inject(x);
        break;
      case 4:
        d.Eject();
        break;
      case 5:
        d.show();
        break;
      case 6:
        cout << "Exiting..." << endl;
        exit(0);
        break;
      default:
        cout << "Invalid choice" << endl;
        break;
    }
  } while (choice != 6);

  return 0;
}

