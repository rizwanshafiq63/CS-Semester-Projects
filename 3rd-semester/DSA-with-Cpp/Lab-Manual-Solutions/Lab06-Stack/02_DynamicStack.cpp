#include <iostream>
using namespace std;

// Linked Stack Implementation
struct Node {
  char data;
  Node* link;
};


class LinkedStack {
private:
  Node* head;
public:
  LinkedStack() {
    head = NULL;
  }
  void push(char e) { // Add an element to the top of the stack
    Node* temp = new Node;
    temp->data = e;
    temp->link = head; // Link new node to the top of the stack
    head = temp;
  }
  char pop() { // Remove the top element and return it
    if(head == NULL) {
      cout<<"\nStack is Empty .... Underflow Codition\n";
      return ' '; // safe return value
    } else {
      Node* temp = head;
      char T = temp->data;
      head = temp->link; // Move head to the next node
      delete temp;
      return T;
    }
  }
  char top() { // Return the top element without removing it
    if(head == NULL) {
      cout<<"\nStack is Empty .... Underflow Codition\n";
      return ' '; // safe return value
    } else {
      return head->data;
    }
  }
  void display() { // Display the elements in the stack
    Node* temp = head;
    if(temp == NULL)
      cout<<"\nStack is Empty .... Underflow Codition\n";
    else {
      cout<<"\nStack Elements are: ";
      while(temp != NULL) {
        cout<<temp->data<<" ";
        temp = temp->link;
      }
    }
  }
  void clear() { // Clear the stack
    Node* temp;
    while(head != NULL) {
      temp = head;
      head = head->link;
      delete temp;
    }
  }
  void printReverseRec(Node* node) { // Recursive function to print stack in reverse order
    if(node == NULL)
      return;
    printReverseRec(node->link);
    cout<<node->data<<" ";
  }
  void printReverse() { // Print the stack in reverse order
    if(head == NULL)
      cout<<"\nStack is Empty .... Underflow Codition\n";
    else {
      cout<<"\nStack Elements in Reverse Order: ";
      printReverseRec(head); // Call the recursive function
    }
  }
};

int main() {
  LinkedStack S;
  char ch, e;
  do {
    cout<<"\n\n1. Push\n2. Pop\n3. Top\n4. Display\n5. Clear\n6. Print Reverse\n7. Exit";
    cout<<"\nEnter your choice: ";
    cin >> ch;
    switch(ch) {
      case '1':
        cout<<"\nEnter element to push: ";
        cin>>e;
        S.push(e);
        break;
      case '2':
        cout<<"\nPopped element: "<<S.pop();
        break;
      case '3':
        cout<<"\nTop element: "<<S.top();
        break;
      case '4':
        S.display();
        break;
      case '5':
        S.clear();
        cout<<"\nStack Cleared!";
        break;
      case '6':
        S.printReverse();
        break;
      case '7':
        exit(0);
      default:
        cout<<"\nInvalid Choice!";
    }
  } while(ch != '7');
  return 0;
}

/* // Uncomment the following lines to test the LinkedStack class
int main() {
  LinkedStack myStack;
  myStack.push('H');
  myStack.push('e');
  myStack.push('l');
  myStack.push('l');
  myStack.push('o');
  cout<<myStack.pop();
  cout<<myStack.pop();
  cout<<myStack.pop();
  cout<<myStack.pop();
  cout<<myStack.pop();
} */

