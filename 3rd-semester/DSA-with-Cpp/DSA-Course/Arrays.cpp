#include "iostream"
#include <utility>
using namespace std;

const int SIZE = 5; //Defined size globally so no need to pass everytime in methods

void printArray(int arr[]) {
  for (int i = 0; i < SIZE; i++) {
    cout<<arr[i]<<" ";
  } cout<<endl;
}

void changeArray(int arr[]) {
  for (int i = 0; i < SIZE; i++) {
    arr[i] = 2 * arr[i]; //double each value
  }
}

int linearSearch(int arr[], int target) {
  for (int i = 0; i < SIZE; i++) {
    if (arr[i] == target) {
      return i; //Found
    }
  }
  return -1; //Not Found
}

void reverseArray(int arr[]) {
  int start = 0, end = SIZE-1;
  while(start < end) {
    swap(arr[start], arr[end]);
    start++, end--;
  }
}

int sumOfArray(int arr[]) {
  int sum = 0;
  for (int i = 0; i < SIZE; i++) {
    sum += arr[i]; // product *= arr[i];
  } return sum;
}

void swapMinMax(int arr[], int size) {
  if (size < 2) {
    cout << "Array is too small to swap elements!" << endl;
    return;
  }
  int minIndex = 0, maxIndex = 0;
  // Find min and max indices
  for (int i = 1; i < size; i++) {
    if (arr[i] < arr[minIndex]) {
      minIndex = i;
    }
    if (arr[i] > arr[maxIndex]) {
      maxIndex = i;
    }
  }
  // Swap min and max elements
  int temp = arr[minIndex];
  arr[minIndex] = arr[maxIndex];
  arr[maxIndex] = temp;
  // Print the updated array
  printArray(arr);
}

void printUniqueValues(int arr[], int size) {
  cout << "Unique values: ";
  for (int i = 0; i < size; i++) {
    int count = 0;
    // Count occurrences of arr[i]
    for (int j = 0; j < size; j++) {
      if (arr[i] == arr[j]) {
        count++;
      }
    }
    // Print only if count is 1 (unique value)
    if (count == 1) {
      cout << arr[i] << " ";
    }
  }
  cout << endl;
}

void printIntersection(int A[], int sizeA, int B[], int sizeB) {
  int result[sizeA]; // Array to store intersection elements
  int index = 0;     // To keep track of unique elements in intersection

  for (int i = 0; i < sizeA; i++) {
    for (int j = 0; j < sizeB; j++) {
      if (A[i] == B[j]) { 
        // Check if already added to result (avoid duplicates)
        bool alreadyAdded = false;
        for (int k = 0; k < index; k++) {
          if (result[k] == A[i]) {
            alreadyAdded = true;
            break;
          }
        }

        if (!alreadyAdded) {
          result[index++] = A[i]; // Store unique intersection element
        }
      }
    }
  }
}

int main () {
  int arr[SIZE];

  // ==========================
  // DEFAULT FUNCTIONS IN C++
  // ==========================
  // Largest Possible Value Default in C++ (plus infinity)-> INT_MAX
  // int smallest = +infinity = INT_MAX -> INT_MIN is vice versa for -ve infinity
  // smallest = min(arr[i], smallest) -> min, max by default  

  //Array SIZE calculation
  int arrUsedBytes = sizeof(arr); // will gice 20
  int arrSize = sizeof(arr) / sizeof(int); // 20 / 4 = 5

  // Input into Array
  cout<<"Enter Data for arr: "<<endl;
  for (int i = 0; i < arrSize; i++) {
    cout<<"arr["<<i<<"] : ";
    cin>>arr[i];
  }

  changeArray(arr); // Pass-By-Reference (changes appear in main() too)

  printArray(arr); // Printing array

  // LINEAR SEARCH ALGORITHM
  int target;
  cout<<"LINEAR SEARCH -> Enter Num: ";
  cin>>target;
  int index = linearSearch(arr, target);
  cout<<"Num: "<<target<<" found at index: "<<index<<endl;

  // INTERSECTION OF TWO ARRAYS
  int A[] = {1, 2, 3, 4, 5, 3};  // Example array 1 (with duplicate 3)
  int B[] = {3, 4, 5, 6, 7, 3};  // Example array 2 (with duplicate 3)
  int sizeA = sizeof(A) / sizeof(A[0]);
  int sizeB = sizeof(B) / sizeof(B[0]);
  printIntersection(A, sizeA, B, sizeB);

  // Printing Unique Values
  int arrU[] = {1, 2, 3, 1, 2, 3, 4, 5};
  int sizeU = sizeof(arrU) / sizeof(arrU[0]);
  printUniqueValues(arrU, sizeU);

  return 0;
}
