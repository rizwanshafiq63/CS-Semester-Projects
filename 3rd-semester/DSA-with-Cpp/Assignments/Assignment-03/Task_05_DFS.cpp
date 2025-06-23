#include <stdlib.h>
#include <iostream>
using namespace std;

#define MAX 5

struct Vertex {
  char label;
  bool visited;
};

// Stack variables
int stk[MAX];
int top = -1;

// Stack functions
void push(int item) {
  stk[++top] = item;
}
int pop() {
  return stk[top--];
}
int peek() {
  return stk[top];
}
bool isStackEmpty() {
  return top == -1;
}

// Graph variables
struct Vertex* lstVertices[MAX];
int adjMatrix[MAX][MAX];
int vertexCount = 0;

// Graph functions
void addVertex(char label) {
  struct Vertex* vertex = (struct Vertex*) malloc(sizeof(struct Vertex));
  vertex->label = label;
  vertex->visited = false;
  lstVertices[vertexCount++] = vertex;
}
void addEdge(int start, int end) {
  adjMatrix[start][end] = 1;
  adjMatrix[end][start] = 1;
}
void displayVertex(int vertexIndex) {
  cout << lstVertices[vertexIndex]->label;
}
int getAdjUnvisitedVertex(int vertexIndex) {
  for (int i = 0; i < vertexCount; i++) {
    if (adjMatrix[vertexIndex][i] == 1 && lstVertices[i]->visited == false) {
      return i;
    }
  }
  return -1;
}

// Depth First Search
void depthFirstSearch() {
  lstVertices[0]->visited = true;
  displayVertex(0);
  push(0);
  while (!isStackEmpty()) {
    int unvisitedVertex = getAdjUnvisitedVertex(peek());
    if (unvisitedVertex == -1) {
      pop();
    } else {
      lstVertices[unvisitedVertex]->visited = true;
      displayVertex(unvisitedVertex);
      push(unvisitedVertex);
    }
  }
  for (int i = 0; i < vertexCount; i++) {
    lstVertices[i]->visited = false;
  }
}

int main() {
  // Initialize adjacency matrix to zero
  for (int i = 0; i < MAX; i++) {
    for (int j = 0; j < MAX; j++) {
      adjMatrix[i][j] = 0;
    }
  }

  addVertex('S'); // 0
  addVertex('A'); // 1
  addVertex('B'); // 2
  addVertex('C'); // 3
  addVertex('D'); // 4

  addEdge(0, 1); // S - A
  addEdge(0, 2); // S - B
  addEdge(0, 3); // S - C
  addEdge(1, 4); // A - D
  addEdge(2, 4); // B - D
  addEdge(3, 4); // C - D

  cout << "Depth First Search of Social Media Connections: ";
  depthFirstSearch();

  return 0;
}