// Implement the BFS.

#include <iostream>
#include <queue> // for BFS queue
#include <stdlib.h>
using namespace std;

#define MAX 5

// Vertex structure
struct Vertex {
  char label;
  bool visited;
};

// Graph variables
Vertex* lstVertices[MAX];
int adjMatrix[MAX][MAX];
int vertexCount = 0;

// Graph Functions
void addVertex(char label) {
  Vertex* vertex = new Vertex;
  vertex->label = label;
  vertex->visited = false;
  lstVertices[vertexCount++] = vertex;
}
void addEdge(int start, int end) { // undirected
  adjMatrix[start][end] = 1;
  adjMatrix[end][start] = 1;
}
void displayVertex(int vertexIndex) {
  cout << lstVertices[vertexIndex]->label << " ";
}
int getAdjUnvisitedVertex(int vertexIndex) {
  for (int i = 0; i < vertexCount; i++) {
    if (adjMatrix[vertexIndex][i] == 1 && !lstVertices[i]->visited) {
      return i;
    }
  }
  return -1;
}

//  Breadth-First Search
void breadthFirstSearch() {
  queue<int> q;

  // Start from vertex 0
  lstVertices[0]->visited = true;
  displayVertex(0);
  q.push(0);

  while (!q.empty()) {
    int currentVertex = q.front();
    q.pop();

    int unvisitedVertex;
    while ((unvisitedVertex = getAdjUnvisitedVertex(currentVertex)) != -1) {
      lstVertices[unvisitedVertex]->visited = true;
      displayVertex(unvisitedVertex);
      q.push(unvisitedVertex);
    }
  }

  // Reset visited flags
  for (int i = 0; i < vertexCount; i++) {
    lstVertices[i]->visited = false;
  }
}

int main() {
  // Initialize adjacency matrix to 0
  for (int i = 0; i < MAX; i++) {
    for (int j = 0; j < MAX; j++) {
      adjMatrix[i][j] = 0;
    }
  }

  // Add vertices
  addVertex('S'); // 0
  addVertex('A'); // 1
  addVertex('B'); // 2
  addVertex('C'); // 3
  addVertex('D'); // 4

  // Add edges
  addEdge(0, 1); // S-A
  addEdge(0, 2); // S-B
  addEdge(0, 3); // S-C
  addEdge(1, 4); // A-D
  addEdge(2, 4); // B-D
  addEdge(3, 4); // C-D

  cout << "\nBreadth-First Search (BFS): ";
  breadthFirstSearch();

  return 0;
}

