/* For a given postfix expression, use dynamic stack to evaluate a numerical result for given values of variables. */

#include <iostream>
#include <cctype>
#include <string>
#include <cmath>
#include <unordered_map>
using namespace std;

// Node structure for the linked stack
struct Node {
  double data;
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

  void push(double x) {
    Node* temp = new Node;
    temp->data = x;
    temp->next = top;
    top = temp;
  }

  double pop() {
    if (isEmpty()) {
      cout << "Stack Underflow!\n";
      return 0;
    }
    Node* temp = top;
    double x = temp->data;
    top = top->next;
    delete temp;
    return x;
  }

  double peek() {
    if (!isEmpty())
      return top->data;
    return 0;
  }

  bool isEmpty() {
    return top == nullptr;
  }
};

// Function to check if character is an operator
bool isOperator(char c) {
  return (c == '+' || c == '-' || c == '*' || c == '/' || c == '^');
}

// Function to evaluate postfix expression
double evaluatePostfix(string expr, unordered_map<char, double>& varValues) {
  Stack s;
  for (int i = 0; i < expr.length(); i++) {
    char ch = expr[i];

    if (isspace(ch)) { // Ignore spaces
      continue;
    }
   
    else if (isalnum(ch)) { // If the character is an operand (number or variable)
      if (isdigit(ch)) { // If it's a number, push its value
        s.push(ch - '0');
      } else { // If it's a variable, push its value from the map
        s.push(varValues[ch]);
      }
    }

    else if (isOperator(ch)) { // If the character is an operator
      double operand2 = s.pop();
      double operand1 = s.pop();
      
      switch(ch) {
        case '+': 
          s.push(operand1 + operand2);
          break;
        case '-': 
          s.push(operand1 - operand2); 
          break;
        case '*': 
          s.push(operand1 * operand2); 
          break;
        case '/': 
          s.push(operand1 / operand2); 
          break;
        case '^':
          s.push(pow(operand1, operand2)); 
          break;
      }
    }
  }

  return s.peek(); // The result will be at the top of the stack
}

int main() {
  string expression;
  char choice;

  // Input variable values
  unordered_map<char, double> varValues;
  int numVariables;
  cout << "Enter the number of variables: ";
  cin >> numVariables;

  for (int i = 0; i < numVariables; i++) {
    double value;
    cout << "Enter the value for variable " << (char)('a' + i) << ": ";
    cin >> value;
    varValues['a' + i] = value;
  }

  do {
    cout << "\nEnter a postfix expression: ";
    cin >> expression;

    double result = evaluatePostfix(expression, varValues);
    cout << "Result of the postfix expression: " << result << endl;

    cout << "\nDo you want to check another expression? (y/n): ";
    cin >> choice;

  } while (choice == 'y' || choice == 'Y');

  cout << "\nGoodbye!\n";
  return 0;
}

