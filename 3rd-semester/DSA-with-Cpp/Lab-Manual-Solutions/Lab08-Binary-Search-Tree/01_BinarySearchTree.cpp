#include <iostream>
using namespace std;

struct BST{
  int data;
  BST *left=NULL;
  BST *right=NULL;
  BST(int d) {
    data = d; 
  }
};

class BinarySearchTree{
private:
  BST *root;
  int add=0;
  int count=0;
  int leafCount=0;
public:
  BinarySearchTree() {
    root = NULL;
  }

  void insertItrative(int a){
    BST *curr=new BST(a);
    if (root==NULL){
      root=curr;
    } else {
      BST *p=root, *q;
      while(p!=NULL){
        q=p;
        if(curr->data > p->data) {
          p = p->right;
        } else {
          p = p->left;
        }
      }
      if(curr->data > q->data) {
        q->right = curr;
      } else {
        q->left = curr;
      }
    }
    //return p; // If you were to return the pointer to the newly inserted node
  }

  BST* Search(int key) {
    if (root==NULL) {
      cout << "Tree is empty" << endl;
      return NULL;
    }
    BST *p=root;
    while(p!=NULL && p->data!=key) {
      if(key > p->data)
        p = p->right;
      else
        p = p->left;
    }
    if(p==NULL) {
      cout << "Key not found" << endl;
      return NULL;
    }
    return p;
  }

  BST* Min() {
    BST *p = root;
    while(p->left != NULL) {
      p = p->left;
    }
    return p; // Most left node
  }

  BST* Max() {
    BST *p = root;
    while(p->right != NULL) {
      p = p->right;
    }
    return p; // Most right node
  }

  void insertRecursive(int val) {
    insertRecursive(root, val);
  }
  BST* SearchRec(int key) {
    if (root==NULL) {
      cout << "Tree is empty" << endl;
      return NULL;
    }
    BST *p=root;
    return SearchRec(p, key);
  }
  void Sum() {
    cout << "Sum of all nodes: ";
    sum(root);
    cout << add << endl;
    cout << "Count of all nodes: ";
    cout << count << endl;
  }
  int Height() {
    return Height(root);
  }
  // Lab Task 1: Implement the methods for Tree Traversal with Right Branch Priority i.e. Pre Order (NRL), Post Order (RLN) and In Order (RNL).
  void Inorder() {
    cout << "Inorder Traversal (RNL): ";
    Inorder(root);
    cout << endl;
  }
  void Preorder() {
    cout << "Preorder Traversal (NRL): ";
    Preorder(root);
    cout << endl;
  }
  void Postorder() {
    cout << "Postorder Traversal (RLN): ";
    Postorder(root);
    cout << endl;
  }
  // Lab Task 2: Write down code to print and count Leaf nodes of a BST.
  void printLeafNodes() {
    cout << "Leaf Nodes: ";
    printLeafNodes(root);
    cout << endl;
  }
  void countLeafNodes() {
    leafCount = countLeafNodes(root);
    cout << "Total Leaf Nodes: " << leafCount << endl;
  }
  // Lab Task 3: Introduce method to delete a Node from BST, keep in mind that there are 3 possiblities for deletion, Node without any child, Node with One child and Node with both the children.
  void deleteNode(int key) {
    if (root == NULL) {
      cout << "Tree is empty" << endl;
      return;
    }

    // Search for the node to be deleted
    BST* p = root, *parent = NULL;
    while (p != NULL && p->data != key) {
      parent = p;
      if (key < p->data) {
        p = p->left;
      } else {
        p = p->right;
      }
    }
    if (p == NULL) {
      cout << "Key not found" << endl;
      return;
    }

    // Node found, now delete it 
    // Case 1: No child
    if (p->left == NULL && p->right == NULL) {
      if (parent == NULL) {
        root = NULL; // Deleting root node
      } else if (parent->left == p) {
        parent->left = NULL;
      } else {
        parent->right = NULL;
      }
      delete p;
    }
    // Case 2: One child
    else if (p->left == NULL || p->right == NULL) {
      BST* child = (p->left != NULL) ? p->left : p->right;
      if (parent == NULL) {
        root = child; // Deleting root node
      } else if (parent->left == p) {
        parent->left = child;
      } else {
        parent->right = child;
      }
      delete p;
    }
    // Case 3: Two children
    else {
      BST* successor = p->right;
      BST* successorParent = p;
      while (successor->left != NULL) {
        successorParent = successor;
        successor = successor->left;
      }
      p->data = successor->data; // Copy the data from the successor
      if (successorParent->left == successor) {
        successorParent->left = successor->right; // Bypass the successor
      } else if (successorParent->right == successor) { // if successor is right child to successorParent
        successorParent->right = successor->right; // Bypass the successor
      }
      delete successor;
    }
  }

private:
  int Height(BST *p) {
    int x, y;
    if (p == NULL) {
      return 0;
    }
    x = Height(p->left);
    y = Height(p->right);
    return x > y ? x + 1 : y + 1;
  }
  void insertRecursive(BST *node, int val) {
    if (node == NULL) {
      node = new BST(val);
      return;
    }
    if (val < node->data) {
      insertRecursive(node->left, val);
    } else if (val > node->data) {
      insertRecursive(node->right, val);
    } else {
      cout << "Duplicate value not allowed" << endl;
    }
  }

