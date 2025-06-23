#include <iostream>
using namespace std;

// Function to partition the array
int partition(int arr[], int low, int high) {
  int pivot = arr[high]; // choose the last element as pivot
  int i = low - 1; // index of smaller element

  for (int j = low; j < high; j++) {
    if (arr[j] < pivot) {
      i++; // increment index of smaller element
      swap(arr[i], arr[j]);
    }
  }

  // place the pivot at the correct position
  swap(arr[i + 1], arr[high]);
  return i + 1;
}

// Recursive QuickSort function
void quickSort(int arr[], int low, int high) {
  if (low < high) {
    // partition the array
    int pi = partition(arr, low, high);

    // recursively sort left and right subarrays
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
  }
}

// Helper function to print the array
void printArray(int arr[], int size) {
  for (int i = 0; i < size; i++)
    cout << arr[i] << " ";
  cout << endl;
}

// Main function
int main() {
  int arr[] = {64, 25, 12, 22, 11};
  int n = sizeof(arr) / sizeof(arr[0]);

  cout << "Original array: ";
  printArray(arr, n);

  quickSort(arr, 0, n - 1);

  cout << "Sorted array using Quick Sort: ";
  printArray(arr, n);

  return 0;
}


