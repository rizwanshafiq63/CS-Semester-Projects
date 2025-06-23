// TASK-2: AVL Tree
// Real-World Scenario:
// Student Records Management System: AVL Tree is used to maintain student records
// by roll numbers. It keeps the tree balanced so searching, inserting, and deleting remain efficient.

#include <cstring>
#include <iostream>
#include <queue>
using namespace std;

struct node {
  int rollNo;         // Roll number of student
  char name[50];      // Name of student
  node *left, *right;
  int ht;
};

// Method 01: Height using height of left and right children
int height(node *T) {
  int lh, rh;
  if (T == NULL) return 0;
  lh = T->left ? 1 + T->left->ht : 0;
  rh = T->right ? 1 + T->right->ht : 0;
  return lh > rh ? lh : rh;
}

// Method 02: Recursive height
int Height(node *p) {
  if (p == NULL) return 0;
  int x = Height(p->left);
  int y = Height(p->right);
  return x > y ? x + 1 : y + 1;
}

int balanceFactor(node* T) {
  return T == NULL ? 0 : Height(T->left) - Height(T->right);
}

// Rotations
node* rotateLeft(node* x) {
  node* y = x->right;
  x->right = y->left;
  y->left = x;
  x->ht = height(x);
  y->ht = height(y);
  return y;
}

node* rotateRight(node* x) {
  node* y = x->left;
  x->left = y->right;
  y->right = x;
  x->ht = height(x);
  y->ht = height(y);
  return y;
}

node* LL(node* T) {
  return rotateRight(T);
}

node* RR(node* T) {
  return rotateLeft(T);
}

node* LR(node* T) {
  T->left = rotateLeft(T->left);
  return rotateRight(T);
}

node* RL(node* T) {
  T->right = rotateRight(T->right);
  return rotateLeft(T);
}

// Insertion
node* insert(node* T, int roll, const char* name) {
  if (T == NULL) {
    T = new node;
    T->rollNo = roll;
    strcpy(T->name, name);
    T->left = T->right = NULL;
    T->ht = 0;
    return T;
  } else if (roll < T->rollNo) {
    T->left = insert(T->left, roll, name);
    if (balanceFactor(T) == 2) {
      if (roll < T->left->rollNo)
        T = LL(T);
      else
        T = LR(T);
    }
  } else if (roll > T->rollNo) {
    T->right = insert(T->right, roll, name);
    if (balanceFactor(T) == -2) {
      if (roll > T->right->rollNo)
        T = RR(T);
      else
        T = RL(T);
    }
  }
  T->ht = height(T);
  return T;
}

// Inorder Traversal
void inorder(node* T) {
  if (T) {
    inorder(T->left);
    cout << T->rollNo << " - " << T->name << endl;
    inorder(T->right);
  }
}

// Level Order Traversal
void levelOrder(node* root) {
  if (root == NULL) return;
  queue<node*> q;
  q.push(root);
  while (!q.empty()) {
    node* curr = q.front(); q.pop();
    cout << curr->rollNo << " - " << curr->name << "  ";
    if (curr->left) q.push(curr->left);
    if (curr->right) q.push(curr->right);
  }
  cout << endl;
}

int main() {
  node* root = NULL;
  root = insert(root, 102, "Ali");
  root = insert(root, 101, "Zain");
  root = insert(root, 105, "Sara");
  root = insert(root, 104, "Omar");
  root = insert(root, 103, "Areeba");

  cout << "\nInorder Traversal (Sorted by Roll No):\n";
  inorder(root);

  cout << "\nLevel Order Traversal (AVL Tree Structure):\n";
  levelOrder(root);

  return 0;
}

