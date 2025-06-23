#include <cstddef>
#include <iostream>
using namespace std;

// ====================================
//   NODETYPE -> SINGLY LINKED LIST
// ====================================

struct Singly {
  int sdata ; 
  Singly *snext=NULL ; 
};
Singly *sfirst=NULL, *slast=NULL; 

// ====================================
//   NODETYPE -> CIRCULAR LINKED LIST
// ====================================

struct Circular {
  int cdata;
  Circular *cnext = NULL;
};
Circular *clast = NULL;
Circular *cp;

// ====================================
//   NODETYPE -> DOUBLY LINKED LIST
// ====================================

struct Doubly {
  int data;
  Doubly *prev=NULL, *next=NULL ; 
};
Doubly *first=NULL, *last=NULL; 

// ====================================
//   TASKS -> SINGLY LINKED LIST
// ====================================

// ==============TASK-01===============
void printReverse() {
  if (sfirst == NULL) {
    cout << "List is Empty." << endl;
    return;
  }
  if (sfirst->snext == NULL) { // Only one node in the list
    cout << "Only one node in List: " << sfirst->sdata << endl;
    return;
  }
  Singly *temp = slast;
  while (temp != NULL) {
    cout << temp->sdata << " ";
    // Finding the previous node before temp
    Singly *p = sfirst;
    Singly *prev = NULL;
    while (p != temp && p->snext != NULL) { // check the condition here for an error
      prev = p;
      p = p->snext;
    }
    // Move temp to the previous node
    temp = prev;
  }
  cout << endl;
}

// ==============TASK-02===============
void reverseList() {
  if (sfirst == NULL) {
    cout << "List is Empty." << endl;
    return;
  }
  if (sfirst->snext == NULL) { // Only one node in the list
    cout << "Only one node in the List. No reverse needed." << endl;
    return;
  }
  Singly *prev = NULL, *current = sfirst, *next = NULL;
  while (current != NULL) {
    next = current->snext; // Store next node
    current->snext = prev; // Reverse pointer
    prev = current;        // Move prev forward
    current = next;        // Move current forward
  }
  // Update head and tail
  slast = sfirst;
  sfirst = prev;
  cout << "List is Reversed: ";
  // printList(); // Uncomment this line to print the list after reversing
  cout << endl;
}


// ==============TASK-03===============
void removeDuplicates() {
  if (sfirst == NULL) {
    cout << "List is Empty." << endl;
    return;
  }
  if (sfirst->snext == NULL) { // Only one node in the list
    cout << "Only one node in the List. No Duplicates possible." << endl;
    return;
  }
  Singly *curr = sfirst;
  while (curr != NULL && curr->snext != NULL) {
    Singly *prev = curr;
    Singly *nextptr = curr->snext;
    while (nextptr != NULL) {
      if (nextptr->sdata == curr->sdata) {
        prev->snext = nextptr->snext; // Remove duplicate node
        if (nextptr->snext == NULL) {
          slast = prev; // Update last is the node to be deleted is last
        }
        delete nextptr;  // Free memory
        nextptr = prev->snext; // Move to the next node
      } else {
        prev = nextptr; // Only update prev if no deletion
        nextptr = nextptr->snext;
      }
    }
    curr = curr->snext; // Move to the next distinct element
  }
}

// ==============TASK-04===============
bool detectLoop() {
  if (sfirst == NULL) {
    cout << "List is Empty." << endl;
    return false;
  }
  if (sfirst->snext == NULL) { // Only one node in the list
    cout << "Only one node. No loop possible." << endl;
    return false;
  }
  Singly *slow = sfirst, *fast = sfirst;
  while (fast != NULL && fast->snext != NULL) {
    slow = slow->snext;       // Move one step
    fast = fast->snext->snext; // Move two steps
    if (slow == fast) { // Cycle detected
      cout << "Loop detected in the linked list!" << endl;
      return true;
    }
  }
  cout << "No loop detected in the linked list." << endl;
  return false;
}

