/* Write algorithms (for insertion and deletion) that implement two queues in one array where first queue will start from 0th position and second queue will start from last position of the array. */

#include <iostream>
using namespace std;

const int MAX_SIZE = 10; // Array size

class DoubleQueue {
private:
  int data[MAX_SIZE];
  int front1, rear1; // Queue 1
  int front2, rear2; // Queue 2
public:
  DoubleQueue() {
    front1 = 0; rear1 = -1;    // Queue 1 starts empty
    front2 = MAX_SIZE - 1; rear2 = MAX_SIZE; // Queue 2 starts empty
  }

  bool isFull() {
    //return rear1 + 1 >= rear2;
    return (rear1 + 1 >= rear2) && rear1 != -1 && rear2 != MAX_SIZE;
  }

  bool isQueue1Empty() {
    return rear1 < front1;
  }

  bool isQueue2Empty() {
    return rear2 > front2;
  }

  void enqueueQueue1(int item) {
    if (isFull()) {
      cout << "Array is full, cannot enqueue " << item <<" to Queue 1" << endl;
      return;
    }
    data[++rear1] = item;
  }

  int dequeueQueue1() {
    if (isQueue1Empty()) {
      cout << "Queue 1 is empty" << endl;
      return -1;
    }
    int item = data[front1];
    for (int i = front1; i < rear1; i++) {
      data[i] = data[i + 1];
    }
    rear1--;
    return item;
  }

  void enqueueQueue2(int item) {
    if (isFull()) {
      cout << "Array is full, cannot enqueue " << item << " to Queue 2" << endl;
      return;
    }
    data[--rear2] = item;
  }

  int dequeueQueue2() {
    if (isQueue2Empty()) {
      cout << "Queue 2 is empty" << endl;
      return -1;
    }
    int item = data[front2];
    for (int i = front2; i > rear2; i--) {
      data[i] = data[i - 1];
    }
    rear2++;
    return item;
  }

  void print() {
    cout << "Queue 1 (front to rear): ";
    if (isQueue1Empty()) {
      cout << "Empty";
    } else {
      for (int i = front1; i <= rear1; i++) {
        cout << data[i] << " ";
      }
    }
    cout << endl;

    cout << "Queue 2 (front to rear): ";
    if (isQueue2Empty()) {
      cout << "Empty";
    } else {
      for (int i = front2; i >= rear2; i--) {
        cout << data[i] << " ";
      }
    }
    cout << endl;
  }
};

// Main function to test
int main() {
  DoubleQueue dq;

  // Test Queue 1
  dq.enqueueQueue1(1);
  dq.enqueueQueue1(2);
  dq.enqueueQueue1(3);
  cout << "After enqueuing 1, 2, 3 to Queue 1:" << endl;
  dq.print();

  // Test Queue 2
  dq.enqueueQueue2(4);
  dq.enqueueQueue2(5);
  cout << "After enqueuing 4, 5 to Queue 2:" << endl;
  dq.print();

  // Dequeue from Queue 1
  cout << "Dequeued from Queue 1: " << dq.dequeueQueue1() << endl;
  dq.print();

  // Dequeue from Queue 2
  cout << "Dequeued from Queue 2: " << dq.dequeueQueue2() << endl;
  dq.print();

  // Test full condition
  dq.enqueueQueue1(6);
  dq.enqueueQueue1(7);
  dq.enqueueQueue1(8);
  dq.enqueueQueue2(4);
  dq.enqueueQueue2(1);
  dq.enqueueQueue2(2);
  dq.enqueueQueue1(9); // Should fill up
  dq.enqueueQueue1(10); // Should fail
  dq.enqueueQueue2(3); // Should fail
  cout << "After filling Queue 1:" << endl;
  dq.print();

  return 0;
}

