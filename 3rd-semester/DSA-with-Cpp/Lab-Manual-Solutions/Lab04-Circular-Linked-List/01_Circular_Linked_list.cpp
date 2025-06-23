#include <cstddef>
#include <iostream>
using namespace std;

// ====================================
//   NODETYPE -> CIRCULAR LINKED LIST
// ====================================

struct Nodetype {
  int data;
  Nodetype *next = NULL;
};
Nodetype *last = NULL;
Nodetype *p;

// ====================
//   GRADED LAB TASKS
// ====================

// LAB TASK 01: Write a function that deletes all those nodes from a linked list which have even/odd numbered value in their data part.
void delete_Even_Data() {
  if (last == NULL) {
    cout << "List is empty. Nothing to delete." << endl;
    return;
  }
  Nodetype *current = last->next, *prev = last;
  bool deleted = false;
  while (current != last) { 
    if (current->data % 2 == 0) { // Even data found
      prev->next = current->next;
      Nodetype *temp = current;
      current = current->next;
      delete temp;
      deleted = true;
    } else {
      prev = current;
      current = current->next;
    }
  }
  // Final check for the last node
  if (last != NULL && last->data % 2 == 0) {
    if (last == last->next) { // Only one node left
      delete last;
      last = NULL;
      cout << "All even elements deleted. List is now empty." << endl;
    } else {
      prev->next = last->next;
      delete last;
      last = prev;
    }
    deleted = true;
  }
  if (!deleted) {
    cout << "No even elements found in the list." << endl;
  }
} // for odd we will change the condition (current->data % 2 != 0)


// LAB TASK 02: Write a function that implements Josephus problem.
void josephus_problem (int k) {
  if (last == NULL) {
    cout << "List is empty. No execution possible." << endl;
    return;
  } else if (last == last->next) {
    cout << "Only one node. No execution possible." << endl;
    return;
  } else {
    Nodetype *prev = last, *current = last->next;
    int count = 1;
    while (last != last->next) {  // Looping until one node remains
      if (count == k) {  // If we reach k-th node
        cout << "Eliminating: " << current->data << endl;
        prev->next = current->next;
        if (current == last) {
          last = prev; // Updated last ptr if last node is eliminated
        }
        delete current;
        current = prev->next; // Moving to next node
        count = 1; // Reset counter
      } else {
        prev = current;
        current = current->next;
        count++;
      }
    }
    cout << "Final Winner: " << current->data << endl;
  }
}

// LAB TASK 03: Write a function that deletes all even positioned nodes from a linked list. Last node should also be deleted if its position is even.
void delete_Even_Positioned_Nodes() {
  if (last == NULL) {
    cout << "List is empty. Nothing to delete." << endl;
    return;
  }
  Nodetype *current = last->next, *prev = last;
  int position = 1; // Just added this in the above method
  bool deleted = false;
  do {
    if (position % 2 == 0) { // If position is even
      if (current == last) { // If it's the last node
        last = prev; // Update last pointer if needed
      }
      prev->next = current->next;
      Nodetype *temp = current;
      current = current->next;
      delete temp;
      deleted = true;
    } else {
      prev = current;
      current = current->next;
    }
    position++;
  } while (current != last->next);
  if (!deleted) {
    cout << "No even-positioned nodes found in the list." << endl;
  }
  // There will be no handle case for a single node.
}

// ==================
//   SEARCH METHODS
// ==================

Nodetype* search_Key(int givenKey) {
  if (last == NULL) {  
    return NULL;
  }
  Nodetype *p = last->next; 
  do {
    if (p->data == givenKey) {  
      return p; 
    }
    p = p->next;
  } while (p != last->next); 
  return NULL; 
}

Nodetype* search_Previous(int givenkey) {
  if (last == NULL) {  // If the list is empty
    return NULL;
  }
  p = last;  // Starting from the last node
  do {
    if (p->next->data == givenkey) {  
      return p; // Found previous node
    }
    p = p->next;
  } while (p != last); 
  return NULL; // If key not found
}

// ==================
//   INSERT METHODS
// ==================

void insert_End() {  
  p = new Nodetype ;
  cout<<"Enter the data in node: ";
  cin>>p->data;
  // List is empty
  if ( last == NULL ) {
    last = p;
    p->next = p;
  } else {
    p->next = last->next;
    last->next = p;
    last = p; //last = last->next;
  }
}

void insert_Start() {
  p = new Nodetype ;
  cout<<"Enter the data in node: ";
  cin>>p->data;
  // List is empty
  if ( last == NULL ) {
    last = p;
    p->next = p;
  } else {
    p->next = last->next;
    last->next = p;
  }
}

void insert_Before(int givenKey) {
  if (last == NULL) {
    cout << "List is empty. Cannot insert before " << givenKey << "." << endl;
    return;
  }
  Nodetype *prev = search_Previous(givenKey);
  if (prev == NULL) {
    cout << "Key not found!" << endl;
    return;
  }
  p = new Nodetype;
  cout << "Enter the data: ";
  cin >> p->data;
  // If inserting before the first node or any node
  p->next = prev->next;
  prev->next = p;
}

