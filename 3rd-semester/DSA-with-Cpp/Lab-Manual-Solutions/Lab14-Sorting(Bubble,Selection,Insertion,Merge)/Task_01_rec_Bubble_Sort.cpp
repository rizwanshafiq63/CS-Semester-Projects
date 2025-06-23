// Lab Task 1: Implement a recursive Bubble sort.

#include <iostream>
using namespace std;

// Function to perform recursive Bubble Sort
void recursiveBubbleSort(int arr[], int n) {
  // Base case: If only one element, return
  if (n == 1)
    return;

  // One pass of Bubble Sort
  for (int i = 0; i < n - 1; i++) {
    if (arr[i] > arr[i + 1])
      swap(arr[i], arr[i + 1]);
  }

  // Recursive call for remaining array
  recursiveBubbleSort(arr, n - 1);
}

int main() {
  int arr[] = {64, 25, 12, 22, 11};
  int size = sizeof(arr) / sizeof(arr[0]);

  cout << "Original array: ";
  for (int i = 0; i < size; i++)
    cout << arr[i] << " ";
  cout << endl;

  recursiveBubbleSort(arr, size);

  cout << "Sorted array: ";
  for (int i = 0; i < size; i++)
    cout << arr[i] << " ";
  cout << endl;

  return 0;
}

