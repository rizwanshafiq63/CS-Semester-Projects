// Implement the Graph by Adjacency List.

#include<iostream>
using namespace std;

struct edge{
  int data;
  edge *next;
};

struct node{
  int data;
  edge *head;
  edge *tail;
  node *next;
}
*head=NULL, *tail=NULL;

void insert_vertex (int data) {
  node *temp = new node;
  temp->data = data;
  temp->head = NULL;
  temp->tail = NULL;
  if (head == NULL) {
    temp->next = NULL;
    head = tail = temp;
  } else{
    tail->next = temp;
    tail = temp;
    tail->next = NULL;
  }
}

bool check_uname (int data) {
  node *temp = head;
  while ((temp->data != data) && (temp != tail)) {
    temp = temp->next;
  }
  if (temp->data != data) {
    cout << "Second Vertix Not Found: " << data << endl;
    return false;
  }
  return true;
}

void add_edge (int vname, int uname) {
  // vname = Source Vertex, uname = Second Vertex
  node *temp = head;
  while ((temp->data != vname) && (temp != NULL)){
    temp = temp->next;
  }
  if (temp == NULL) {
    cout << "Source Vertix Not Found: " << vname << endl;
    return;
  }
  if ((temp != NULL) && check_uname(uname)) {
    edge *etemp = new edge;
    etemp->data = uname;
    if (temp->head == NULL) {
      etemp->next = NULL;
      temp->head = temp->tail = etemp;
    } else {
      temp->tail->next = etemp;
      temp->tail = etemp;
      etemp->next = NULL;
    }
  } else {
    cout << "Unable to insert Edge: " << vname << "-" << uname << endl;
  }
}

void display() {
  node *temp = head;
  edge *etem;
  while (temp != NULL) {
    etem = temp->head;
    cout << temp->data << " -> ";
    while (etem != NULL) {
      cout << etem->data << " ";
      etem = etem->next;
    }
    temp = temp->next;
    cout<<endl;
  }
}

void delete_edge (int vname, int uname) {
  node *temp = head;
  while (temp != NULL){
    if(temp->data == vname){
      break;
    }
    temp = temp->next;
  }
  if (temp == NULL) {
    cout << "Vertix Not Found" << endl;
    return;
  } else {
    edge *emp = temp->head;
    if(emp->data == uname){
      if(temp->head == temp->tail){
        temp->head = temp->tail = NULL;
        return;
      }
      temp->head = temp->head->next;
      return;
    }
    while (emp != NULL) {
      if (emp->next->data == uname) {
        emp->next = emp->next->next;
        return;
      }
      emp = emp->next;
    }
    if (emp == NULL) {
      cout << "Edge Not Found" << endl;
    }
  }
}

int main(){
  insert_vertex(1);
  insert_vertex(2);
  insert_vertex(3);
  insert_vertex(4);
  insert_vertex(5);

  add_edge(1,2);
  add_edge(2,15);//exception handled if node if not found
  add_edge(1,4);
  add_edge(4,1);
  cout << "\nDisplay of Edges: " << endl;
  display();

  cout << "\nAfter Deleting (1,2) edge: " << endl;
  delete_edge(1,2);
  display();
}


