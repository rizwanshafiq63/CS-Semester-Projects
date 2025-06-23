/* Implement a Stack in Array, use class in the implementation so that Stack can be treated as an object and its operations as public interface for the user. */

#include <cstring>
#include <iostream>
using namespace std;

// Stack implementation using array
class Stack {
private:
  int top;
  char* values; // Pointer to dynamically allocate array for stack elements
  int size; // Size of the stack
public:
  Stack(int x) {
    top = -1; // Initialize top to -1 indicating stack is empty
    values = new char[x]; // Dynamically allocate memory for the array
    size = x; // Set the size of the stack
  }
  void push(char x) { // Adds an element to the top of the stack
    if(top==size-1)
      cout<<"\nStack overflow condition";
    else
      values[++top] = x;
  }
  char pop() { // Removes the top element of the stack
    if(top == -1){
      cout<<"\nStack Underflow condition";
      return ' ';
    }
    else
    return values[top--];
  }
  char peek() { // Returns the top element of the stack without removing it
    if(top == -1){
      cout<<"\nStack Underflow condition";
      return ' ';
    }
    else
    return values[top];
  }
  void display() { // Displays all elements in the stack
    if(top == -1)
      cout<<"\nStack is empty";
    else {
      cout<<"\nStack elements are: ";
      for(int i=top; i>=0; i--)
        cout<<values[i]<<" ";
    }
  }
};

int main() {
  Stack* myStack = new Stack(10);

  myStack->push('B');
  myStack->push('S');
  myStack->push('S');
  myStack->push('E');
  myStack->push('3');
  myStack->push('Z');

  myStack->display();
  cout<<"\nTop element is: "<<myStack->peek()<<endl;

  cout<<"\nPopping elements from stack: ";
  cout<<myStack->pop();
  cout<<myStack->pop();
  cout<<myStack->pop();
  cout<<myStack->pop();
  cout<<myStack->pop();
  cout<<myStack->pop();
  cout<<myStack->pop();

  /* Implement a Stack in Array, use class in the implementation so that Stack can be treated as an object and its operations as public interface for the user. */
  char str[]="I Love Programming";
  int len = strlen(str);
  Stack s1(len);
  cout<<"\nPushing elements to stack: ";
  for(int i=0; i<len; i++)
    s1.push(str[i]);
  s1.display();
  cout<<"\nPopping elements from stack: ";
  for(int i=0; i<len; i++)
    s1.pop();
}
