/* Consider the following recursion for integer multiplication of two positive number a and b:
a* 1 = a
a*b = a(b -1) + a
This can be implemented using following recursive algorithm as follows:
Algorithm recursive_multiplication(a, b)
  if b = 1 then
    return a
  else
    return a + recursive_multiplication ( a, b-1)
a) Convert above recursive algorithm in to an iterative algorithm? Present your iterative version into Pseudo code.
b) Mathematically the following definition for integer multiplication is valid:
  a multiply by b : a*b = a(b+1) – a
Can we have recursive algorithm for calculating integer multiplication based on above definition? Explain carefully. */

#include <iostream>
using namespace std;

// Part a) Iterative multiplication
int iterative_multiplication(int a, int b) {
  int result = a;
  for (int i = 1; i <= b - 1; i++) {
    result += a;
  }
  return result;
}

// Original recursive multiplication (for comparison)
int recursive_multiplication(int a, int b) {
  if (b == 1) {
    return a;
  } else {
    return a + recursive_multiplication(a, b - 1);
  }
}

// Main function to test
int main() {
  int a = 3, b = 4;

  // Test iterative multiplication
  cout << "Iterative: " << a << " * " << b << " = ";
  int iter_result = iterative_multiplication(a, b);
  cout << iter_result << endl;

  // Test original recursive multiplication
  cout << "Recursive: " << a << " * " << b << " = ";
  int rec_result = recursive_multiplication(a, b);
  cout << rec_result << endl;

  // Demonstrate part b issue (infinite recursion if uncommented)
  // int alt_result = recursive_multiplication_alt(a, b); // Would cause stack overflow
  cout << "\nPart b explanation: The definition a*b = a(b+1) - a increases b, "
    << "leading to infinite recursion with no natural base case." << endl;

  return 0;
}

