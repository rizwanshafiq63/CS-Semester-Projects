#include <cstddef>
#include <iostream>
using namespace std;

// ====================================
//   NODETYPE -> DOUBLY LINKED LIST
// ====================================

struct Nodetype {
  int data;
  Nodetype *next = NULL, *prev = NULL;
};
Nodetype *first = NULL, *last = NULL, *p;

// ====================================
//             SEARCH METHOD
// ====================================

Nodetype* search_key(int key) {
  p = first;
  if (first == NULL) {
    cout<<"List is Empty"<<endl;
    p = NULL;
    return p;
  }
  while (p!=NULL && p->data!=key) {
    p = p->next;
  }
  return p;
}

// ====================================
//            INSERT METHODS
// ====================================

void insertAtEnd() {
  p = new Nodetype ;
  cout<<"Enter the data in node: ";
  cin>>p->data;
  if ( first == NULL ) 
    first = last = p;
  else {
    last->next = p;
    p->prev=last;
    last = p;
  }
  cout<<"Inserted At End: "<<p->data<<endl;
}

void insertAtStart() {
  p = new Nodetype;
  cout << "Enter the data in node: ";
  cin >> p->data;
  if (first == NULL)
    first = last = p;
  else {
    p->next = first;
    first->prev = p;
    first = p;
  }
  cout<<"Inserted At Start: "<<p->data<<endl;
}

void insertAfterSpecific(int key) {
  Nodetype *specific = search_key(key);
  if (specific == NULL) {
    cout<<key<<" not found in the list"<<endl;
    return;
  }
  p = new Nodetype ;
  cout<<"Enter the data in node: ";
  cin>>p->data;
  if ( specific == last ) { //if specific is last
    last->next = p;
    p->prev = last;
    last = p;
  }else { // if specific is in between somewhere
    p->next = specific->next;
    p->prev = specific;
    p->next->prev = p;
    specific->next = p;
  }
  cout<<"Inserted After "<<key<<": "<<p->data<<endl;
}

void insertBeforeSpecific(int key) {
  Nodetype *specific = search_key(key);
  if (specific == NULL) {
    cout<<key<<" not found in the list"<<endl;
    return;
  }
  p = new Nodetype ;
  cout<<"Enter the data in node: ";
  cin>>p->data;
  if ( specific == first ) { //if specific is before the first
    p->next = first;
    first->prev = p;
    first = p;
  } else { // if specific is in between somewhere
    specific = specific->prev; // just added this line here
    p->next = specific->next;
    p->prev = specific;
    p->next->prev = p;
    specific->next = p;
    // OR:
    // p->next = specific;
    // p->prev = specific->prev;
    // p->prev->next = p;
    // specific->prev = p;
  }
  cout<<"Inserted Before "<<key<<": "<<p->data<<endl;
}

// ====================================
//            DELETE METHODS
// ====================================

void deleteFromEnd(){
  if (first == NULL) { // List Empty
    cout<<"List is Empty. Nothing to delete."<<endl;
    return;
  }
  if (first == last) {  // Only one node
    delete(last);
    first = last = NULL;
    cout << "Deleted Single Node! List is now empty." << endl;
    return;
  }
  p = last;
  last = last->prev;
  last->next = NULL;
  cout<<"Deleted From Last: "<<p->data<<endl;
  delete(p);
}

void deleteFromStart() {
  if (first == NULL) { // List Empty
    cout<<"List is Empty. Nothing to delete."<<endl;
    return;
  } 
  if (first == last) {  // Only one node
    delete(last);
    first = last = NULL;
    cout << "Deleted Single Node! List is now empty." << endl;
    return;
  }
  p = first;
  first = first->next;
  first->prev = NULL;
  cout<<"Deleted From Start: "<<p->data<<endl;
  delete(p);
}

void deleteSpecific(int key) {
  Nodetype *specific = search_key(key);
  if (specific == NULL) { // Key not found
    cout<<key<<" not found in the list"<<endl;
    return;
  }
  if (first == last && specific->data == key) {  // Only one node
    delete(specific);
    first = last = NULL;
    cout<<"Deleted "<<key<<" Successfully! List is now empty."<<endl;
    return;
  }
  if (specific == first) { // Node is at first
    first = first->next;
    first->prev = NULL;
  } else if (specific == last) { // Node is at last
    last = last->prev;
    last->next = NULL;
  } else { // Node is in between
    specific->prev->next = specific->next;
    specific->next->prev = specific->prev;
  }
  cout<<"Deleted "<<key<<" Successfully!"<<endl;
  delete(specific);

}