void insert_After(int givenKey) {
  if (last == NULL) {
    cout << "List is empty. Cannot insert after " << givenKey << "." << endl;
    return;
  }

  Nodetype *current = search_Key(givenKey); // Find the node with givenKey
  if (current == NULL) {
    cout << "Key not found!" << endl;
    return;
  }

  Nodetype *p = new Nodetype;
  cout << "Enter the data: ";
  cin >> p->data;

  p->next = current->next; // Insert after current node
  current->next = p;

  // If inserting after the last node, update last
  if (current == last) {
    last = p;
  }
}

// ==================
//   DELETE METHODS
// ==================

void delete_Specific(int givenKey) {
  // Case when list is empty
  if (last == NULL) {
    cout << "List is empty. Nothing to delete." << endl;
    return;
  } else if (last->next == last && last->data == givenKey) {
    // Case when there's only one node and it matches the given key
    delete last;
    last = NULL;
    return;
  } else {
    Nodetype *prev_of_key = search_Previous(givenKey);
    // If the key is not found
    if (prev_of_key == NULL) {
      cout << "Key not found!" << endl;
      return;
    }
    Nodetype *toDelete = prev_of_key->next;
    prev_of_key->next = toDelete->next;
    // If deleting the last node, update `last`
    if (toDelete == last) {
      last = prev_of_key;
    }
    delete toDelete;
  }
}

void delete_Before(int givenKey) {
  if (last == NULL || last->next == last) { 
    cout << "List is too small to delete before " << givenKey << "." << endl;
    return;
  }
  Nodetype *prev = search_Previous(givenKey);
  if (prev == NULL || prev->next == last->next) { 
    cout << "No valid node to delete before " << givenKey << "." << endl;
    return;
  }
  Nodetype *beforePrev = search_Previous(prev->data);
  beforePrev->next = prev->next;
  delete prev;
}

void delete_After(int givenKey) {
  if (last == NULL || last->next == last) { 
    cout << "List is too small to delete after " << givenKey << "." << endl;
    return;
  }
  Nodetype *current = search_Key(givenKey);
  if (current == NULL) { 
    cout << "Key not found!" << endl;
    return;
  }
  Nodetype *toDelete = current->next; 
  // If the node to be deleted is the last node, update last
  if (toDelete == last) {
    last = current;
  }
  current->next = toDelete->next;
  delete toDelete;
}


// ==================
//   DISPLAY METHOD
// ==================
void display() {
  if (last == NULL) {  // First, check if the list is empty
    cout << "List is Empty" << endl;
    return;
  }
  p = last->next; // Start from the first node
  do {
    cout << p->data << " -> ";
    p = p->next;
  } while (p != last->next); // Loop until it comes back to the first node
  cout<<"(back to "<<last->next->data<<")"<< endl;
}

// ===============
//   MAIN METHOD
// ===============

int main() {
  int choice, key;
  while (true) {
    cout << "\nCircular Linked List Operations:\n";
    cout << "1. Insert at End\n";
    cout << "2. Insert at Start\n";
    cout << "3. Insert Before a Key\n";
    cout << "4. Insert After a Key\n";
    cout << "5. Delete a Specific Node\n";
    cout << "6. Delete Before a Key\n";
    cout << "7. Delete After a Key\n";
    cout << "8. Search for a Key\n";
    cout << "9. Display List\n";
    cout << "10. Delete Even Data\n";
    cout << "11. Delete Even Positioned Nodes\n";
    cout << "12. Josephus Problem\n";
    cout << "0. Exit\n";
    cout << "Enter your choice (0-11): ";
    cin >> choice;

    switch (choice) {
      case 1:
        insert_End();
        break;
      case 2:
        insert_Start();
        break;
      case 3:
        cout << "Enter key to insert before: ";
        cin >> key;
        insert_Before(key);
        break;
      case 4:
        cout << "Enter key to insert after: ";
        cin >> key;
        insert_After(key);
        break;
      case 5:
        cout << "Enter key to delete: ";
        cin >> key;
        delete_Specific(key);
        break;
      case 6:
        cout << "Enter key to delete before: ";
        cin >> key;
        delete_Before(key);
        break;
      case 7:
        cout << "Enter key to delete after: ";
        cin >> key;
        delete_After(key);
        break;
      case 8:
        cout << "Enter key to search: ";
        cin >> key;
        if (search_Key(key)) {
          cout << "Key found in the list." << endl;
        } else {
          cout << "Key not found." << endl;
        }
        break;
      case 9:
        display();
        break;
      case 10:
        delete_Even_Data();
        break;
      case 11:
        delete_Even_Positioned_Nodes();
        break;
      case 12:
        cout << "Enter k for Josephus problem: ";
        cin >> key;
        josephus_problem(key);
        break;
      case 0:
        cout << "Exiting..." << endl;
        return 0;
      default:
        cout << "Invalid choice. Try again." << endl;
    }
  }
}

