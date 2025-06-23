#include <iostream>
using namespace std;

int main () {
  int x = 10;
  cout << "Address of x: " << &x << endl;

  // ============
  //   POINTERS  -> Store Address of other variables
  // ============
  int* xp = &x;
  cout << "Address of xp: " << &xp << endl;
  cout << "Value of xp: " << xp << endl;
  cout << "*xp: " << *xp << " x: " << x << endl;
   
  // POINTER TO POINTER
  int** xp2 = &xp; // ** tells it's storing address of another pointer
  // It's value = Address of xp and &xp2 = it's own address
  
  // DEREFERENCING OPERATOR -> * -> value at address
  cout << "Dereference Operator: *(&x): " << *(&x) << " and *(xp): " << *(xp) << endl;

  return 0;
}
