#include <stdlib.h>
#include <iostream>
using namespace std;

#define MAX 5

struct Vertex {
  char label;
  bool visited;
};

//stack variables
int stack[MAX];
int top = -1;

//stack functions
void push(int item) {
  stack[++top] = item;
}
int pop() {
  return stack[top--];
}
int peek() {
  return stack[top];
}
bool isStackEmpty() {
  return top == -1;
}

//graph variables
struct Vertex* lstVertices[MAX]; //array of vertices
int adjMatrix[MAX][MAX]; //adjacency matrix
int vertexCount = 0; //vertex count

//graph functions
void addVertex(char label) { //add vertex to the vertex list
  struct Vertex* vertex = (struct Vertex*) malloc(sizeof(struct Vertex));
  vertex->label = label;
  vertex->visited = false;
  lstVertices[vertexCount++] = vertex;
}
void addEdge(int start,int end) { //add edge to edge array
  adjMatrix[start][end] = 1;
  adjMatrix[end][start] = 1;
}
void displayVertex(int vertexIndex) { //display the vertex
  cout<<lstVertices[vertexIndex]->label;
}
int getAdjUnvisitedVertex(int vertexIndex) { //get the adjacent unvisited vertex
  int i;
  for(i = 0; i < vertexCount; i++) {
    if(adjMatrix[vertexIndex][i] == 1 && lstVertices[i]->visited == false) {
      return i;
    }
  }
  return -1;
}

// DEPTH FIRST SEARCH
void depthFirstSearch() {
  int i;
  //mark first node as visited
  lstVertices[0]->visited = true;
  //display the vertex
  displayVertex(0);
  //push vertex index in stack
  push(0);
  while(!isStackEmpty()) {
    //get the unvisited vertex of vertex which is at top of the stack
    int unvisitedVertex = getAdjUnvisitedVertex(peek());
    //no adjacent vertex found
    if(unvisitedVertex == -1) {
      pop();
    } else {
      lstVertices[unvisitedVertex]->visited = true;
      displayVertex(unvisitedVertex);
      push(unvisitedVertex);
    }
  }
  //stack is empty, search is complete, reset the visited flag
  for(i = 0;i < vertexCount;i++) {
    lstVertices[i]->visited = false;
  }
}

int main() {
  // Initializing the matrix to zero
  int i, j;
  for(i = 0; i < MAX; i++) { // set adjacency
    for(j = 0; j < MAX; j++) // matrix to 0
      adjMatrix[i][j] = 0;
  }

  addVertex('S');// 0
  addVertex('A');// 1
  addVertex('B');// 2
  addVertex('C');// 3
  addVertex('D');// 4

  addEdge(0, 1);// S - A
  addEdge(0, 2);// S - B
  addEdge(0, 3);// S - C
  addEdge(1, 4);// A - D
  addEdge(2, 4);// B - D
  addEdge(3, 4);// C - D

  cout<<"\n Depth First Search: ";
  depthFirstSearch();

  return 0;
}


