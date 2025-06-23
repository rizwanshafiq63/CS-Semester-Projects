#include <iostream>
#include <utility>
using namespace std;

int H[50];
int heapSize = -1;

// Function to return the index of the parent node of a given node
int parent(int i) {
  return (i - 1) / 2;
}

// Function to return the index of the left child of the given node
int leftChild(int i) {
  return ((2 * i) + 1);
}

// Function to return the index of the right child of the given node
int rightChild(int i) {
  return ((2 * i) + 2);
}

// Function to shift up the node in order to maintain the heap property
void shiftUp(int i) {
  while (i > 0 && H[parent(i)] < H[i]) {
    // Swap parent and current node
    swap(H[parent(i)], H[i]);
    // Update i to parent of i
    i = parent(i);
  }
}

void insert(int p) {
  heapSize = heapSize + 1;
  H[heapSize] = p;
  // Shift Up to maintain heap property
  shiftUp(heapSize);
}

// Function to shift down the node in order to maintain the heap property
void shiftDown(int i) {
  int maxIndex = i;
  // Left Child
  int l = leftChild(i);
  if (l <= heapSize && H[l] > H[maxIndex]) {
    maxIndex = l;
  }
  // Right Child
  int r = rightChild(i);
  if (r <= heapSize && H[r] > H[maxIndex]) {
    maxIndex = r;
  }
  // If i not same as maxIndex
  if (i != maxIndex) {
    swap(H[i], H[maxIndex]);
    shiftDown(maxIndex);
  }
}

// Function to extract the element with maximum priority
int extractMax() {
  int result = H[0];
  // Replace the value at the root with the last leaf
  H[0] = H[heapSize];
  heapSize = heapSize - 1;
  // Shift down the replaced element to maintain the heap property
  shiftDown(0);
  return result;
}

// Print heap for visualization
void printHeap() {
  for (int i = 0; i <= heapSize; ++i) {
    cout << H[i] << " ";
  }
  cout << endl;
}

// M=Function to Heapify
void heapify() {
  for (int i = (heapSize - 1) / 2; i >= 0; --i) {
    shiftDown(i);
  }
}

// Function to convert it to Min Heap
void shiftDownMin(int i) {
  int minIndex = i;
  int l = leftChild(i);
  if (l <= heapSize && H[l] < H[minIndex]) {
    minIndex = l;
  }
  int r = rightChild(i);
  if (r <= heapSize && H[r] < H[minIndex]) {
    minIndex = r;
  }
  if (i != minIndex) {
    swap(H[i], H[minIndex]);
    shiftDownMin(minIndex);
  }
}
void heapifyMin() {
  for (int i = (heapSize - 1) / 2; i >= 0; --i) {
    shiftDownMin(i);
  }
}

// Example usage
int main() {
  insert(10);
  insert(4);
  insert(15);
  insert(20);
  insert(0);
  insert(8);

  cout << "Max-Heap: ";
  printHeap();

  cout << "Extracted Max: " << extractMax() << endl;
  cout << "Heap after extraction: ";
  printHeap();

  cout << "Min-Heap: ";
  heapifyMin();
  printHeap();

  return 0;
}


