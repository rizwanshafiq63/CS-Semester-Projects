/* Using the stack check that the given expression has balanced paranthesis or not. */

#include<iostream>
using namespace std;

class stack {
  char *arr;
  int topelem;
  int capacity;
public:
  stack(int size) {
    arr = new char[size];
    capacity = size;
    topelem = -1;
  }
  ~stack() {
    delete[] arr;
  }
  void push(char x) {
    if (topelem == capacity - 1) {
      cout << "Stack Overflow\n";
      return;
    }
    arr[++topelem] = x;
  }
  char pop() {
    if (topelem == -1) {
      cout << "Stack Underflow\n";
      return '\0';
    }
    return arr[topelem--];
  }
  char top() {
    if (topelem == -1) {
      cout << "Stack is empty\n";
      return '\0';
    }
    return arr[topelem];
  }
  bool empty() {
    return topelem == -1;
  }
};

// bool isBalanced(string expr) {
bool isBalanced(const string& expr) { // avoids copying large strings
  int len = expr.length();
  stack s(len);
  char ch;
  for (int i=0; i<expr.length(); i++) {
    if (expr[i]=='('||expr[i]=='['||expr[i]=='{') {
      s.push(expr[i]);
      continue;
    }
    if (s.empty())
      return false;
    switch (expr[i]) {
      case ')':
        ch = s.top();
        s.pop();
        if (ch=='{' || ch=='[')
          return false;
        break;
      case '}':
        ch = s.top();
        s.pop();
        if (ch=='(' || ch=='[')
          return false;
        break;
      case ']':
        ch = s.top();
        s.pop();
        if (ch =='(' || ch == '{')
          return false;
        break;
    }
  }
  return (s.empty()); //when stack is empty, return true
}

bool isBalanced_Updated(const string& expr) { // Support Extra Characters in Expression
  int len = expr.length();
  stack s(len);
  char ch;
  for (int i = 0; i < len; i++) {
    char current = expr[i];
    if (current == '(' || current == '[' || current == '{') {
      s.push(current);
    } else if (current == ')' || current == ']' || current == '}') {
      if (s.empty())
        return false;
      ch = s.top();
      s.pop();
      if ((current == ')' && ch != '(') || (current == '}' && ch != '{') || (current == ']' && ch != '['))
        return false;
    }
    // else: skip non-bracket characters
  }
  return s.empty(); // Return true if stack is empty, indicating all brackets were matched
}


int main() {
  cout << "Testing without extra characters:" << endl;
  string expr = "[{}(){()}]";
  cout << "Input: " << expr << endl;
  if (isBalanced(expr))
    cout << "Balanced"<<endl;
  else
    cout << "Not Balanced"<<endl; 
  string expr2 = "[(])";
  cout << "Input: " << expr2 << endl;
  if (isBalanced(expr2))
    cout << "Balanced"<<endl;
  else
    cout << "Not Balanced"<<endl;

  // Test with extra characters
  cout << "\nTesting with extra characters:" << endl;
  string expr3 = "[{a+b}*(x/y)-{z+1}]";
  cout << "Input: " << expr3 << endl;
  cout << (isBalanced_Updated(expr3) ? "Balanced" : "Not Balanced") << endl;

  string expr4 = "if(x > 0 && (y < 0 || z == 1) {";
  cout << "Input: " << expr4 << endl;
  cout << (isBalanced_Updated(expr4) ? "Balanced" : "Not Balanced") << endl;
  return 0;
}

// Input: [{}(){()}]
// Output: Balanced
// Input: [(])
// Output: Not Balanced
// The above code uses stack to check for balanced paranthesis.
// The code uses a stack to keep track of the opening brackets and checks if they are closed in the correct order.
// If the stack is empty at the end,it means all brackets were closed correctly and the expression is balanced.
// If the stack is not empty, it means there are unmatched opening brackets and the expression is not balanced.
// The code also checks for mismatched brackets by comparing the top of the stack with the closing bracket.
// If they do not match, the expression is not balanced.

