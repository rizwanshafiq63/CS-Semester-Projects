#include <iostream>
#include <string>
#include <cctype>
using namespace std;

const int MAX_SIZE = 100;

class Stack {
private:
    char data[MAX_SIZE];
    int top;
public:
    Stack() { top = -1; }
    bool isEmpty() { return top == -1; }
    bool isFull() { return top == MAX_SIZE - 1; }
    void push(char item) {
        if (isFull()) { cout << "Stack overflow!" << endl; return; }
        data[++top] = item;
    }
    char pop() {
        if (isEmpty()) { cout << "Stack underflow!" << endl; return '\0'; }
        return data[top--];
    }
    char peek() {
        if (isEmpty()) { return '\0'; } return data[top];
    }
};

// Helper function for precedence
int precedence(char op) {
    if (op == '^') return 3;
    if (op == '*' || op == '/') return 2;
    if (op == '+' || op == '-') return 1;
    return 0;
}

// Infix to Prefix with debug checks
string infixToPrefix(string infix) {
    Stack operatorStack;
    string prefix = "";

    // Step 1: Reverse infix and swap parentheses
    string reversed = "";
    for (int i = infix.length() - 1; i >= 0; i--) {
        if (infix[i] == '(') reversed += ')';
        else if (infix[i] == ')') reversed += '(';
        else reversed += infix[i];
    }
    cout << "Reversed Infix: " << reversed << endl;

    // Step 2: Process reversed infix
    for (char c : reversed) {
        cout << "Processing: " << c << endl;
        if (isalnum(c)) { // Operand
            cout << " - Appending operand: " << c << endl;
            prefix += c;
        } else if (c == ')') { // Closing parenthesis in reversed infix
            cout << " - Pushing closing parenthesis: " << c << endl;
            operatorStack.push(c);
        } else if (c == '(') { // Opening parenthesis in reversed infix
            cout << " - Popping until closing parenthesis" << endl;
            while (!operatorStack.isEmpty() && operatorStack.peek() != ')') {
                char op = operatorStack.pop();
                cout << "   - Popping operator: " << op << endl;
                prefix += op;
            }
            if (!operatorStack.isEmpty()) {
                operatorStack.pop(); // Discard ')'
                cout << "   - Discarding closing parenthesis" << endl;
            }
        } else { // Operator
            while (!operatorStack.isEmpty() && operatorStack.peek() != ')' && 
                   precedence(operatorStack.peek()) > precedence(c)) {
                char op = operatorStack.pop();
                cout << " - Popping operator: " << op << endl;
                prefix += op;
            }
            cout << " - Pushing operator: " << c << endl;
            operatorStack.push(c);
        }
    }

    // Step 3: Pop remaining operators
    while (!operatorStack.isEmpty()) {
        char op = operatorStack.pop();
        if (op != ')') { // Skip stray parentheses
            cout << " - Popping remaining operator: " << op << endl;
            prefix += op;
        }
    }

    // Step 4: Reverse the result
    string result = "";
    for (int i = prefix.length() - 1; i >= 0; i--) {
        result += prefix[i];
    }
    cout << "Final Prefix before reversal: " << prefix << endl;
    return result;
}

// Main function to test
int main() {
    string infix = "(A+B)*C";
    cout << "Infix: " << infix << endl;
    string prefix = infixToPrefix(infix);
    cout << "Prefix: " << prefix << endl;
    return 0;
}
