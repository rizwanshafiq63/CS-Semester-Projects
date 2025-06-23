/* Design a Hospital Registration system for patients using Priority Queue.
a.Assume a struct that you think is appropriate for such a system.
b.Take the priority factor, the condition of patient.
c.Design it using the above implemented system of Priority Queue.*/

#include <iostream>
#include <string>
using namespace std;

struct Patient {
  string name, condition;
  int age;

  int priority;  //high means more critical
};

//maxheap Priority Queue
Patient heap[50];
int TheSize = -1;

int parent(int i) {
  return (i - 1) / 2;   
}

int leftChild(int i) {
  return ((2 * i) + 1);  
}

int rightChild(int i) {
  return ((2 * i) + 2);
}

void shiftUp(int i) {
  while (i > 0 && heap[parent(i)].priority < heap[i].priority) {
    swap(heap[i], heap[parent(i)]);
    i = parent(i);
  }
}

void shiftDown(int i) {
  int maxIndex = i;
  int l = leftChild(i);
  if (l <= TheSize && heap[l].priority > heap[maxIndex].priority) {
    maxIndex = l;
  }
  int r = rightChild(i);
  if (r <= TheSize && heap[r].priority > heap[maxIndex].priority) {
    maxIndex = r;
  }
  if (i != maxIndex) {
    swap(heap[i], heap[maxIndex]);
    shiftDown(maxIndex);
  }
}

// Insert Patient 
void insertPatient(Patient p) {
  TheSize++;
  heap[TheSize] = p;
  shiftUp(TheSize);
}

//remove and return highest priority patient
Patient removeMax() {
  if (TheSize < 0) {
    cout << "No patients in the queue.\n";
    return {"None", "N/A", 0, -1};
  }
  Patient top = heap[0];
  heap[0] = heap[TheSize];
  TheSize--;
  shiftDown(0);
  return top;
}

void displayPatients() {
  if (TheSize < 0) {
    cout << "No patients registered."<<endl;
    return;
  }
  cout << "\n--- Patient Queue ---"<<endl;
  for (int i = 0; i <= TheSize; i++) {
    cout << i + 1 << ". " << heap[i].name << " | Age: " << heap[i].age << " | Condition: " << heap[i].condition << " | Priority: " << heap[i].priority << endl;
  }
  cout << "----------------------------------------------------------------"<<endl;
}

// Main
int main() {
  int choice;
  while (true) {
    cout << "\n--------Hospital Patient Registration---------"<<endl;
    cout << "1. Register Patient\n2. Call Next Patient\n3. Show All Patients\n4. Exit\nChoose: ";
    cin >> choice;

    if (choice == 1) {
      Patient p;
      cout << "Enter patient name: ";
      cin.ignore();

      getline(cin, p.name);
      cout << "Enter age: ";
      cin >> p.age;
      cout << "Enter condition (e.g. Normal, Serious, Critical): ";

      cin.ignore();
      getline(cin, p.condition);
      cout << "Enter priority (1=Low, 5=High): ";
      cin >> p.priority;

      insertPatient(p);
      cout << "Patient registered successfully>>>>>"<<endl;
    } else if (choice == 2) {
      Patient next = removeMax();
      if (next.priority != -1) {
        cout << "\nCalling next patient:\n";
        cout << "Name: " << next.name << "\nAge: " << next.age << "\nCondition: " << next.condition << "\n";
      }
    } else if (choice == 3) {
      displayPatients();
    } else if (choice == 4) {
      cout << "Exiting......>>"<<endl;
      break;
    } else {
      cout << "Invalid choice>>"<<endl;
    }
  }

  return 0;
}


