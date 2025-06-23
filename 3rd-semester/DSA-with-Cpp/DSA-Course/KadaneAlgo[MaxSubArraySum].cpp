#include <algorithm>
#include <climits>
#include <iostream>
using namespace std;

// =====================
//   LEETCODE PROB. 53
// =====================

int main () {
  int n = 5;
  int arr[5] = {1, 2, 3, 4, 5};

  // This will give all possible Sub-Arrays -> O(n^3) [Time Complexity]
  for (int start = 0; start < n; start++) {
    for (int end = start; end < n; end++) {
      for (int i = start; i <= end; i++) {
        cout<<arr[i];
      }
      cout<<" ";
    }
    cout<<endl;
  }

  //Brute Force Approach -> O(n^2) [Time Complexity]
  int maxSum = INT_MIN;
  for (int start = 0; start < n; start++) {
    int currentSum = 0;
    for (int end = start; end < n; end++) {
      currentSum += arr[end];
      maxSum = max(currentSum, maxSum);
    }
  }
  cout<<"Max Sub-Array Sum: "<<maxSum<<endl;
  
  // Kadane's Algorithm -> O(n) [Time Complexity]
  // Prob. 53 -> LeetCode (with vector)
  int arr1[7] = {3,-4,5,4,-1,7,-8};
  int size = sizeof(arr1) / sizeof(arr1[0]);
  int currSum = 0, maximumSum = INT_MIN;
  for (int i = 0; i < size-1; i++) {
    currSum += arr1[i];
    maximumSum = max(currSum, maximumSum);
    if (currSum < 0) {
      currSum = 0; // Reset it 
    }
  }
  cout<<"Kadane's Algorithm output: "<<maximumSum<<endl;

  return 0;
}
