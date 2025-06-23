// Task-1: Binary Search Tree (BST)
// Real-World Scenario: Phone Directory System

#include <iostream>
#include <string>
using namespace std;

struct Node {
  string name;
  string phone;
  Node *left, *right;

  Node(string n, string p) : name(n), phone(p), left(nullptr), right(nullptr) {}
};

Node* insert(Node* root, string name, string phone) {
  if (!root) return new Node(name, phone);
  if (name < root->name)
    root->left = insert(root->left, name, phone);
  else
    root->right = insert(root->right, name, phone);
  return root;
}

void inorder(Node* root) {
  if (root) {
    inorder(root->left);
    cout << root->name << " : " << root->phone << endl;
    inorder(root->right);
  }
}

int main() {
  Node* root = nullptr;
  root = insert(root, "Ali", "0300-1234567");
  root = insert(root, "Zara", "0311-7654321");
  root = insert(root, "Ahmed", "0322-1112222");
  root = insert(root, "Sara", "0333-9998888");

  cout << "\nPhone Directory (Sorted by Name):" << endl;
  inorder(root);

  return 0;
}

