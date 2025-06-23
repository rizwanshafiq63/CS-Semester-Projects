#include <cstddef>
#include <iostream>
using namespace std;

struct Nodetype {
  int data;
  Nodetype *next = NULL;
};
Nodetype *first = NULL, *last = NULL;

// ======================
//   GRADED LAB TASK 01
// ======================

// functions to print the linked list in reverse without modifying the list
void printReverseRecursive(Nodetype *p) {
  if (p == NULL) return;
  printReverseRecursive(p->next);
  cout << p->data << " ";
}

void printReverseUsingLoops() {
  if (first == NULL) {
    cout << "List is empty." << endl;
    return;
  }
  if (first->next == NULL) {
    cout << "Only one element in the list: " << first->data << endl;
    return;
  }
  Nodetype *temp = last;

  while (temp != NULL) {
    cout << temp->data << " ";

    // Finding the previous node before temp
    Nodetype *p = first;
    Nodetype *prev = NULL;
    while (p != temp && p->next != NULL) {
      prev = p;
      p = p->next;
    }

    // Move temp to the previous node
    temp = prev;
  }
  cout << endl;
}

// ======================
//   GRADED LAB TASK 03
// ======================

// Function to find multiple occurrences of a data element in the list
void findOccurrences(int key) {
  Nodetype *p = first;
  bool found = false;
  int index = 0;
  cout << "Occurrences of " << key << " found at positions: ";
  while (p != NULL) {
    if (p->data == key) {
      cout << index << " ";
      found = true;
    }
    p = p->next;
    index++;
  }
  if (!found) {
    cout << "None";
  }
  cout << endl;
}

// ======================
//     OTHER METHODS
// ======================

void insert_end() {
  Nodetype *p = new Nodetype;
  cout << "Enter the data in node: ";
  cin >> p->data;
  if (first == NULL) {
    first = last = p;
  } else {
    last->next = p;
    last = p;
  }
}

void insert_start() {
  Nodetype *p = new Nodetype;
  cout << "Enter the data in node: ";
  cin >> p->data;
  p->next = first;
  first = p;
  if (last == NULL) {
    last = p;
  }
}
void display() {
  Nodetype *p = first;
  while (p != NULL) {
    cout << p->data << " ";
    p = p->next;
  }
  cout << endl;
}

int main() {
  int choice;
  do {
    cout << "1. Insert at end\n2. Insert at start\n3. Display List\n4. Print Reverse (Recursive)\n5. Print Reverse (Using Loops)\n6. Find occurrences\n7. Exit\nEnter your choice: ";
    cin >> choice;
    switch (choice) {
      case 1:
        insert_end();
        break;
      case 2:
        insert_start();
        break;
      case 3:
        display();
        break;
      case 4:
        printReverseRecursive(first);
        break;
      case 5:
        printReverseUsingLoops();
        break;
      case 6: {
        int value;
        cout << "Enter value to find: ";
        cin >> value;
        findOccurrences(value);
        break;
      }
      case 7:
        cout << "Exiting..." << endl;
        return 0;
    }
  } while (choice != 7);
}


