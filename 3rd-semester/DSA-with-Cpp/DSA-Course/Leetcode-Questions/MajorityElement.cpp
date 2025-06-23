#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int majorityElement(vector<int>& nums) {
  int n = nums.size();

  // 1. Brute_Force_approach -> O(n^2)
  /* for(int val : nums) {
    int freq = 0;
    for(int element : nums) {
      if (element == val) {
        freq++;
      }
    }
    if (freq > n/2) {
      return val;
    }
  } */

  // 2. Optimized_Form -> By Sorting O(nlogn) and finally O(nlogn + n)
  /* sort(nums.begin(), nums.end());
  int freq = 1, ans = nums[0];
  for (int i = 1; i < n; i++) {
    if (nums[i] == nums[i-1]) {
      freq++;
    } else {
      freq = 1;
      ans = nums[i];
    }
    if (freq > n/2) {
      return ans;
    }
  } */

  // 3. Moore's_Voting_Algorithm -> O(n)
  int freq = 0, ans = 0;
  for (int i = 0; i < n; i++) {
    if (freq == 0) {
      ans = nums[i];
    }
    if (ans == nums[i]) {
      freq++;
    } else {
      freq--;
    }
  }
  if (freq >= 0 ) {
    return ans;
  }

  return -1;
}

int main () {
  // Prob. 169
  // MajElement: It is the element that appears moe then floor n/2 times in array (n is size of array)
  // Floor: 8 / 2 = 4, 9 / 2 = 4.5 -> 4 , so the element should exist > 4 times


  return 0;
}
