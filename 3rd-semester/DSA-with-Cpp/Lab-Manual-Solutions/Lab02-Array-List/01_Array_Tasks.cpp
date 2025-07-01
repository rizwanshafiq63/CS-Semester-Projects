#include <iostream>
using namespace std;

const int SIZE = 5;
int arr[SIZE];
int startIndex = -1;
int lastIndex = -1;

// ====================
//   VALIDATION CASES
// ====================

bool isEmpty(){
  return lastIndex == -1;
}

bool isFull(){
  return (lastIndex - startIndex + 1) >= SIZE;
}

bool isEmptyFromStart(){
  return startIndex > 0;
}

bool isEmptyFromLast(){
  return lastIndex < SIZE - 1;
}

int indexOfSpecific(int value){
  if (isEmpty()) { return -1; }
  for(int i = startIndex; i <= lastIndex; i++){
    if(arr[i] == value){
      return i;
    }
  }
  return -1;
}

// ======================
//   METHODS TO DEVELOP
// ======================

void insertAtEnd(int value){
  if (isFull()) {
    cout<<"Array is Full"<<endl;
    return;
  }
  if (isEmpty()) {
    startIndex = 0;
  }  
  arr[++lastIndex] = value;
  cout<<"Inserted "<<value<<" at index "<<lastIndex<<endl;
}

void insertAtStart(int value){
  if (isFull()) {
    cout<<"Array is Full"<<endl;
    return;
  } else if (isEmpty()) {
    startIndex = 0;
    arr[++lastIndex] = value;
    cout<<"Inserted "<<value<<" at index "<<lastIndex<<endl;
  } else if (isEmptyFromStart()) {
    arr[--startIndex] = value;
    cout<<"Inserted "<<value<<" at index "<<startIndex<<endl;
  } else if (isEmptyFromLast()) {
    //shift elements to right to make space
    for(int i = lastIndex; i >= startIndex; i--){
      arr[i + 1]= arr[i]; 
    }
    arr[startIndex] = value;
    lastIndex++;
  }
}

void insertBeforeSpecific(int value, int specific){
  // check it the specific value exist in the array
  int index = indexOfSpecific(specific);
  if (index == -1){
    cout<<"The specfic valus you are trying to reach does not exist in the array"<<endl;
    return;
  }
  // If the value exist then do this:
  if (isFull()) {
    cout<<"Array is Full"<<endl;
    return;
  } else if (isEmptyFromStart() || isEmptyFromLast()) {
    if (isEmptyFromStart()) {
      //Left Shift
      for(int i = startIndex; i < index; i++){
        arr[i - 1] = arr[i];
      }
      startIndex--;
      arr[index - 1] = value;
    } else if (isEmptyFromLast()) {
      //Right Shift
      for(int i = lastIndex; i >= index; i--){
        arr[i + 1] = arr[i];
      }
      lastIndex++;
      arr[index] = value;
    }
    cout<<"Inserted "<<value<<" before "<<specific<<endl;
  }
}

void insertAfterSpecific(int value, int specific){
  int index = indexOfSpecific(specific);
  if (index == -1) {
    cout<<"The specific value does not exist in the array"<<endl;
    return;
  }
  if (isFull()) {
    cout<<"Array is Full"<<endl;
    return;
  } else if (isEmptyFromStart() || isEmptyFromLast()) {
    if (isEmptyFromStart()) {
      // Left Shift
      for (int i = startIndex; i <= index; i++) {
        arr[i - 1] = arr[i];
      }
      startIndex--;
      arr[index] = value;
    } else if (isEmptyFromLast()) {
      // Right Shift
      for (int i = lastIndex; i > index; i--) {
        arr[i + 1] = arr[i];
      }
      lastIndex++;
      arr[index + 1] = value;
    }
    cout<<"Inserted "<<value<<" after "<<specific<<endl;
  }
}

