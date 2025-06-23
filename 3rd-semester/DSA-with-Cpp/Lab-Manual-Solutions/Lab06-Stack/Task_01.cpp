/* Write an application using Stack that checks whether the entered string of brackets is balanced, e.g. [{( )}] is Balanced while {[( )] } is not Balanced because the priority of the pranthesis is not maintained. */

#include <iostream>
using namespace std;

class Stack {
private:
  char* arr;
  int topIndex;
  int capacity;
public:
  Stack(int size) {
    capacity = size;
    arr = new char[capacity];
    topIndex = -1;
  }

  void push(char ch) {
    if (topIndex == capacity - 1) {
      cout << "Stack Overflow!\n";
      return;
    }
    arr[++topIndex] = ch;
  }

  char pop() {
    if (topIndex == -1) {
      return '\0';
    }
    return arr[topIndex--];
  }

  char top() {
    if (topIndex == -1) {
      return '\0';
    }
    return arr[topIndex];
  }

  bool empty() {
    return topIndex == -1;
  }
};

// Function to check if brackets are matching
bool isMatchingPair(char open, char close) {
  return (open == '(' && close == ')') || (open == '{' && close == '}') || (open == '[' && close == ']');
}

// Main logic to check if expression is balanced
bool isBalanced(string expr) {
  Stack s(expr.length());

  for (char ch : expr) {
    if (ch == '(' || ch == '{' || ch == '[') {
      s.push(ch);
    } else if (ch == ')' || ch == '}' || ch == ']') {
      if (s.empty())
        return false;
      char top = s.top();
      if (!isMatchingPair(top, ch))
        return false;
      s.pop();
    }
    // Ignore other characters
  }
  return s.empty(); // If stack is empty, all brackets are matched
}

int main() {
  string input;
  char choice;

  do {
    cout << "\nEnter a string of brackets: ";
    cin >> input;

    if (isBalanced(input))
      cout << "Expression is Balanced.\n";
    else
      cout << "Expression is NOT Balanced.\n";

    cout << "\nDo you want to check another expression? (y/n): ";
    cin >> choice;

  } while (choice == 'y' || choice == 'Y');

  cout << "Exiting... \n";
  return 0;
}

