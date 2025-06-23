/* In each plastic container of Pez candy, the colors are stored in random order. Your little brother likes only yellow ones, so he painstakingly takes out all the candies, one by one, eats the yellow ones, and keeps the other in order, so that he can return them to container in exactly the same order as before- minus the yellow candies, of course. Write the algorithm to simulate this process. You may use any of the stack operations defined in the stack ADT, but may not assume any knowledge of stack’s implementation. */

#include <iostream>
#include <string>
using namespace std;

const int MAX_SIZE = 100; // Imaginary max size for the stack

class Stack {
private:
  string data[MAX_SIZE]; // Array to hold stack elements
  int top;               // Index of the top element

public:
  // Constructor
  Stack() {
    top = -1; // Stack starts empty
  }

  // Check if stack is empty
  bool isEmpty() {
    return top == -1;
  }

  // Check if stack is full
  bool isFull() {
    return top == MAX_SIZE - 1;
  }

  // Push an item onto the stack
  void push(string item) {
    if (isFull()) {
      cout << "Stack overflow!" << endl;
      return;
    }
    top++;
    data[top] = item;
  }

  // Pop an item from the stack
  string pop() {
    if (isEmpty()) {
      cout << "Stack underflow!" << endl;
      return ""; // Return empty string for simplicity
    }
    string item = data[top];
    top--;
    return item;
  }

  // Peek at the top item without removing it
  string peek() {
    if (isEmpty()) {
      return "";
    }
    return data[top];
  }

  // Print stack contents from top to bottom without modifying it
  void printStack() {
    if (isEmpty()) {
      cout << "Empty";
    } else {
      cout << "Stack (top to bottom): ";
      for (int i = top; i >= 0; i--) {
        cout << data[i] << " ";
      }
    }
    cout << endl;
  }
};

// Function to filter yellow candies using the custom Stack class
void filterYellowCandies(Stack& originalStack) {
  Stack tempStack; // Temporary stack for non-yellow candies

  // Step 1: Process original stack, keeping non-yellow candies
  while (!originalStack.isEmpty()) {
    string candy = originalStack.pop();
    if (candy != "yellow") {
      tempStack.push(candy);
    }
  }

  // Step 2: Transfer non-yellow candies back to original stack
  while (!tempStack.isEmpty()) {
    string candy = tempStack.pop();
    originalStack.push(candy);
  }
}

// Main function to test the solution
int main() {
  Stack pezContainer; // Custom stack for the Pez container

  // Push candies (bottom to top order)
  pezContainer.push("Green");  // Bottom
  pezContainer.push("Yellow");
  pezContainer.push("Blue");
  pezContainer.push("Yellow");
  pezContainer.push("Red");    // Top

  cout << "Original stack: ";
  pezContainer.printStack(); // Non-destructive print

  // Filter out yellow candies
  filterYellowCandies(pezContainer);

  cout << "After filtering yellow candies: ";
  pezContainer.printStack(); // Non-destructive print

  return 0;
}


