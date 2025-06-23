#include <iostream>
using namespace std;

class Stack {
private:
  char* arr;
  int* priorityArr; // Array to store priorities
  int topIndex;
  int capacity;
public:
  Stack(int size) {
    capacity = size;
    arr = new char[capacity];
    priorityArr = new int[capacity];
    topIndex = -1;
  }

  void push(char ch, int priority) {
    if (topIndex == capacity - 1) {
      cout << "Stack Overflow!\n";
      return;
    }
    arr[++topIndex] = ch;
    priorityArr[topIndex] = priority;
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

  int topPriority() {
    if (topIndex == -1) {
      return -1;
    }
    return priorityArr[topIndex];
  }

  bool empty() {
    return topIndex == -1;
  }

  ~Stack() {
    delete[] arr;
    delete[] priorityArr;
  }
};

// Function to return bracket priority
int getPriority(char ch) {
  if (ch == '(' || ch == ')') return 1;
  if (ch == '[' || ch == ']') return 2;
  if (ch == '{' || ch == '}') return 3;
  return 0;
}

// Function to check if brackets are matching
bool isMatchingPair(char open, char close) {
  return (open == '(' && close == ')') ||
         (open == '[' && close == ']') ||
         (open == '{' && close == '}');
}

// Main logic to check if expression is balanced and follows priority
bool isBalanced(string expr) {
  Stack s(expr.length());

  for (char ch : expr) {
    if (ch == '(' || ch == '[' || ch == '{') {
      int currPriority = getPriority(ch);
      if (!s.empty() && currPriority <= s.topPriority()) {
        // If inner bracket has lower or same priority → invalid
        return false;
      }
      s.push(ch, currPriority);
    } else if (ch == ')' || ch == ']' || ch == '}') {
      if (s.empty())
        return false;
      char topChar = s.top();
      if (!isMatchingPair(topChar, ch))
        return false;
      s.pop();
    }
    // Ignore other characters
  }

  return s.empty(); // If stack is empty, all brackets were matched correctly
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

