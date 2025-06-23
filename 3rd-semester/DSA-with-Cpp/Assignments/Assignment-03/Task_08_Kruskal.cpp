// Task-8:Kruskal’s Algorithm 
// Real-World Scenario: Connecting school buildings with minimum cost paths

#include <iostream>
using namespace std;

#define MAX 5
#define INF 9999

// Structure for edge
struct Edge {
  int u, v, weight;
};

// Function to sort edges by weight (selection sort)
void sortEdges(Edge edges[], int edgeCount) {
  for (int i = 0; i < edgeCount - 1; i++) {
    for (int j = i + 1; j < edgeCount; j++) {
      if (edges[j].weight < edges[i].weight) {
        Edge temp = edges[i];
        edges[i] = edges[j];
        edges[j] = temp;
      }
    }
  }
}

// Find parent for union-find
int findParent(int parent[], int i) {
  while (parent[i] != i)
    i = parent[i];
  return i;
}

// Kruskal’s Algorithm
void kruskal(Edge edges[], int edgeCount) {
  int parent[MAX];
  for (int i = 0; i < MAX; i++)
    parent[i] = i;

  cout << "Minimum Paths to Connect School Buildings:\n";
  int totalCost = 0;

  for (int i = 0; i < edgeCount; i++) {
    int u = edges[i].u;
    int v = edges[i].v;
    int w = edges[i].weight;

    int parentU = findParent(parent, u);
    int parentV = findParent(parent, v);

    if (parentU != parentV) {
      cout << "Connect building " << u << " to building " << v << " with cost " << w << endl;
      totalCost += w;
      parent[parentU] = parentV; // union
    }
  }

  cout << "Total Minimum Cost: " << totalCost << endl;
}

int main() {
  // Sample graph (5 buildings, 7 possible paths)
  Edge edges[] = {
    {0, 1, 10},
    {0, 2, 6},
    {0, 3, 5},
    {1, 3, 15},
    {2, 3, 4},
    {1, 4, 9},
    {3, 4, 7}
  };
  int edgeCount = sizeof(edges) / sizeof(edges[0]);

  // Sort edges and apply Kruskal
  sortEdges(edges, edgeCount);
  kruskal(edges, edgeCount);

  return 0;
}

