/* Activity: Implements the KRUSKAL'S algorithm to construct the MST.
INTRODUCTION: Kruskal's algorithm is a greedy algorithm that finds a minimum spanning tree
for a connected weighted graph. It adds the lowest weight edge that doesn't form a cycle.
Steps:
1. Sort all the edges in increasing order of weight.
2. Pick smallest edge. If it doesn't form a cycle, add it to the MST.
3. Repeat until MST has (V - 1) edges.
*/

#include <iostream>
using namespace std;

#define V 5     // Number of vertices
#define E 7     // Number of edges

// Structure to store edge
struct Edge {
  int src, dest, weight;
};

// Structure for union-find
struct Subset {
  int parent;
  int rank;
};

// Find set of a node (with path compression)
int find(Subset subsets[], int i) {
  if (subsets[i].parent != i)
    subsets[i].parent = find(subsets, subsets[i].parent);
  return subsets[i].parent;
}

// Union of two sets (by rank)
void Union(Subset subsets[], int x, int y) {
  int xroot = find(subsets, x);
  int yroot = find(subsets, y);

  if (subsets[xroot].rank < subsets[yroot].rank)
    subsets[xroot].parent = yroot;
  else if (subsets[xroot].rank > subsets[yroot].rank)
    subsets[yroot].parent = xroot;
  else {
    subsets[yroot].parent = xroot;
    subsets[xroot].rank++;
  }
}

// Function to sort edges by weight (Bubble Sort)
void sortEdges(Edge edges[]) {
  for(int i = 0; i < E - 1; i++) {
    for(int j = i + 1; j < E - 1; j++) {
      if (edges[i].weight > edges[j].weight) {
        // Swap the edges
        Edge temp = edges[i];
        edges[i] = edges[j];
        edges[j] = temp;
      }
    }
  }
}

// Kruskal’s MST algorithm
void kruskalMST(Edge edges[]) {
  Edge result[V];  // To store MST result
  Subset subsets[V];

  // Initialize subsets
  for (int v = 0; v < V; v++) {
    subsets[v].parent = v;
    subsets[v].rank = 0;
  }

  // Step 1: Sort all edges by weight
  sortEdges(edges);

  int e = 0; // Index for result[]
  int i = 0; // Index for edges[]

  // Step 2: Pick edges one by one
  while (e < V - 1 && i < E) { // V = no of vertices(5), E = no of Edges(7)
    Edge next = edges[i++];

    int x = find(subsets, next.src);
    int y = find(subsets, next.dest);

    // If no cycle, add to result
    if (x != y) {
      result[e++] = next;
      Union(subsets, x, y);
    }
  }

  // Print MST	1
  cout << "\n Edge \t| Weight \n\t| " << endl;
  for (int i = 0; i < e; i++)
    cout << result[i].src << " -> " << result[i].dest << "  | " << result[i].weight << endl;
}

// Driver function
int main() {
  // Define the edges of the graph
  Edge edges[E] = {
    {0, 1, 2}, {0, 3, 6}, {1, 2, 3}, {1, 3, 8},
    {1, 4, 5}, {2, 4, 7}, {3, 4, 9}
  };

  kruskalMST(edges);

  return 0;
}

//GRAPH_TAKEN:
//         2
//   [0]--------[1]---|
//     |       / |    |
//     |      /  |3   |
//    6|   8 /   |    |
//     |    /    |    |
//     |   /     |    |
//     |  /      |    |
//    [3]       [2]   |5 
//     |         |    |
//     |         |7   |
//    9|         |    |
//     |         |    |
//     |--------[4]---|
//


