// Implement the recursive method of DFS.

#include <iostream>
#include <stdlib.h>
using namespace std;

#define MAX 5

struct Vertex {
  char label;
  bool visited;
};

// Graph variables
struct Vertex* lstVertices[MAX];
int adjMatrix[MAX][MAX];
int vertexCount = 0;

// Graph Methods
void addVertex(char label) {
  Vertex* vertex = new Vertex;
  vertex->label = label;
  vertex->visited = false;
  lstVertices[vertexCount++] = vertex;
}
void addEdge(int start, int end) {
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

// Recursive DFS function
void recursiveDFS(int vertexIndex) {
  lstVertices[vertexIndex]->visited = true;
  displayVertex(vertexIndex);

  int adjVertex;
  while ((adjVertex = getAdjUnvisitedVertex(vertexIndex)) != -1) {
    recursiveDFS(adjVertex);
  }
}

// Reset visited flags
void resetVisited() {
  for (int i = 0; i < vertexCount; i++) {
    lstVertices[i]->visited = false;
  }
}

int main() {
  // Initialize matrix
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
  addEdge(0, 1);
  addEdge(0, 2);
  addEdge(0, 3);
  addEdge(1, 4);
  addEdge(2, 4);
  addEdge(3, 4);

  cout << "\nRecursive DFS Traversal: ";
  recursiveDFS(0); // Start DFS from vertex 0 ('S')

  resetVisited(); // Optional: Reset if you plan to reuse

  return 0;
}

