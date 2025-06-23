#include <iostream>
using namespace std;

// ======================================================
//   STRUCTURES FOR SINGLY AND DOUBLY LINKED LISTS
// ======================================================

struct SLLNode {
  int data;
  SLLNode *next = NULL;
};

struct DLLNode {
  int data;
  DLLNode *next = NULL, *prev = NULL;
};

// Pointers for both lists
SLLNode *sll_first = NULL, *sll_last = NULL;
DLLNode *dll_first = NULL, *dll_last = NULL, *p;

// ======================================================
//            INSERT METHODS FOR DLL & SLL
// ======================================================

// ------------------ SLL Insert At End ------------------
void insertAtEnd_SLL() {
  SLLNode *temp = new SLLNode;
  cout << "Enter data for SLL Node: ";
  cin >> temp->data;
  if (sll_first == NULL)
    sll_first = sll_last = temp;
  else {
    sll_last->next = temp;
    sll_last = temp;
  }
  cout << "Inserted in SLL: " << temp->data << endl;
}

// ------------------ DLL Insert At End ------------------
void insertAtEnd_DLL() {
  p = new DLLNode;
  cout << "Enter data for DLL Node: ";
  cin >> p->data;
  if (dll_first == NULL)
    dll_first = dll_last = p;
  else {
    dll_last->next = p;
    p->prev = dll_last;
    dll_last = p;
  }
  cout << "Inserted in DLL: " << p->data << endl;
}

// ======================================================
//        LAB TASK 1: REVERSE DOUBLY LINKED LIST
// ======================================================

void reverseList() {
  if (dll_first == NULL) {
    cout << "Doubly Linked List is Empty. Cannot reverse the list." << endl;
    return;
  }
  if (dll_first == dll_last) {
    cout << "Only one node in DLL. No Need to reverse." << endl;
    return;
  }
  // Method 1:
  DLLNode *curr = dll_first, *prev = NULL, *next = dll_first->next;
  while (curr != NULL) {
    curr->next = prev; // Reverse the next pointer
    curr->prev = next; // Set the previous pointer to the next node
    prev = curr;       // Move prev to current node
    curr = next;      // Move to the next node
    if (next != NULL)
      next = next->next; // Move to the next node in original list
  }
    // Update the last node's next pointer to NULL
  dll_last = dll_first;
  // At this point, prev is the new head of the reversed list
  dll_first = prev; // Update the head of the list
  /* // Method 2:
  DLLNode *current = dll_first, *temp = NULL;
  while (current != NULL) {
    temp = current->prev;
    current->prev = current->next;
    current->next = temp;
    current = current->prev;
  }
  // Adjust head and tail
  if (temp != NULL)
    dll_first = temp->prev; // New head
  // Swap dll_first and dll_last
  DLLNode *swapTemp = dll_first;
  dll_first = dll_last;
  dll_last = swapTemp;
  */
  cout << "Doubly Linked List has been reversed." << endl;
}

// ======================================================
//             LAB TASK 2: SWAP TWO NODES
// ======================================================

void swapNodes(int val1, int val2) {
  if (dll_first == NULL) { // Empty List
    cout << "Doubly Linked List is Empty!" << endl;
    return;
  }
  if (dll_first == dll_last) { // One Node
    cout << "Only one node in DLL. No Need to swap" << endl;
    return;
  }
  if (val1 == val2) { // Same keys
    cout << "Both values are same. No need to swap." << endl;
    return;
  }
  // Finding the keys in Doubly List
  DLLNode *node1 = dll_first, *node2 = dll_first;
  while (node1 && node1->data != val1) { 
    node1 = node1->next;
  }
  while (node2 && node2->data != val2) { 
    node2 = node2->next;
  }

  if (!node1 || !node2) { // If not found
    cout << "One or both values not found." << endl;
    return;
  }
  // Adjusting previous nodes' next pointers
  if (node1->prev) {
    node1->prev->next = node2; // If node1 has a previous node, make its next point to node2.
  } else {
    dll_first = node2; // If node1 is the first node (head) (no previous), update dll_first to node2.
  }
  if (node2->prev) {
    node2->prev->next = node1;
  } else {
    dll_first = node1;
  }
  // Similarly Adjusting next nodes' prev pointers
  if (node1->next) {
    node1->next->prev = node2;
  } else {
    dll_last = node2;  // If node1 was last, now node2 will be last
  }
  if (node2->next) {
    node2->next->prev = node1;
  } else {
    dll_last = node1;  // If node2 was last, now node1 will be last
  }
  // Swapping node1 and node2
  DLLNode *temp_prev = node1->prev;
  DLLNode *temp_next = node1->next;

  node1->prev = node2->prev;
  node1->next = node2->next;

  node2->prev = temp_prev;
  node2->next = temp_next;

  cout << "Nodes swapped successfully." << endl;
}

