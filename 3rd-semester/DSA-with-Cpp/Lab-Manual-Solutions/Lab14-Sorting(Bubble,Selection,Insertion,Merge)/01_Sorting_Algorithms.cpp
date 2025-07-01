#include <iostream>
#include <algorithm>
#include <list>
using namespace std;

/* BUBBLE SORT ALGORITHM:
1. Starting with the first element (index = 0/node = 1), compare the current element with the next element of the array.
2. If the current element is greater than the next element of the array, swap them.
3. If the current element is less than the next element, move to the next element. Repeat Step 1. */
/*
void bubbleSort(int arr[], int n) {
  int i, j, temp;
  for(i = 0; i < n; i++){
    for(j = 0; j < n-i-1; j++) {
      if (arr[j] > arr[j+1]) {
        // swap the elements
        temp = arr[j];
        arr[j] = arr[j+1];
        arr[j+1] = temp;
      }
    }
  }
} */
void bubbleSort(int arr[], int n) {
  int i, j, temp;
  for(i = 0; i < n; i++){
    for(j = i+1; j < n; j++) {
      if (arr[i] > arr[j]) {
        // swap the elements
        temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
      }
    }
  }
}

/* SELECTION SORT ALGORITHM:
1. Starting from the first element, we search the smallest element in the array, and replace it with the element in the first position.
2. We then move on to the second position, and look for smallest element present in the subarray, starting from index 1, till the last index.
3. We replace the element at the second position in the original array, or we can say at the first position in the subarray, with the second smallest element.
4. This is repeated, until the array is completely sorted. */

int findMin_Index(int a[], int size, int startIndex){
  int i = startIndex;
  int min = i;
  for(; i<size; i++){
    if(a[i] < a[min]){
      min = i;
    }
  }
  return min;
}

void swap_Elems(int a[], int i, int j){
  int temp = a[i];
  a[i] = a[j];
  a[j] = temp;
}

void select_andSort(int a[], int size){
  int minIndex;
  for(int i=0; i<size; i++){
    minIndex = findMin_Index(a, size ,i);
    swap_Elems(a, i, minIndex);
  }
}

/* INSERTION SORT ALGORITHM:
1. It is efficient for smaller data sets, but very inefficient for larger lists.
2. Insertion Sort is adaptive, that means it reduces its total number of steps if a partially sorted array is provided as input, making it efficient.
3. It is better than Selection Sort and Bubble Sort algorithms.
4. Its space complexity is less. Like bubble Sort, insertion sort also requires a single additional memory space.
5. It is a stable sorting technique, as it does not change the relative order of elements which are equal. */

void insertionSort(int arr[], int length){
  int i, j, key;
  for (i = 1; i < length; i++){
    j = i;
    while (j > 0 && arr[j - 1] > arr[j]){
      key = arr[j];
      arr[j] = arr[j - 1];
      arr[j - 1] = key;
      j--;
    }
  }
}

/* MERGE SORT ALGORITHM:
1. Divide the problem into multiple small problems.
2. Conquer the sub-problems by solving them. The idea is to break down the problem into atomic sub-problems, where they are actually solved.
3. Combine the solutions of the sub-problems to find the solution of the actual problem */

const int SIZE = 100; // Adjust as needed
int tempArray[SIZE];

void merge(int list[], int first, int mid, int last) {
  int firstA = first;
  int lastA = mid;
  int firstB = mid + 1;
  int lastB = last;
  int index = first;

  while (firstA <= lastA && firstB <= lastB) {
    if (list[firstA] < list[firstB])
      tempArray[index++] = list[firstA++];
    else
      tempArray[index++] = list[firstB++];
  }
  for (; firstA <= lastA; firstA++)
    tempArray[index++] = list[firstA];
  for (; firstB <= lastB; firstB++)
    tempArray[index++] = list[firstB];

  // Copy back to original array (sorted merge)
  index = first;
  for (int i = first; i <= last; i++) {
    list[i] = tempArray[i];
  }
}

void mergesort(int list[], int first, int last) {
  if (first < last) {
    int mid = (first + last) / 2;
    // Sort the 1st half of the list
    mergesort(list, first, mid);
    // Sort the 2nd half of the list
    mergesort(list, mid + 1, last);
    // Merge the two halves
    merge(list, first, mid, last);
  }
}

// MAIN METHOD
int main() {
  int original[] = {64, 25, 12, 22, 11};
  int n = sizeof(original) / sizeof(original[0]);

  // Bubble Sort
  int bubbleArr[SIZE];
  copy(original, original + n, bubbleArr);
  bubbleSort(bubbleArr, n);
  cout << "Bubble Sorted array: ";
  for (int i = 0; i < n; i++) cout << bubbleArr[i] << " ";
  cout << endl;

  // Selection Sort
  int selectionArr[SIZE];
  copy(original, original + n, selectionArr);
  select_andSort(selectionArr, n);
  cout << "Selection Sorted array: ";
  for (int i = 0; i < n; i++) cout << selectionArr[i] << " ";
  cout << endl;

  // Insertion Sort
  int insertionArr[SIZE];
  copy(original, original + n, insertionArr);
  insertionSort(insertionArr, n);
  cout << "Insertion Sorted array: ";
  for (int i = 0; i < n; i++) cout << insertionArr[i] << " ";
  cout << endl;

  // Merge Sort
  int mergeArr[SIZE];
  copy(original, original + n, mergeArr);
  mergesort(mergeArr, 0, n - 1);
  cout << "Merge Sorted array: ";
  for (int i = 0; i < n; i++) cout << mergeArr[i] << " ";
  cout << endl;

  return 0;
}

