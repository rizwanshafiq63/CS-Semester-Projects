#include <iostream>
#include <queue>
using namespace std;

struct node {
  int data;
  node *left;
  node *right;
  int ht;
};

// Height of the Tree
int height(node *T) {
  int lh, rh;
  if (T == NULL)
    return(0);
  if (T->left == NULL)
    lh = 0;
  else
    lh = 1 + T->left->ht;
  if (T->right == NULL)
    rh = 0;
  else
    rh = 1 + T->right->ht;
  return (lh > rh ? lh : rh);
}
// Method 02 -> Recursive
int Height(node *p) {
  int x, y;
  if (p == NULL) {
    return 0;
  }
  x = Height(p->left);
  y = Height(p->right);
  return x > y ? x + 1 : y + 1;
}

// ==============================================
// Lab Task 1: Complete All AVL Tree Rotations
// ==============================================

// Rotate Right
node *rotateright(node *x) {
  node *y = x->left;
  x->left = y->right;
  y->right = x;
  x->ht = height(x);
  y->ht = height(y);
  return y;
}

// Rotate Left
node *rotateleft(node *x) {
  node *y = x->right;
  x->right = y->left;
  y->left = x;
  x->ht = height(x);
  y->ht = height(y);
  return y;
}

// Apply the left right rotation
node *LR(node *T) {
  T->left = rotateleft(T->left);
  T = rotateright(T);
  return T;
}

// Apply the right left rotation
node *RL(node *T) {
  T->right = rotateright(T->right);
  T = rotateleft(T);
  return T;
}

// Apply the left left rotation
node *LL(node *T) {
  T = rotateright(T);
  return T;
}

// Apply the right right rotation
node *RR(node *T) {
  T = rotateleft(T);
  return T;
}

// ==============================================
// Lab Task 2: Level Order Traversal of AVL Tree
// ==============================================

void levelOrder(node* root) {
  if (root == NULL) return;

  queue<node*> q;
  q.push(root);

  while (!q.empty()) {
    node* current = q.front();
    q.pop();

    cout << current->data << " ";

    if (current->left != NULL)
      q.push(current->left);
    if (current->right != NULL)
      q.push(current->right);
  }
}
// ==============================================
// Insertion, Deletion, and Balance factor
// ==============================================

// Find the balance factor
int BF(node *T) {
  int lh, rh;
  if (T == NULL)
    return 0;
  if (T->left == NULL)
    lh = 0;
  else
    lh = 1 + T->left->ht;
  if (T->right == NULL)
    rh = 0;
  else
    rh = 1 + T->right->ht;
  return (lh - rh);
}

int balanceFactor(node* T) {
  int lh, rh;
  if (T == NULL)
    return 0;
  lh = Height(T->left);
  rh = Height(T->right);
  return (lh - rh);
}

// Insert the new node in AVL
node *insert(node *T, int x) {
  if (T == NULL) {
    T = new node;
    T->data = x;
    T->left = NULL;
    T->right = NULL;
    T->ht = 0;
  } else if (x > T->data) {
    T->right = insert(T->right, x);
    if (BF(T) == -2) {
      if (x > T->right->data) {
        T = RR(T);
      } else {
        T = RL(T);
      }
    }
  } else if (x < T->data) {
    T->left = insert(T->left, x);
    if (BF(T) == 2) {
      if (x < T->left->data) {
        T = LL(T);
      } else {
        T = LR(T);
      }
    }
  }
  T->ht = height(T);
  return T;
}

// Delete from AVL Tree
node *Delete(node *T, int x) {
  node *p;
  if (T == NULL) {
    return NULL;
  } else if (x > T->data) {
    T->right = Delete(T->right, x);
    if (BF(T) == 2) {
      if (BF(T->left) >= 0) {
        T = LL(T);
      } else {
        T = LR(T);
      }
    }
  } else if (x < T->data) {
    T->left = Delete(T->left, x);
    if (BF(T) == -2) {
      if (BF(T->right) <= 0) {
        T = RR(T);
      } else {
        T = RL(T);
      }
    }
  } else {
    if (T->right != NULL) {
      p = T->right;
      while (p->left != NULL) {
        p = p->left;
      }
      T->data = p->data;
      T->right = Delete(T->right, p->data);
      if (BF(T) == 2) {
        if (BF(T->left) >= 0) {
          T = LL(T);
        } else {
          T = LR(T);
        }
      }
    } else {
      return T->left;
    }
  }
  T->ht = height(T);
  return T;
}

// Inorder traversal 
void inorder(node *T) {
  if (T != NULL) {
    inorder(T->left);
    cout << T->data << " ";
    inorder(T->right);
  }
}

int main() {
  node *root = NULL;
  root = insert(root, 30);
  root = insert(root, 20);
  root = insert(root, 40);
  root = insert(root, 10);
  root = insert(root, 25);
  root = insert(root, 35);
  root = insert(root, 50);

  cout << "Inorder Traversal: ";
  inorder(root);
  cout << endl;

  root = Delete(root, 20);
  cout << "After deleting 20: ";
  inorder(root); 
  cout << endl;

  cout << "Level Order Traversal of AVL Tree: ";
  levelOrder(root);
  cout << endl;

  return 0;
}