// ======================================================
//    LAB TASK 3: CONVERT SLL TO DLL (COPY DATA)
// ======================================================

void convertSLLtoDLL() {
  if (sll_first == NULL) {
    cout << "Singly Linked List is Empty! Nothing to Reverse..." << endl;
    return;
  }
  SLLNode *temp = sll_first;
  while (temp != NULL) {
    // Creating new DLL node
    p = new DLLNode;
    p->data = temp->data;
    p->next = NULL; // extra line
    p->prev = dll_last;

    // Inserting into DLL
    if (dll_first == NULL)
      dll_first = dll_last = p;
    else {
      dll_last->next = p;
      dll_last = p;
    }

    temp = temp->next;
  }
  cout << "Singly Linked List successfully converted to Doubly Linked List." << endl;
}

// ======================================================
//            DISPLAY METHODS FOR DLL & SLL
// ======================================================

// ------------------ DLL Display ------------------
void Display_DLL() {
  if (dll_first == NULL) {
    cout << "Doubly Linked List is Empty!" << endl;
    return;
  }
  p = dll_first;
  cout << "Doubly Linked List: ";
  while (p != NULL) {
    cout << p->data;
    if (p->next != NULL) cout << " <-> ";
    p = p->next;
  }
  cout << endl;
}

// ------------------ Display SLL ------------------
void Display_SLL() {
  if (sll_first == NULL) {
    cout << "Singly Linked List is empty." << endl;
    return;
  }
  SLLNode *temp = sll_first;
  cout << "Singly Linked List: ";
  while (temp != NULL) {
    cout << temp->data << " -> ";
    temp = temp->next;
  }
  cout << "NULL" << endl;
}

// ======================================================
//          COMPLETE DELETION FOR DLL & SLL
// ======================================================

// ------------------ DLL Deletion ------------------
void completeDeletion_DLL() {
  if (dll_first == NULL) {
    cout << "Doubly Linked List is already empty!" << endl;
    return;
  }
  cout << "Deleting complete DLL...!" << endl;
  while (dll_first != NULL) {
    p = dll_first;
    dll_first = dll_first->next;
    delete p;
  }
  dll_last = NULL;
  cout << "Doubly Linked List has been deleted completely." << endl;
}

// ------------------ SLL Deletion ------------------
void completeDeletion_SLL() {
  if (sll_first == NULL) {
    cout << "Singly Linked List is already empty!" << endl;
    return;
  }
  cout << "Deleting complete SLL...!" << endl;
  SLLNode *temp;
  while (sll_first != NULL) {
    temp = sll_first;
    sll_first = sll_first->next;
    delete temp;
  }
  sll_last = NULL;
  cout << "Singly Linked List has been deleted completely." << endl;
}

// ======================================================
//                       MAIN METHOD
// ======================================================

int main() {
  int choice;
  while (true) {
    cout << "\n=========== OPTIONS MENU ===========\n";
    cout << "1. Insert in SLL\n";
    cout << "2. Insert in DLL\n";
    cout << "3. Display SLL\n";
    cout << "4. Display DLL\n";
    cout << "5. Delete SLL Completely\n";
    cout << "6. Delete DLL Completely\n";
    cout << "7. Reverse DLL (Lab Task 1)\n";
    cout << "8. Swap nodes in DLL (Lab Task 2)\n";
    cout << "9. Convert SLL to DLL (Lab Task 3)\n";
    cout << "0. Exit\n";
    cout << "Enter your choice: ";
    cin >> choice;

    cout << "\n============== OUTPUT ==============\n";
    switch (choice) {
      case 1:
        insertAtEnd_SLL();
        break;
      case 2:
        insertAtEnd_DLL();
        break;
      case 3:
        Display_SLL();
        break;
      case 4:
        Display_DLL();
        break;
      case 5:
        completeDeletion_SLL();
        break;
      case 6:
        completeDeletion_DLL();
        break;
      case 7:
        reverseList();
        break;
      case 8:
        int val1, val2;
        cout << "Enter first value to swap: ";
        cin >> val1;
        cout << "Enter second value to swap: ";
        cin >> val2;
        swapNodes(val1, val2);
        break;
      case 9:
        convertSLLtoDLL();
        break;
      case 0:
        cout << "Exiting Program...\nGoodbye!" << endl;
        return 0;
      default:
        cout << "Invalid Choice! Please try again." << endl;
    }
  }
}

