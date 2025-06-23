// Lab Task 3: Implement the bubble sort for Linked list.

#include <iostream>
using namespace std;

// Node structure
struct Node {
  int data;
  Node* next;
};

// Function to insert a node at the end of the list
void insertEnd(Node*& head, int value) {
  Node* newNode = new Node{value, nullptr};
  if (!head) {
    head = newNode;
    return;
  }
  Node* temp = head;
  while (temp->next) {
    temp = temp->next;
  }
  temp->next = newNode;
}

// Function to print the linked list
void printList(Node* head) {
  Node* temp = head;
  while (temp) {
    cout << temp->data << " ";
    temp = temp->next;
  }
  cout << endl;
}

// Bubble Sort on linked list
void bubbleSortLinkedList(Node* head) {
  if (!head) {
    return;
  }
  bool swapped;
  Node* ptr1;
  Node* lptr = nullptr;
  do {
    swapped = false;
    ptr1 = head;
    while (ptr1->next != lptr) {
      if (ptr1->data > ptr1->next->data) {
        swap(ptr1->data, ptr1->next->data);
        swapped = true;
      }
      ptr1 = ptr1->next;
    }
    lptr = ptr1;
  } while (swapped);
}

// Main function to demonstrate the sort
int main() {
  Node* head = nullptr;

  insertEnd(head, 64);
  insertEnd(head, 25);
  insertEnd(head, 12);
  insertEnd(head, 22);
  insertEnd(head, 11);

  cout << "Original linked list: ";
  printList(head);

  bubbleSortLinkedList(head);

  cout << "Sorted linked list: ";
  printList(head);

  return 0;
}

