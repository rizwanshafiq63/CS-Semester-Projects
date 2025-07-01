// Insertion by chaining method.

#include<stdio.h>
#include<stdlib.h>
#include<iostream>
using namespace std;

#define size 7

struct node {
  int data;
  node *next;
};

node *chain[size];

void init() {
  for (int i = 0; i < size; i++)
    chain[i] = NULL;
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
    node *temp = chain[key];
    while(temp->next) {
      temp = temp->next;
    }
    temp->next = newNode;
  }
}

void print() {
  for (int i = 0; i < size; i++) {
    node *temp = chain[i];
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
  //init array of list to NULL
  init();

  insert(7);
  insert(0);
  insert(3);
  insert(10);
  insert(4);
  insert(5);

  print();

  return 0;
}


