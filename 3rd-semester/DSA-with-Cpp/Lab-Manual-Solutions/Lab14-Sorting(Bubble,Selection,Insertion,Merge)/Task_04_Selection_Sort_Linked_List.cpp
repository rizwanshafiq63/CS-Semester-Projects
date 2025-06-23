// Lab Task 4: Implement the Selection sort for Linked list.

#include <iostream>
using namespace std;

// Node structure
struct Node {
  int data;
  Node* next;
};

// Function to insert node at the end
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

// Function to print linked list
void printList(Node* head) {
  while (head) {
    cout << head->data << " ";
    head = head->next;
  }
  cout << endl;
}

// Selection Sort for Linked List
void selectionSortLinkedList(Node* head) {
  Node* current = head;
  while (current) {
    Node* minNode = current;
    Node* nextNode = current->next;
    while (nextNode) {
      if (nextNode->data < minNode->data)
        minNode = nextNode;
      nextNode = nextNode->next;
    }
    // Swap the data
    if (minNode != current) {
      swap(current->data, minNode->data);
    }
    current = current->next;
  }
}

// Main function
int main() {
  Node* head = nullptr;

  insertEnd(head, 29);
  insertEnd(head, 10);
  insertEnd(head, 14);
  insertEnd(head, 37);
  insertEnd(head, 13);

  cout << "Original Linked List: ";
  printList(head);

  selectionSortLinkedList(head);

  cout << "Sorted Linked List: ";
  printList(head);

  return 0;
}


