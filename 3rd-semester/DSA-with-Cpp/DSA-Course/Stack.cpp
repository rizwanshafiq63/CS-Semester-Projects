#include <climits>
#include <iostream>
#include <unordered_map>
#include <stack>
#include <vector>
using namespace std;

// LeetCode question: 155. Min Stack
// Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
// Implement a min stack using a stack of pairs where the first element is the value and the second element is the minimum value in the stack.
class MinStack {
  stack<pair<int, int>> s; // stack to store the elements and the minimum element
public:
  MinStack() {
    // constructor
  }

  void push(int val) {
    if(s.empty()) {
      s.push({val, val});
    } else {
      s.push({val, min(val, s.top().second)});
    }
  }

  void pop() {
    s.pop();   
  }

  int top() {
    return s.top().first;
  }

  int getMin() {
    return s.top().second;
  }
  // Time complexity: O(1) for all operations
  // Space complexity: O(2xn) for the stack
};

class BetterMinStack {
  stack<long long int> s; // stack to store the elements
  long long int minVal; // variable to store the minimum value
public:
  BetterMinStack() {
    // constructor
    minVal = INT_MAX;
  }

  void push(int val) {
    if(s.empty()) {
      s.push(val);
      minVal = val;
    } else {
      if(val < minVal) {
        // Formula: val'(val to push) = 2 * new val - old minVal
        s.push(2 * (long long int)val - minVal);
        minVal = val;
      } else {
        s.push(val);
      }
    }
  }

  void pop() {
    if(s.top() < minVal) {
      // Formula: old minVal = 2 * new minVal - val'(val popped)
      minVal = 2 * minVal - s.top();
    }
    s.pop();
  }

  int top() {
    if(s.top() < minVal) {
      return minVal;
    }
    return s.top();
  }

  int getMin() {
    return minVal;
  }
  // Time complexity: O(1) for all operations
  // Space complexity: O(n) for the stack
};

// LeetCode question: 20. Valid Parentheses
// Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if:
  // 1. Open brackets must be closed by the same type of brackets.
  // 2. Open brackets must be closed in the correct order.
bool isValidParenthesis(string str) {
  stack<char> s; // stack to store the opening brackets
  for(int i = 0; i < str.size(); i++) {
    if(str[i] == '(' || str[i] == '{' || str[i] == '[') {
      s.push(str[i]);
    } else {
      if(s.empty()) {
        return false;
      }
      char top = s.top();
      if((str[i] == ')' && top != '(') || (str[i] == '}' && top != '{') || (str[i] == ']' && top != '[')) {
        return false;
      }
      s.pop();
    }
  }
  return s.empty();
}


// LeetCode question: 496. Next Greater Element I
// You are given two arrays nums1 and nums2, where nums1 is a subset of nums2. Find the next greater element for each element in nums1 from nums2.
vector<int> ngeLeetCodeQuestion() {
  // nums1 = [4, 1, 2], nums2 = [1, 3, 4, 2]
  // Find the next greater element for each element in nums1 from nums2 where elements in nums1 are present in nums2
  vector<int> nums1 = {4, 1, 2}, nums2 = {1, 3, 4, 2};

  // Better approach: 1st find the next greater element for nums2, then use a map to store the next greater element for nums2 
  unordered_map<int, int> m; // map to store the next greater element for nums2
  stack<int> s;
  for(int i = nums2.size() - 1; i >= 0; i--) {
    while(s.size() > 0 && s.top() <= nums2[i]) {
      s.pop();
    }
    if(s.empty()) {
      m[nums2[i]] = -1;
    } else {
      m[nums2[i]] = s.top();
    }
    s.push(nums2[i]);
  }

  vector<int> ans;
  for(int i = 0; i < nums1.size(); i++) {
    ans.push_back(m[nums1[i]]);
  }

  // print the result
  for(int val : ans) {
    cout << val << " ";
  }
  cout << endl;
  return ans;
  // Time complexity: O(n)
  // Space complexity: O(n)
}

vector<int> previousSmallerElement() {
  vector<int> arr = {3, 1, 0, 8, 6}; // Example input
  
  // previous smaller element
  stack<int> s;
  vector<int> ans(arr.size(), 0); 

  for(int i = 0; i < arr.size(); i++) {
    while(s.size() > 0 && s.top() >= arr[i]) {
      s.pop();
    }
    if(s.empty()) {
      ans[i] = -1;;
    } else {
      ans[i] = s.top();
    }
    s.push(arr[i]);
  }

  // print the result
  for(int val : ans) {
    cout << val << " ";
  }
  cout << endl;
  return ans;
}

// LeetCode question: 503. Next Greater Element II

int main (int argc, char *argv[]) {
  // main code here
  return 0;
}
