#include <cstddef>
#include <iostream>
using namespace std;

struct Nodetype {
  int data ; 
  Nodetype *next=NULL ; // link to next node, assigned NULL so that should not point garbage
};
Nodetype *first=NULL, *last=NULL; // first and last pointers are global and point first and last node 

void insert_end() {
  Nodetype *p; //take the pointer to hold the address of nodetype record
  p = new Nodetype;   //allocate runtime memory for new record of nodetype using new operator
  cout<<"Enter the data in node: ";
  cin>>p->data;
  if ( first == NULL ) { // List is empty
    first=last = p; // p becomes first node and first and last pointer will point to same node 
  } else {
    last->next = p; // link the last pointer with newly created node (p) 
    last = p; // assign p to last node 
  }
}

void insert_start() {
  Nodetype *p; //take the pointer to hold the address of nodetype record
  p = new Nodetype; //allocate runtime memory for new record of nodetype using new operator
  cout<<"Enter the data in node: ";
  cin>>p->data;
  if ( first == NULL ) { // List is empty 
    first=last = p; // p becomes first node and first and last pointer will point to same node
  } else {
    p->next=first; // link the new node with first node
    first = p; // assign p to last node 
  }
}

Nodetype* search(int key) {
  Nodetype* p = NULL;
  p = first;
  while (p != NULL && p->data != key) {
    p = p->next;
  }
  return p;  // Return pointer instead of dereferencing
  // if p is NULL then value not found
}

void insert_after (int key) {
  Nodetype *p = NULL;
  p = search(key);
  if(p == NULL){ 
    cout<<"Value not found";
  } else {
    Nodetype *Newnode = new Nodetype;
    cout<<"Enter the data in node: ";
    cin>>Newnode->data;
    if (p == last) { // if p is last node
      last->next = Newnode; // link the last node with new node
      last = Newnode; // assign new node to last node
    } else {
      Newnode->next = p->next; // link new node with next node of p
      p->next = Newnode; // link p with new node
    }
    cout<<"New node linked successfully";
  }
}

void delete_first() {
  Nodetype *p;
  if ( first == NULL ) { // list is empty
    cout<<"\n Linked List is empty";
  } else if ( first == last ) { // only one node
    delete first; // free up memory
    first = last = NULL; // set first and last to NULL
  } else { // non−empty list
    p = first;
    first = first -> next ;
    delete ( p ) ; // free up memory
  }
}

void delete_last() {
  Nodetype *q, *q1;
  q1 = NULL; // initialize 
  q = first ;
  if (q==NULL) {
    cout<<"\n Linked List is empty";
  } else { // non−empty list
    while ( q != last ) { // advance towards end
      q1 = q; // q1 will follow the q pointer
      q = q->next ;
    }
    if ( q == first ) { // only one node
      first = last = NULL;
    } else { // more than one node
      q1->next = NULL;
      last = q1;
    }
    delete q; 
  }
}

void remove_spec(int key) {
  Nodetype *q, *q1;
  q1 = NULL; 
  q = first ;
  /* search node */
  while ( q != NULL && q->data != key ) {
    q1 = q;
    q = q->next ;
  }
  if ( q == NULL ) {
    cout<<"Not found supplied key";
  } else {
    if(q==first && q==last) {
      first=last=NULL;
    } else if (q==last) { 
      q1->next=NULL;
      last=q1; // make 2nd last node as last node
    } else { // other than first node and last
      q1->next = q->next;
    }
    delete q; 
  }
}

void complete_deletion() {
  Nodetype* p;
  while (first != NULL) {
    p = first;
    first = first->next;
    delete p;  // Use delete instead of free because we used new
  }
  last = NULL;
}

void printReverseIterative() {
  if (first == NULL) {
    cout << "List is Empty." << endl;
    return;
  }
  if (first->next == NULL) { // Only one node in the list
    cout << "Only one node in List: " << first->data << endl;
    return;
  }
  Nodetype *temp = last;

  while (temp != NULL) {
    cout << temp->data << " ";

    // Find the node before temp
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


int main() {
  int choice, key;
  while (true) {
    cout << "\nMenu:\n";
    cout << "1. Insert at End\n";
    cout << "2. Insert at Start\n";
    cout << "3. Insert After a Specific Node\n";
    cout << "4. Delete First Node\n";
    cout << "5. Delete Last Node\n";
    cout << "6. Delete a Specific Node\n";
    cout << "7. Display List\n";
    cout << "8. Exit\n";
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        insert_end();
        break;
      case 2:
        insert_start();
        break;
      case 3:
        cout << "Enter value after which to insert: ";
        cin >> key;
        insert_after(key);
        break;
      case 4:
        delete_first();
        break;
      case 5:
        delete_last();
        break;
      case 6:
        cout << "Enter value to delete: ";
        cin >> key;
        remove_spec(key);
        break;
      case 7:
        Nodetype* temp;
        temp = first;
        cout << "Linked List: ";
        while (temp != NULL) {
          cout << temp->data << " -> ";
          temp = temp->next;
        }
        cout << "NULL\n";
        break;
      case 8:
        cout << "Exiting...\n";
        complete_deletion();
        return 0;
      default:
        cout << "Invalid choice. Try again.\n";
    }
  }
}