void deleteFromEnd(){
  if (isEmpty()) {
    cout<<"Array is Empty."<<endl;
    return;
  } else if (startIndex == lastIndex){ //1 element in array
    startIndex = lastIndex = -1;
  } else {
    cout<<"Deleted "<<arr[lastIndex]<<" from end."<<endl;
    lastIndex--;
  }
}

void deleteFromStart(){
  if (isEmpty()) {
    cout<<"Array is Empty."<<endl;
    return;
  } else if (startIndex == lastIndex) {
    startIndex = lastIndex = -1;
  } else {
    cout<<"Deleted "<<arr[startIndex]<<" from start."<<endl;
    startIndex++;
  }
}

void deleteBeforeSpecific(int specific){
  int index = indexOfSpecific(specific);
  cout<<"Index of specific: "<<index<<endl;
  if ((index == -1) || (index == startIndex)) {
    cout<<"No element before "<<specific<<" exist to delete OR "<<specific<<" not found."<<endl;
    return;
  } else {
    cout<<"Deleted "<<arr[index -1]<<" before "<<specific<<"."<<endl;
    // Right Shift
    for (int i = index - 1; i > startIndex ; i--) {
      arr[i] = arr[i - 1];
    }
    startIndex++;
  }
}

void deleteAfterSpecific(int specific){
  int index = indexOfSpecific(specific);
  cout<<"Index of Specific: "<<index<<endl;
  if ((index == -1) || (index == lastIndex) ) {
    cout <<"No element after "<<specific<<" exist to delete OR "<<specific<<" not found."<<endl;
    return;
  } else {
    cout<<"Deleted "<<arr[index + 1]<<" after "<<specific<<"."<<endl;
    // Left Shift
    for (int i = index + 1; i < lastIndex; i++) {
      arr[i] = arr[i + 1];
    }
    lastIndex--;
  }
}

void display(){
  if (isEmpty()) {
    cout<<"Array is Empty."<<endl;
    return;
  }
  cout<<"Array Elements: ";
  for (int i = startIndex ; i <= lastIndex; i++) {
    cout<<arr[i]<<" ";
  }
  cout<<endl;
}

// ===============
//   MAIN METHOD
// ===============

int main () {
  int choice, value, specific;

  while (true) {
    cout << "\n----- Options Available -----\n";
    cout << "1. Insert At End\n";
    cout << "2. Insert At Start\n";
    cout << "3. Insert Before Specific Value\n";
    cout << "4. Insert After Specific Value\n";
    cout << "5. Delete From End\n";
    cout << "6. Delete From Start\n";
    cout << "7. Delete Before Specific Value\n";
    cout << "8. Delete After Specific Value\n";
    cout << "9. Display Array\n";
    cout << "0. Exit\n";
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        cout << "Enter value to insert at end: ";
        cin >> value;
        insertAtEnd(value);
        break;
      case 2:
        cout << "Enter value to insert at start: ";
        cin >> value;
        insertAtStart(value);
        break;
      case 3:
        cout << "Enter value to insert: ";
        cin >> value;
        cout << "Now enter the specific value before which to insert: ";
        cin >> specific;
        insertBeforeSpecific(value, specific);
        break;
      case 4:
        cout << "Enter value to insert: ";
        cin >> value;
        cout << "Now enter the specific value before which to insert: ";
        cin >> specific;
        insertAfterSpecific(value, specific);
        break;
      case 5:
        deleteFromEnd();
        break;
      case 6:
        deleteFromStart();
        break;
      case 7:
        cout << "Enter the specific value before which to delete: ";
        cin >> specific;
        deleteBeforeSpecific(specific);
        break;
      case 8:
        cout << "Enter the specific value after which to delete: ";
        cin >> specific;
        deleteAfterSpecific(specific);
        break;
      case 9:
        display();
        break;
      case 0:
        cout << "Exiting program. Goodbye!\n";
        return 0; // It will exit the loop and program
      default:
        cout << "Invalid choice! Please enter a valid option.\n";
    }
  }
}

