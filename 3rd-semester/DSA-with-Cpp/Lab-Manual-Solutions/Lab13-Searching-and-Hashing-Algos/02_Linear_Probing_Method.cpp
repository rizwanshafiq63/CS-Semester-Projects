// Linear Probing Method
// Output: The method will insert, display and search the value from Hash Table.

#include <stdio.h>
#include<stdlib.h>
#include<iostream>
using namespace std;

#define TABLE_SIZE 10
int h[TABLE_SIZE] = {NULL};

void insert() {
  int key, index, i, hkey;
  cout<<"\nEnter a value to insert into hash table: ";
  cin>>key;
  hkey = key % TABLE_SIZE;
  for(i = 0; i < TABLE_SIZE; i++) {
    index = (hkey + i) % TABLE_SIZE;
    if (h[index] == NULL) {
      h[index] = key;
      break;
    }
  }
  if(i == TABLE_SIZE)
    cout<<"\nElement cannot be inserted...!\n";
}

void search() {
  int key, index, i, hkey;
  cout<<"\nEnter search element: ";
  cin>>key;
  hkey=key%TABLE_SIZE;
  for(i = 0; i < TABLE_SIZE; i++) {
    index = (hkey + i) % TABLE_SIZE;
    if(h[index] == key) {
      cout<<"Value is found at index"<<index;
      break;
    }
  }
  if(i == TABLE_SIZE)
    cout<<"\nValue is not found...!\n";
}

void display() {
  int i;
  cout<<"\nElements in the hash table are: \n";
  for (i = 0; i < TABLE_SIZE; i++)
    cout<<"\n At index "<<i<<" \t value = "<<h[i];
}

int main() {
  int opt,i;
  while(1) {
    cout<<"\n Press 1. Insert\t 2. Display \t3. Search \t4.Exit \n";
    cin>>opt;
    switch(opt) {
      case 1:
        insert();
        break;
      case 2:
        display();
        break;
      case 3:
        search();
        break;
      case 4:
        exit(0);
    }
  }
}


