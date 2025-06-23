// Lab Task 5: Implement the Insertion sort for Linked list.

#include <iostream>
using namespace std;

// Node structure
struct Node {
  int data;
  Node* next;
};

// Function to insert at the end of the list
void insertEnd(Node*& head, int value) {
  Node* newNode = new Node{value, nullptr};
  if (!head) {
    head = newNode;
    return;
  }
  Node* temp = head;
  while (temp->next)
    temp = temp->next;
  temp->next = newNode;
}

// Function to print the linked list
void printList(Node* head) {
  while (head) {
    cout << head->data << " ";
    head = head->next;
  }
  cout << endl;
}

// Insertion Sort for Linked List
void insertionSortLinkedList(Node*& head) {
  Node* sorted = nullptr; // new sorted list
  Node* current = head;
  while (current) {
    Node* next = current->next;
    // Insert current into sorted list
    if (!sorted || current->data < sorted->data) {
      current->next = sorted;
      sorted = current;
    } else {
      Node* temp = sorted;
      while (temp->next && temp->next->data < current->data) {
        temp = temp->next;
      }
      current->next = temp->next;
      temp->next = current;
    }
    current = next;
  }
  head = sorted; // update original head
}

// Main function
int main() {
  Node* head = nullptr;

  insertEnd(head, 50);
  insertEnd(head, 20);
  insertEnd(head, 40);
  insertEnd(head, 10);
  insertEnd(head, 30);

  cout << "Original Linked List: ";
  printList(head);

  insertionSortLinkedList(head);

  cout << "Sorted Linked List: ";
  printList(head);

  return 0;
}