// ==============TASK-05===============
void swapNodes(int key1, int key2) {
  if (sfirst == NULL) {
    cout << "List is Empty." << endl;
    return;
  }
  if (sfirst->snext == NULL) { // Only one node in the list
    cout << "Only one node. No swap possible." << endl;
    return;
  }
  if (key1 == key2) {
    cout << "Both keys are the same, no swap needed." << endl;
    return;
  }
  // Find x and y along with their previous nodes
  Singly *prevX = NULL, *prevY = NULL, *x = sfirst, *y = sfirst;
  while (x && x->sdata != key1) {
    prevX = x;
    x = x->snext;
  }
  while (y && y->sdata != key2) {
    prevY = y;
    y = y->snext;
  }
  // If either node is not found, return
  if (!x || !y) {
    cout << "One or both keys are not in the list." << endl;
    return;
  }
  // If x is not the head, update its previous node to point to y
  if (prevX != NULL)
    prevX->snext = y;
  else // Make y the new head
    sfirst = y;
  // If y is not the head, update its previous node to point to x
  if (prevY != NULL)
    prevY->snext = x;
  else // Make x the new head
    sfirst = x;
  // Swap next pointers
  Singly *temp = x->snext;
  x->snext = y->snext;
  y->snext = temp;
  cout << "Nodes swapped successfully." << endl;
}


// ==============TASK-06===============
// Split list into even and odd lists
void splitEvenOdd() {
  if (sfirst == NULL) {
    cout << "List is Empty." << endl;
    return;
  }

  Singly *evenFirst = NULL, *evenLast = NULL;
  Singly *oddFirst = NULL, *oddLast = NULL;
  Singly *temp = sfirst;

  while (temp != NULL) {
    Singly *newNode = new Singly;
    newNode->sdata = temp->sdata;
    newNode->snext = NULL;

    if (temp->sdata % 2 == 0) { // Even
      if (evenFirst == NULL)
        evenFirst = evenLast = newNode;
      else {
        evenLast->snext = newNode;
        evenLast = newNode;
      }
    } else { // Odd
      if (oddFirst == NULL)
        oddFirst = oddLast = newNode;
      else {
        oddLast->snext = newNode;
        oddLast = newNode;
      }
    }

    temp = temp->snext; // Move to next node
  }

  // Display Even List
  cout << "Even List: ";
  temp = evenFirst;
  while (temp != NULL) {
    cout << temp->sdata << " -> ";
    temp = temp->snext;
  }
  cout << "NULL" << endl;

  // Display Odd List
  cout << "Odd List: ";
  temp = oddFirst;
  while (temp != NULL) {
    cout << temp->sdata << " -> ";
    temp = temp->snext;
  }
  cout << "NULL" << endl;
}

// ==============TASK-07===============
void reverseHalves(Singly*& sfirst) {
  if (sfirst == NULL) {
    cout << "List is Empty." << endl;
    return;
  }
  if (sfirst->snext == NULL) { // Only one node in the list
    cout << "Only one node in the List. No reverse needed." << endl;
    return;
  }

  // Step 1: Find the middle of the linked list
  Singly *slow = sfirst, *fast = sfirst, *firstHalfEnd = NULL;
  while (fast != NULL && fast->snext != NULL) {
    firstHalfEnd = slow; // Store the last node of first half
    slow = slow->snext;
    fast = fast->snext->snext;
  }

  // Step 2: Break the list into two halves
  firstHalfEnd->snext = NULL; // First half ends here, second half starts from slow

  // Step 3: Reverse the first half (and track its last node)
  Singly *prev = NULL, *curr = sfirst, *next = NULL;
  while (curr != NULL) {
    next = curr->snext;
    curr->snext = prev;
    prev = curr;
    curr = next;
  }
  firstHalfEnd = sfirst; // firstHalfEnd is actually the last node of reversed first half
  sfirst = prev; // New head of reversed first half
  // Step 4: Reverse the second half
  prev = NULL, curr = slow, next = NULL;
  while (curr != NULL) {
    next = curr->snext;
    curr->snext = prev;
    prev = curr;
    curr = next;
  }
  slast = slow; //updated this line here

  // Step 5: Directly connect firstHalfEnd to the reversed second half
  firstHalfEnd->snext = prev;

  cout << "List after reversing halves: ";
  // printList(sfirst);
  cout << endl;
}

