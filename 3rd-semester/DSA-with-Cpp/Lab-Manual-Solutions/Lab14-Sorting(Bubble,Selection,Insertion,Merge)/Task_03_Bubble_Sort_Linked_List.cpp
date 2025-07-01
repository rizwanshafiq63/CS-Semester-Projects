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

// Bubble Sort on linked list (swapping of data)
void bubbleSortLinkedList(Node* head) {
  if (!head) return;

  bool swapped;
  Node* current;
  Node* lastSorted = nullptr;

  do {
    swapped = false;
    current = head;

    while (current->next != lastSorted) {
      if (current->data > current->next->data) {
        // Swap the data, not the nodes
        swap(current->data, current->next->data);
        swapped = true;
      }
      current = current->next;
    }

    lastSorted = current; // The last node is now sorted
  } while (swapped);
}

// Bubble Sort on linked list (swapping of actual nodes)
void bubbleSortLL(Node*& head) {
  if (!head || !head->next) return;

  bool swapped;
  Node* lastSorted = nullptr;

  do {
    swapped = false;
    Node* curr = head;
    Node* prev = nullptr;

    while (curr->next != lastSorted) {
      Node* next = curr->next;
      if (curr->data > next->data) {
        // Swap needed
        curr->next = next->next;
        next->next = curr;

        if (prev == nullptr) {
          // Swapping at the head
          head = next;
        } else {
          prev->next = next;
        }

        // Update pointers
        prev = next;
        swapped = true;
      } else {
        // No swap
        prev = curr;
        curr = curr->next;
      }
    }
    lastSorted = curr; // Everything after this is sorted
  } while (swapped);
}

// Main function to demonstrate the sort
int main() {
  Node* head = nullptr;

  insertEnd(head, 64);
  insertEnd(head, 75);
  insertEnd(head, 23);
  insertEnd(head, 12);
  insertEnd(head, 22);
  insertEnd(head, 11);

  cout << "Original linked list: ";
  printList(head);

  //bubbleSortLinkedList(head);
  bubbleSortLL(head);

  cout << "Sorted linked list: ";
  printList(head);

  return 0;
}