void deleteAfterSpecific(int key) {
  Nodetype *specific = search_key(key);
  if (specific == NULL) {
    cout<<key<<" not found in the list"<<endl;
    return;
  } 
  if (specific == last) {
    cout<<key<<" is the last of List. Nothing to delete after it."<<endl;
    return;
  }
  // LOGIC_01:
  Nodetype *toDelete = specific->next; // node to be deleted
  if (toDelete == last) { // if next node is last
    specific->next = NULL;
    last = specific;
  } else { // middle node
    specific->next = toDelete->next;
    toDelete->next->prev = specific;
  }
  cout<<"Deleted "<<toDelete->data<<" Successfully!"<<endl;
  delete(toDelete);
}

void deleteBeforeSpecific(int key) {
  Nodetype *specific = search_key(key);
  if (specific == NULL) {
    cout<<key<<" not found in the list"<<endl;
    return;
  }
  if (specific == first) {
    cout<<key<<" is at first of list. Nothing to delete before it."<<endl;
    return;
  }
  // LOGIC_02:
  specific = specific->prev; //decrement to the node to be deleted
  if (specific == first){ // if first node
    specific->next->prev = NULL;
    first = specific->next;
  } else { // middle node
    specific->prev->next = specific->next;
    specific->next->prev = specific->prev;
  }
  cout<<"Deleted "<<specific->data<<" Successfully!"<<endl;
  delete(specific);
}

void completeDeletion() {
  cout<<"Deleting complete list...!"<<endl;
  while (first != NULL) {
    p = first;
    first = first->next;
    delete(p);
  }
  last = NULL;
  cout<<"List has been deleted completely."<<endl;
}

// ====================================
//             DISPLAY METHOD
// ====================================

void Display() {
  if (first == NULL) {
    cout<<"List is Empty! Nothing to Display..."<<endl;
    return;
  }
  p = first;
  cout<<"Doubly Linked List: ";
  while(p->next != NULL){
    cout<<p->data<<" <-> ";
    p = p->next;
  }
  cout<<p->data<<endl;
}

// ====================================
//             MAIN METHOD
// ====================================

int main() {
  int choice, key;

  while (true) {
    cout << "\n======= Doubly Linked List Menu =======\n";
    cout << "1. Insert at Start\n";
    cout << "2. Insert at End\n";
    cout << "3. Insert After Specific Node\n";
    cout << "4. Insert Before Specific Node\n";
    cout << "5. Search a Node\n";
    cout << "6. Delete from Start\n";
    cout << "7. Delete from End\n";
    cout << "8. Delete Specific Node\n";
    cout << "9. Delete After Specific Node\n";
    cout << "10. Delete Before Specific Node\n";
    cout << "11. Complete Deletion (Delete All Nodes)\n";
    cout << "12. Display List\n";
    cout << "13. Exit\n";
    cout << "Enter your choice(1-13): ";
    cin >> choice;

    cout << "\n================ Output ===============\n";
    switch (choice) {
      case 1:
        insertAtStart();
        break;
      case 2:
        insertAtEnd();
        break;
      case 3:
        cout << "Enter key after which to insert: ";
        cin >> key;
        insertAfterSpecific(key);
        break;
      case 4:
        cout << "Enter key before which to insert: ";
        cin >> key;
        insertBeforeSpecific(key);
        break;
      case 5:
        cout << "Enter key to search: ";
        cin >> key;
        if (search_key(key) != NULL)
          cout << key << " found in the list." << endl;
        else
          cout << key << " not found in the list." << endl;
        break;
      case 6:
        deleteFromStart();
        break;
      case 7:
        deleteFromEnd();
        break;
      case 8:
        cout << "Enter key to delete: ";
        cin >> key;
        deleteSpecific(key);
        break;
      case 9:
        cout << "Enter key after which to delete: ";
        cin >> key;
        deleteAfterSpecific(key);
        break;
      case 10:
        cout << "Enter key before which to delete: ";
        cin >> key;
        deleteBeforeSpecific(key);
        break;
      case 11:
        completeDeletion();
        break;
      case 12:
        Display();
        break;
      case 13:
        cout << "Exiting program. Goodbye!" << endl;
        return 0;
      default:
        cout << "Invalid choice! Please try again." << endl;
    }
  }
}

