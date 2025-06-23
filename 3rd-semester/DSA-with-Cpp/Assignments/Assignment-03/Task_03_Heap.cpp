// Task-3: Heap Tree
// Real-World Scenario: Print Job Manager using Max Heap

#include <iostream>
#include <utility>
using namespace std;

int H[50];
int heapSize = -1;

// Parent, left and right child
int parent(int i) { return (i - 1) / 2; }
int leftChild(int i) { return (2 * i) + 1; }
int rightChild(int i) { return (2 * i) + 2; }

// Shift Up (Maintain Max Heap)
void shiftUp(int i) {
  while (i > 0 && H[parent(i)] < H[i]) {
    swap(H[parent(i)], H[i]);
    i = parent(i);
  }
}

// Insert new print job
void insertJob(int priority) {
  heapSize++;
  H[heapSize] = priority;
  shiftUp(heapSize);
}

// Shift Down (Maintain Max Heap)
void shiftDown(int i) {
  int maxIndex = i;
  int l = leftChild(i);
  if (l <= heapSize && H[l] > H[maxIndex]) maxIndex = l;
  int r = rightChild(i);
  if (r <= heapSize && H[r] > H[maxIndex]) maxIndex = r;
  if (i != maxIndex) {
    swap(H[i], H[maxIndex]);
    shiftDown(maxIndex);
  }
}

// Process highest-priority job
int processJob() {
  int result = H[0];
  H[0] = H[heapSize];
  heapSize--;
  shiftDown(0);
  return result;
}

// Print all pending jobs
void printQueue() {
  for (int i = 0; i <= heapSize; ++i) {
    cout << H[i] << " ";
  }
  cout << endl;
}

// Convert Max Heap to Min Heap for demo
void shiftDownMin(int i) {
  int minIndex = i;
  int l = leftChild(i);
  if (l <= heapSize && H[l] < H[minIndex]) minIndex = l;
  int r = rightChild(i);
  if (r <= heapSize && H[r] < H[minIndex]) minIndex = r;
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

int main() {
  // Inserting print jobs
  insertJob(40); // High priority job
  insertJob(10);
  insertJob(30);
  insertJob(50); // Highest priority job
  insertJob(20);

  cout << "Current Print Queue (Max-Heap): ";
  printQueue();

  // Processing jobs
  cout << "Processing Job with Priority: " << processJob() << endl;
  cout << "Queue after processing: ";
  printQueue();

  // Optional: Show Min-Heap version (for lowest priority first)
  cout << "Queue as Min-Heap (for demo): ";
  heapifyMin();
  printQueue();

  return 0;
}

