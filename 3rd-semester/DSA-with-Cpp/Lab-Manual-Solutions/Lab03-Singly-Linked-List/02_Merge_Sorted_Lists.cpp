// Task: Merge two sorted singly linked lists into a new sorted linked list without modifying the original lists.

#include <iostream>
using namespace std;

struct Nodetype {
  int data;
  Nodetype *next = NULL;
};

// Function to insert nodes at the end of a linked list
void insert_end(Nodetype *&first, Nodetype *&last, int data) {
  Nodetype *p = new Nodetype;
  p->data = data;
  if (first == NULL) {
    first = last = p;
  } else {
    last->next = p;
    last = p;
  }
}

// Merge function that creates a new linked list in ascending order
Nodetype* mergeTwoSortedSinglyLinkedLists(Nodetype *first1, Nodetype *first2) {
  Nodetype *newFirst = NULL, *newLast = NULL;

  // Used temp variables so that first1 and first2 remain unchanged
  Nodetype *temp1 = first1;
  Nodetype *temp2 = first2;

  while (temp1 != NULL && temp2 != NULL) {
    if (temp1->data < temp2->data) {
      insert_end(newFirst, newLast, temp1->data);
      temp1 = temp1->next;
    } else {
      insert_end(newFirst, newLast, temp2->data);
      temp2 = temp2->next;
    }
  }

  // Appending remaining elements from non-terminated list
  while (temp1 != NULL) {
    insert_end(newFirst, newLast, temp1->data);
    temp1 = temp1->next;
  }

  while (temp2 != NULL) {
    insert_end(newFirst, newLast, temp2->data);
    temp2 = temp2->next;
  }

  return newFirst; // Return the start of the merged list
}

// Function to print a linked list
void printList(Nodetype *first) {
  while (first != NULL) {
    cout << first->data << " -> ";
    first = first->next;
  }
  cout << "NULL" << endl;
}

int main() {
  // Create first sorted linked list
  Nodetype *first1 = NULL, *last1 = NULL;
  insert_end(first1, last1, 1);
  insert_end(first1, last1, 3);
  insert_end(first1, last1, 5);

  // Create second sorted linked list
  Nodetype *first2 = NULL, *last2 = NULL;
  insert_end(first2, last2, 2);
  insert_end(first2, last2, 4);
  insert_end(first2, last2, 6);

  cout << "First List: ";
  printList(first1);

  cout << "Second List: ";
  printList(first2);

  // Merge lists
  Nodetype *mergedList = mergeTwoSortedSinglyLinkedLists(first1, first2);

  cout << "Merged List: ";
  printList(mergedList);

  // After merging, first1 and first2 are still unchanged
  cout << "First List After Merging: ";
  printList(first1);

  cout << "Second List After Merging: ";
  printList(first2);

  return 0;
}