// ==============TASK-08===============
// Pairwise swap of nodes in SLL
void pairwiseSwap() {
  if (sfirst == NULL || sfirst->snext == NULL) {
    cout << "List too small to swap." << endl;
    return;
  }

  Singly *prev = NULL;
  Singly *current = sfirst;
  sfirst = sfirst->snext; // Update head to second node (new head after first swap)

  while (current != NULL && current->snext != NULL) {
    Singly *temp = current->snext;
    current->snext = temp->snext;
    temp->snext = current;

    if (prev != NULL)
      prev->snext = temp; // Connect previous swapped pair with current

    // Move to next pair
    prev = current;
    current = current->snext;

    // added check to update last pointer
    if (current->snext == slast) {
      slast = current;
    }
  }

  cout << "Nodes swapped in pairs successfully." << endl;
}

// ====================================
//   TASKS -> CIRCULAR LINKED LIST
// ====================================

// ==============TASK-01===============
void josephus_problem (int k) {
  if (clast == NULL) {
    cout << "List is empty. No execution possible." << endl;
    return;
  } else if (clast == clast->cnext) {
    cout << "Only one node. No execution possible." << endl;
    return;
  } else {
    Circular *prev = clast, *current = clast->cnext;
    int count = 1;
    while (clast != clast->cnext) {  // Looping until one node remains
      if (count == k) {  // If we reach k-th node
        cout << "Eliminating: " << current->cdata << endl;
        prev->cnext = current->cnext;
        if (current == clast) {
          clast = prev; // Updated last ptr if last node is eliminated
        }
        delete current;
        current = prev->cnext; // Moving to next node
        count = 1; // Reset counter
      } else {
        prev = current;
        current = current->cnext;
        count++;
      }
    }
    cout << "Final Winner: " << current->cdata << endl;
  }
}

// ====================================
//   TASKS -> DOUBLY LINKED LIST
// ====================================

// ==============TASK-01===============
// TASK: Swap alternate nodes from start and end
void swapAlternateStartEnd() {
  // Step 1: Check if list is empty
  if (first == NULL) {
    cout << "Doubly Linked List is Empty!" << endl;
    return;
  }

  // Step 2: Check for only one node
  if (first == last) {
    cout << "Only one node. No swap needed." << endl;
    return;
  }

  // Step 3: Count total nodes
  Doubly *countPtr = first;
  int count = 0;
  while (countPtr != NULL) {
    count++;
    countPtr = countPtr->next;
  }

  // Special case for two-node list
  if (count == 2) {
    // Swap first and last manually
    Doubly *temp = first;
    first = last;
    last = temp;

    // Adjust links
    first->prev = NULL;
    first->next = last;
    last->prev = first;
    last->next = NULL;

    cout << "List had only two nodes. Swapped successfully." << endl;
    return;
  }


  // Step 5: Loop to swap alternate nodes from start and end
  Doubly *left, *right;
  for (int i = 2; i <= count / 2; i += 2) {
    // Find i-th node from start
    left = first;
    for (int j = 1; j < i; j++) left = left->next;

    // Find i-th node from end
    right = last;
    for (int j = 1; j < i; j++) right = right->prev;

    if (left == right) break; // Center reached or same node (odd case)

    // Check if nodes are adjacent
    if (left->next == right) {
      // Update neighbors' pointers
      left->prev->next = right;
      right->next->prev = left;

      // Adjacent nodes, handle carefully
      Doubly* leftPrev = left->prev;
      Doubly* rightNext = right->next;

      // Swap left and right
      right->prev = leftPrev;
      left->next = rightNext;

      right->next = left;
      left->prev = right;
    }
    else {
      // Normal swapping of non-adjacent nodes

      // Update neighbors' pointers
      left->prev->next = right;
      left->next->prev = right;
      right->prev->next = left;
      right->next->prev = left;

      // Swap left and right's next and prev
      Doubly *tempPrev = left->prev;
      Doubly *tempNext = left->next;

      left->prev = right->prev;
      left->next = right->next;

      right->prev = tempPrev;
      right->next = tempNext;
    }
  }

  cout << "Alternate nodes swapped from start and end successfully." << endl;
}

// ==============TASK-02===============
// Another file in this directory named:
// Inventory-Management-System.cpp

// ====================================
//   MAIN METHOD OF THE PROGRAM
// ====================================

int main () {
  /* CODE HERE */
  /* MENU DRIVEN SWITCH STATEMENT INSIDE A WHILE LOOP WITH TERMINATION CONDITION */
  return 0;
}


