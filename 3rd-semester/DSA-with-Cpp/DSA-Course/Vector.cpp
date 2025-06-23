#include <iostream>
#include <vector> //if not added then vector will show error
using namespace std;

// Linear Search Function
int linearSearch(vector<int>& vec1, int key) {
  for (int i = 0; i < vec1.size(); i++) {
    if (vec1[i] == key) {
      return i; // Return index of the found element
    }
  }
  return -1; // Return -1 if not found
}

// Reverse Vector Function
void reverseVector(vector<int>& vec1) {
  int left = 0, right = vec1.size() - 1;
  while (left < right) {
    swap(vec1[left], vec1[right]);
    left++;
    right--;
  }
}

// Function to Display Vector
void displayVector(const vector<int>& vec1) {
  for (int num : vec1) {
    cout << num << " ";
  }
  cout << endl;
}

int main () {
  // Arrays -> Static
  // Vectors -> Dynamic , can be resized as well
  // g++ -std=c++11 Vector.cpp && ./a.out

  // CREATING A VECTOR
  // vector<int> vec; // By default size = 0 
  vector<int> vec = {1,2,3}; // size = 3 default, but can be changed 
  // vector<int> vec(3,0) // 1st value (3) is size of vec & 2nd val(0) tell what should be put at each index of vec

  cout<<vec[0]<<endl;

  // FOR EACH LOOP -> VECTOR
  for(int value : vec) {
    cout<<value<<endl;
  }

  // ======================
  // FUNCTIONS FOR VECTORS
  // ======================
  // 1. SIZE
  cout<<"Size = " << vec.size() <<endl;

  // 2. PUSH BACK -> pushes a value at the end of the vector
  vec.push_back(25); 
  vec.push_back(21);

  // 3. POP BACK -> Deletes a value from the end of vector
  // No need to tell the value as it will remove the last value
  vec.pop_back();

  // 4. FRONT -> Returns the first value
  // 5. BACK -> Returns the last value
  cout<<"First: "<< vec.front() <<" & Back: "<< vec.back()<<endl;

  // 6. AT -> Used for accessing a value at particular index
  cout<<vec.at(3)<<endl; // same as vec[i]

  // =======================
  // WORKING AND PROPERTIES
  // =======================
  /* Every time we push_Back a value into the vector, a new array of 2x size of the already existing vector is created and the this is now the new vector and old one is deleted.
   [1] vec...push_back(2) -> [1] * 2x -> [1,2] new vec, old deleted from memory
   [1,2] vec...push_back(3) -> [1,2] * 2x -> [1,2,3,-] new vec, old deleted, so on...
   => Size -> No of elements (3), Capacity -> Can store? (4) for [1,2,3,-] vec
   */
  cout<<"Vec Size: "<<vec.size()<<endl;
  cout<<"Vec Capacity: "<<vec.capacity()<<endl;

  // ======================
  // METHODS DEFINED BELOW
  // ======================
  vector<int> vec1 = {10, 20, 30, 40, 50};

  cout << "Original Vector: ";
  displayVector(vec1);

  // Searching for an element
  int key = 30;
  int index = linearSearch(vec1, key);
  if (index != -1)
    cout << key << " found at index " << index << endl;
  else
    cout << key << " not found in the vector." << endl;

  // Reversing the vector
  reverseVector(vec1);
  cout << "Reversed Vector: ";
  displayVector(vec1);

  return 0;
}


