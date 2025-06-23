// Lab Task 1: Write the deletion method for chaining.

#include<stdio.h>
#include<stdlib.h>
#include<iostream>
using namespace std;

#define size 7

struct node {
  int data;
  struct node *next;
};

struct node *chain[size];

void init() {
  int i;
  for(i = 0; i < size; i++)
    chain[i] = NULL;
}

void deleteValue(int value) {
  int key = value % size;
  struct node *temp = chain[key];
  struct node *prev = NULL;

  while(temp != NULL) {
    if(temp->data == value) {
      if(prev == NULL) {
        // Deleting the head node
        chain[key] = temp->next;
      } else {
        // Deleting a middle or last node
        prev->next = temp->next;
      }
      delete temp;
      cout << "Value " << value << " deleted from chain[" << key << "]\n";
      return;
    }
    prev = temp;
    temp = temp->next;
  }

  cout << "Value " << value << " not found in chain[" << key << "]\n";
}

void insert(int value) {
  //create a new node with value
  node *newNode = new node;
  newNode->data = value;
  newNode->next = NULL;
  //calculate hash key
  int key = value % size;
  //check if chain[key] is empty
  if(chain[key] == NULL) {
    chain[key] = newNode; //collision
  } else {
    //add the node at the end of chain[key].
    struct node *temp = chain[key];
    while(temp->next) {
      temp = temp->next;
    }
    temp->next = newNode;
  }
}

void print() {
  int i;
  for(i = 0; i < size; i++) {
    struct node *temp = chain[i];
    cout<<"chain["<<i<<"]-->";
    if (temp == NULL) {
      cout<<" NULL\n";
    } else {
      while(temp) {
        cout<<" "<<temp->data;
        temp = temp->next;
      }
      cout<<endl;
    }
  }
}

int main() {
  init();

  insert(7);
  insert(0);
  insert(3);
  insert(10);
  insert(4);
  insert(5);

  cout << "Before deletion:\n";
  print();

  deleteValue(10);
  deleteValue(7);
  deleteValue(99); // not in hash table

  cout << "\nAfter deletion:\n";
  print();

  return 0;
}


