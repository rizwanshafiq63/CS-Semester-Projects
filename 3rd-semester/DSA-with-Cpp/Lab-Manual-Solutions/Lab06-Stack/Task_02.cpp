/* Use dynamic stack and implement Infix to Postfix conversion algorithm and test it for various inputs. */

#include <iostream>
#include <cctype>
#include <string>
using namespace std;

// Node structure for the linked stack
struct Node {
  char data;
  Node* next;
};

// Dynamic Stack using Linked List
class Stack {
private:
  Node* top;
public:
  Stack() {
    top = nullptr;
  }

  void push(char x) {
    Node* temp = new Node;
    temp->data = x;
    temp->next = top;
    top = temp;
  }

  char pop() {
    if (isEmpty()) {
      cout << "Stack Underflow!\n";
      return '\0';
    }
    Node* temp = top;
    char x = temp->data;
    top = top->next;
    delete temp;
    return x;
  }

  char peek() {
    if (!isEmpty())
      return top->data;
    return '\0';
  }

  bool isEmpty() {
    return top == nullptr;
  }
};

// Function to return precedence of operators
int precedence(char op) {
  if (op == '^') {
    return 3;
  } else if (op == '*' || op == '/') {
    return 2;
  }else if (op == '+' || op == '-') {
    return 1;
  } else {
    return 0;
  }
}

// Function to check if operator is right-associative
bool isRightAssociative(char op) { // All operators are left associative except '^'
  return op == '^';
}

// Function to check if character is operator
bool isOperator(char c) {
  return (c == '+' || c == '-' || c == '*' || c == '/' || c == '^');
}

// Function to convert infix to postfix
string infixToPostfix(string infix) {
  Stack s;
  string postfix = "";
  for (int i = 0; i < infix.length(); i++) {
    char ch = infix[i];
    if (isspace(ch)) { // Ignore spaces
      continue;
    } else if (isalnum(ch)) { // If the character is an operand (number or letter)
      postfix += ch;
    } else if (ch == '(') { // If the character is '(', push it to stack
      s.push(ch);
    } else if (ch == ')') { // If the character is ')', pop and output from the stack
      while (!s.isEmpty() && s.peek() != '(')
        postfix += s.pop();
      if (!s.isEmpty() && s.peek() == '(')
        s.pop(); // discard the '('
    } else if (isOperator(ch)) { // If the character is an operator
      while (!s.isEmpty() && isOperator(s.peek())) { // While the stack is not empty and the top of the stack is an operator
        char topOp = s.peek();
        if ((precedence(topOp) > precedence(ch)) || (precedence(topOp) == precedence(ch) && !isRightAssociative(ch))) {
          postfix += s.pop(); // Pop from stack to output
        } else {
          break;
        }
      }
      s.push(ch); // Push the current operator to stack.
    }
  }

  while (!s.isEmpty()) { // Pop all the operators from the stack
    postfix += s.pop();
  }

  return postfix;
}

int main() {
  string expression;
  char choice;

  do {
    cout << "\nEnter an Infix expression: ";
    cin >> expression;

    string result = infixToPostfix(expression);
    cout << "Postfix Expression: " << result << endl;

    cout << "\nCheck another expression? (y/n): ";
    cin >> choice;
  } while (choice == 'y' || choice == 'Y');

  cout << "\nGoodbye!\n";
  return 0;
}

