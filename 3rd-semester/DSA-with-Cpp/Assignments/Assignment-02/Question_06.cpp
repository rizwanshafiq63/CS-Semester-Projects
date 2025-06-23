/* i. Write an algorithm for converting an infix expression into prefix expression
ii. Write an algorithm for evaluation of prefix expression */

#include <iostream>
#include <string>
#include <cctype>
#include <cmath>
using namespace std;

const int MAX_SIZE = 100; // Imaginary max size for the stack
template <typename T> // Template Stack class

class Stack {
private:
  T data[MAX_SIZE]; // Array to hold elements
  int top;          // Index of the top element

public:
  Stack() {
    top = -1;
  }

  bool isEmpty() {
    return top == -1;
  }

  bool isFull() {
    return top == MAX_SIZE - 1;
  }

  void push(T item) {
    if (isFull()) {
      cout << "Stack overflow!" << endl;
      return;
    }
    data[++top] = item;
  }

  T pop() {
    if (isEmpty()) {
      cout << "Stack underflow!" << endl;
      return T(); // Default value for type T
    }
    return data[top--];
  }

  T peek() {
    if (isEmpty()) {
      return T(); // Default value for type T
    }
    return data[top];
  }
};

// Helper function to get operator precedence
int precedence(char op) {
  if (op == '^') return 3;
  if (op == '*' || op == '/') return 2;
  if (op == '+' || op == '-') return 1;
  return 0;
}

// i. Algorithm to convert infix to prefix
string infixToPrefix(string infix) {
  Stack<char> operatorStack;
  string prefix = "";

  // Step 1: Reverse infix and swap parentheses
  string reversed = "";
  for (int i = infix.length() - 1; i >= 0; i--) {
    if (infix[i] == '(') reversed += ')';
    else if (infix[i] == ')') reversed += '(';
    else reversed += infix[i];
  }

  // Step 2: Process reversed infix
  for (char c : reversed) {
    if (isalnum(c)) { // Operand
      prefix += c;
    } else if (c == '(') { // Closing parenthesis in reversed infix
      operatorStack.push(c);
    } else if (c == ')') { // Opening parenthesis in reversed infix
      while (!operatorStack.isEmpty() && operatorStack.peek() != '(') {
        char op = operatorStack.pop();
        prefix += op;
      }
      if (!operatorStack.isEmpty()) {
        operatorStack.pop(); // Discard '('
      }
    } else { // Operator
      while (!operatorStack.isEmpty() && operatorStack.peek() != '(' && 
        precedence(operatorStack.peek()) >= precedence(c)) { // Note: >= for correct associativity
        char op = operatorStack.pop();
        prefix += op;
      }
      operatorStack.push(c);
    }
  }

  // Step 3: Pop remaining operators
  while (!operatorStack.isEmpty()) {
    char op = operatorStack.pop();
    if (op != ')' && op != '(') { // Skip parentheses
      prefix += op;
    }
  }

  // Step 4: Reverse the result
  string result = "";
  for (int i = prefix.length() - 1; i >= 0; i--) {
    result += prefix[i];
  }
  return result;
}

// ii. Algorithm to evaluate prefix expression
double evaluatePrefix(string prefix) {
  Stack<double> operandStack;

  // Process from right to left
  for (int i = prefix.length() - 1; i >= 0; i--) {
    char t = prefix[i];
    if (isdigit(t)) { // Assuming single-digit numbers for simplicity
      operandStack.push(t - '0'); // Convert char to double
    } else if (t == '+' || t == '-' || t == '*' || t == '/' || t == '^') {
      double operand1 = operandStack.pop();
      double operand2 = operandStack.pop();
      double result;
      switch (t) {
        case '+': result = operand1 + operand2; break;
        case '-': result = operand1 - operand2; break;
        case '*': result = operand1 * operand2; break;
        case '/': result = operand1 / operand2; break;
        case '^': result = pow(operand1, operand2); break;
        default: result = 0;
      }
      operandStack.push(result);
    }
  }
  return operandStack.pop();
}

// Main function to test both algorithms
int main() {
  // Test infix to prefix conversion
  string infix1 = "(A+B)*C";
  //string infix1 = "7+(5-3*6)+8/2+9";
  cout << "Infix: " << infix1 << endl;
  string prefix1 = infixToPrefix(infix1);
  cout << "Prefix: " << prefix1 << endl;

  string infix2 = "A^B*C-D+E/F";
  cout << "\nInfix: " << infix2 << endl;
  string prefix2 = infixToPrefix(infix2);
  cout << "Prefix: " << prefix2 << endl;

  // Test prefix evaluation (using numbers)
  string prefixEval = "+*23 4"; // Represents + (* 2 3) 4
  //string prefixEval = "+7+-5*36+/829";
  cout << "\nPrefix expression: " << prefixEval << endl;
  double result = evaluatePrefix(prefixEval);
  cout << "Evaluation result: " << result << endl;

  return 0;
}

