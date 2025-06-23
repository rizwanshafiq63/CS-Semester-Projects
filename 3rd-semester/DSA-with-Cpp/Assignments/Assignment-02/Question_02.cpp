/* Two stacks of positive integers are needed, one containing elements with values less than or equal to 1,000 and other containing elements with values larger than 1,000. The total number of elements in the small – value stack and the large – value stack combined are not more than 200 at any time, but we cannot predict how many are in each stack. (All of the elements could be in the small –value stack, they could be evenly divided, both stacks could be empty, and so on). Can you think of a way to implement both stacks in one array?
a) Draw a diagram of how the stack might look.
b) Write the definitions for such a double – stack structure. 
c) Write the algorithm for Push operation; it should store the new item into the correct stack according to its value. */

#include <iostream>
using namespace std;

const int MAX_SIZE = 200; // Maximum combined capacity

class DoubleStack {
private:
  int data[MAX_SIZE];     // Array to hold both stacks
  int topSmall;           // Top index of small-value stack (≤ 1,000)
  int topLarge;           // Top index of large-value stack (> 1,000)

public:
  DoubleStack() {
    topSmall = -1;       // Small-value stack starts empty
    topLarge = MAX_SIZE; // Large-value stack starts beyond the end
  }

  // Push method (to be detailed in part c)
  void push(int item) {
    // Check if there's space
    if (topSmall + 1 >= topLarge) {
      cout << "Stack overflow: No space available" << endl;
      return;
    }

    // Push to appropriate stack based on value
    if (item <= 1000) {
      topSmall++;            // Move topSmall right
      data[topSmall] = item; // Store item in small-value stack
    } else {
      topLarge--;            // Move topLarge left
      data[topLarge] = item; // Store item in large-value stack
    }
  }


  // Helper method to print the stacks (for testing)
  void printStacks() {
    cout << "Small-value stack (≤ 1000): ";
    if (topSmall == -1) {
      cout << "Empty";
    } else {
      for (int i = 0; i <= topSmall; i++) {
        cout << data[i] << " ";
      }
    }
    cout << endl;

    cout << "Large-value stack (> 1000): ";
    if (topLarge == MAX_SIZE) {
      cout << "Empty";
    } else {
      for (int i = MAX_SIZE - 1; i >= topLarge; i--) {
        cout << data[i] << " ";
      }
    }
    cout << endl;
  }

  // Optional: Check if the stacks are full
  bool isFull() {
    return topSmall + 1 >= topLarge;
  }
};

// Main function to test the DoubleStack class
int main() {
  DoubleStack ds; // Create an instance of DoubleStack

  // Test pushing some values
  cout << "Pushing values: 500, 200, 1500, 800, 1200" << endl;
  ds.push(500);   // Small-value stack
  ds.push(200);   // Small-value stack
  ds.push(1500);  // Large-value stack
  ds.push(800);   // Small-value stack
  ds.push(1200);  // Large-value stack

  // Print the stacks after pushing
  cout << "\nAfter pushing values:" << endl;
  ds.printStacks();

  // Test overflow condition (optional)
  cout << "\nAttempting to push 300 after filling some space:" << endl;
  ds.push(300);   // Should work
  ds.printStacks();

  return 0;
}
