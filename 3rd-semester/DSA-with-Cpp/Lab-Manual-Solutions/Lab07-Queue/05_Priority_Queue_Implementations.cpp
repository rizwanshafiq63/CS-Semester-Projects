#include <iostream>
#include <stack>
using namespace std;

// ======================= Priority Queue Implementations ======================

// ===============================================================
//                     Static Implementation
// ===============================================================
// 1. Using Linear Array
class StaticPriorityQueue{
private:
  int* a;
  int size, StartIndex, LastIndex;

public:
  StaticPriorityQueue (int x) {
    a = new int(5);
    size = x;
    StartIndex = -1;
    LastIndex = -1;
  }

  void enqueue(){
    int x;
    if(LastIndex == size - 1) {
      cout << "\n No Space in Queue";
    } else {
      cout << "\n Enter the value in Queue:";
      cin >> x;
      if (StartIndex == -1) {
        StartIndex = LastIndex = 0;
        a[LastIndex] = x;
      } else if (a[LastIndex] <= x) {
        a[++LastIndex] = x;
      } else {
        int i = LastIndex;
        while ((a[i] > x) && (i >= StartIndex)){
          a[i+1] = a[i];
          i--;
        }
        cout << "\n Value to be inserted at index: " << i+1 << "is: " << x;
        a[i+1] = x;
        LastIndex++;
      }
    }
  }

  int dequeue() {
    if (StartIndex == -1) {
      cout << "\n Queue is Empty";
      return -1;
    } else {
      int x = a[StartIndex];
      for (int i = StartIndex; i < LastIndex; i++) {
        a[i] = a[i+1];
      }
      LastIndex--;
      return x;
    }
  }

  void display() {
    if (StartIndex == -1) {
      cout << "\n Queue is Empty\n";
    } else {
      cout << "\n Queue Elements: ";
      for (int i = StartIndex; i <= LastIndex; i++) {
        cout << a[i] << " ";
      }
      cout << endl;
    }
  }
};

 
// ===============================================================
//                      Dynamic Implementation
// ===============================================================
// 1. Using Linked List
struct PQueue {
  int data;
  PQueue* next = NULL;
};

class LinkedListPriorityQueue {
private:
  PQueue *front, *rear;
public:
  LinkedListPriorityQueue () {
    front = NULL;
    rear = NULL;
  }

  void enqueue () {
    PQueue *curr, *q;
    curr = new PQueue;
    cout << "\n Enter the data: ";
    cin >> curr->data;

    if (front == NULL) {
      front = rear = curr;
    } else if ( curr->data < front->data){
      curr->next = front;
      front = curr;
    } else if (curr->data >= rear->data){  
      rear->next = curr;
      rear = curr;
    } else {
      q = front;
      while ((q->next != NULL) && (q->next->data <= curr->data)) {
        q = q->next;
      }
      curr->next = q->next;
      q->next = curr;
    }
  }

  int dequeue () {
    PQueue *curr;
    if (front == NULL) {
      cout << "\n Queue Underflow!";
      return -1;
    }
    curr = front;
    int x = front->data;
    front = front->next;
    cout << "\n Deleted item is " << curr->data;
    delete curr;
    return x;
  }

  void display() {
    if (front == NULL) {
      cout << "\n Queue is Empty\n";
    } else {
      cout << "\n Queue Elements: ";
      PQueue* temp = front;
      while (temp != NULL) {
        cout << temp->data << " ";
        temp = temp->next;
      }
      cout << endl;
    }
  }
};

//2. Using Stack (Sorted Insertion)
class StackPriorityQueue {
private:
  stack<int> s;
public:
  StackPriorityQueue () {}

  void enqueue () {
    int x;
    cout << "\n Enter the value to insert: ";
    cin >> x;

    stack<int> temp;

    // Move elements greater than x to temp stack
    while (!s.empty() && s.top() < x) {
      temp.push(s.top());
      s.pop();
    }

    // Insert the new element
    s.push(x);

    // Restore the rest of the elements
    while (!temp.empty()) {
      s.push(temp.top());
      temp.pop();
    }
  }

  int dequeue () {
    if (s.empty()) {
      cout << "\n Queue is Empty!\n";
      return -1;
    } else {
      int x = s.top();
      s.pop();
      cout << "\n Deleted item is: " << x << endl;
      return x;
    }
  }

  void display() {
    if (s.empty()) {
      cout << "\nQueue is Empty\n";
    } else {
      cout << "\nQueue Elements (Top to Bottom): ";
      stack<int> temp = s; // Create a copy to preserve the original stack
      while (!temp.empty()) {
        cout << temp.top() << " ";
        temp.pop();
      }
      cout << endl;
    }
  }
};

// Runner Methods
void staticPriorityQueueRunner() {
  int size;
  cout << "Enter maximum size for StaticPriorityQueue: ";
  cin >> size;
  StaticPriorityQueue q(size);
  int choice;

  do {
    cout << "\n--- StaticPriorityQueue Menu ---\n";
    cout << "1. Enqueue\n2. Dequeue\n3. Display\n4. Exit Static Queue\nChoice: ";
    cin >> choice;
    switch (choice) {
      case 1:
        q.enqueue();
        break;
      case 2:
        q.dequeue();
        break;
      case 3:
        q.display();
        break;
      case 4:
        cout << "Exiting StaticPriorityQueue...\n";
        break;
      default:
        cout << "Invalid Choice!\n";
    }
  } while (choice != 4);
}

void linkedListPriorityQueueRunner() {
  LinkedListPriorityQueue q;
  int choice;

  do {
    cout << "\n--- LinkedListPriorityQueue Menu ---\n";
    cout << "1. Enqueue\n2. Dequeue\n3. Display\n4. Exit LinkedList Queue\nChoice: ";
    cin >> choice;
    switch (choice) {
      case 1:
        q.enqueue();
        break;
      case 2:
        q.dequeue();
        break;
      case 3:
        q.display();
        break;
      case 4:
        cout << "Exiting LinkedListPriorityQueue...\n";
        break;
      default:
        cout << "Invalid Choice!\n";
    }
  } while (choice != 4);
}

void stackPriorityQueueRunner() {
  StackPriorityQueue q;
  int choice;

  do {
    cout << "\n--- StackPriorityQueue Menu ---\n";
    cout << "1. Enqueue\n2. Dequeue\n3. Display\n4. Exit Stack Queue\nChoice: ";
    cin >> choice;
    switch (choice) {
      case 1:
        q.enqueue();
        break;
      case 2:
        q.dequeue();
        break;
      case 3:
        q.display();
        break;
      case 4:
        cout << "Exiting StackPriorityQueue...\n";
        break;
      default:
        cout << "Invalid Choice!\n";
    }
  } while (choice != 4);
}

// Main Menu
int main() {
  int choice;

  do {
    cout << "\n=== Priority Queue Implementation Menu ===\n";
    cout << "1. Static Priority Queue (Array)\n2. Linked List Priority Queue\n3. Stack Priority Queue\n4. Exit Program\nChoice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        staticPriorityQueueRunner();
        break;
      case 2:
        linkedListPriorityQueueRunner();
        break;
      case 3:
        stackPriorityQueueRunner();
        break;
      case 4:
        cout << "Exiting Program...\n";
        break;
      default:
        cout << "Invalid Choice!\n";
    }
  } while (choice != 4);

  return 0;
}