  BST* SearchRec(BST *node, int key) {
    if (node == NULL) {
      cout << "Key not found" << endl;
      return NULL;
    }
    if (node->data == key) {
      cout << "Key found" << endl;
      return node;
    }
    if (key > node->data) {
      return SearchRec(node->right, key);
    } else {
      return SearchRec(node->left, key);
    }
  }

  void Inorder(BST *node) {
    // Left, Root, Right
    if (node == NULL) {
      return;
    }
    Inorder(node->left);
    cout << node->data << " > ";
    Inorder(node->right);
  }

  void Preorder(BST *node) {
    // Root, Left, Right
    if (node == NULL) {
      return;
    }
    cout << node->data << " > ";
    Preorder(node->left);
    Preorder(node->right);
  }

  void Postorder(BST *node) {
    // Left, Right, Root
    if (node == NULL) {
      return;
    }
    Postorder(node->left);
    Postorder(node->right);
    cout << node->data << " > ";
  }

  void printLeafNodes(BST* node) {
    if (node == NULL) return;
    if (node->left == NULL && node->right == NULL) {
      cout << node->data << " ";
    }
    printLeafNodes(node->left);
    printLeafNodes(node->right);
  }

  int countLeafNodes(BST* node) {
    if (node == NULL) return 0;
    if (node->left == NULL && node->right == NULL) return 1;
    return countLeafNodes(node->left) + countLeafNodes(node->right);
  }

  void sum(BST *s) {
    if(s!=NULL) {
      count += 1;
      add += s->data;
      sum(s->left);
      sum(s->right);
    }
  }
};

int main() {
  BinarySearchTree bst;
  int choice, val;

  do {
    cout << "\n--- Binary Search Tree Menu ---\n";
    cout << "1. Insert Iteratively\n";
    cout << "2. Insert Recursively\n";
    cout << "3. Search (Iterative)\n";
    cout << "4. Search (Recursive)\n";
    cout << "5. Find Min\n";
    cout << "6. Find Max\n";
    cout << "7. Delete Node\n";
    cout << "8. Inorder Traversal (RNL)\n";
    cout << "9. Preorder Traversal (NRL)\n";
    cout << "10. Postorder Traversal (RLN)\n";
    cout << "11. Print Leaf Nodes\n";
    cout << "12. Count Leaf Nodes\n";
    cout << "13. Sum and Count of all Nodes\n";
    cout << "0. Exit\n";
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        cout << "Enter value to insert iteratively: ";
        cin >> val;
        bst.insertItrative(val);
        break;
      case 2:
        cout << "Enter value to insert recursively: ";
        cin >> val;
        bst.insertRecursive(val);
        break;
      case 3:
        cout << "Enter value to search: ";
        cin >> val;
        bst.Search(val);
        break;
      case 4:
        cout << "Enter value to search (recursive): ";
        cin >> val;
        bst.SearchRec(val);
        break;
      case 5: {
        BST* min = bst.Min();
        if (min != NULL) cout << "Minimum value: " << min->data << endl;
        break;
      }
      case 6: {
        BST* max = bst.Max();
        if (max != NULL) cout << "Maximum value: " << max->data << endl;
        break;
      }
      case 7:
        cout << "Enter value to delete: ";
        cin >> val;
        bst.deleteNode(val);
        break;
      case 8:
        bst.Inorder();
        break;
      case 9:
        bst.Preorder();
        break;
      case 10:
        bst.Postorder();
        break;
      case 11:
        bst.printLeafNodes();
        break;
      case 12:
        bst.countLeafNodes();
        break;
      case 13:
        bst.Sum();
        break;
      case 0:
        cout << "Exiting program..." << endl;
        break;
      default:
        cout << "Invalid choice. Try again." << endl;
    }
  } while (choice != 0);

  return 0;
}

