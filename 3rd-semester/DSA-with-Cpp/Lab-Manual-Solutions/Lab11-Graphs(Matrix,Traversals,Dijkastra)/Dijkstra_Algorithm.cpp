#include <iostream>
#include <climits>
using namespace std;

#define V 5  // Number of vertices

// Find the vertex with minimum distance value, from the set of vertices not yet processed
int minDistance(int dist[], bool visited[]) {
  int min = INT_MAX, min_index;

  for (int v = 0; v < V; v++) {
    if (!visited[v] && dist[v] <= min) {
      min = dist[v];
      min_index = v;
    }
  }
  return min_index;
}

// Print the constructed distance array
void printSolution(int dist[], int src) {
  cout << "Shortest distances from vertex " << src << ":\n";
  for (int i = 0; i < V; i++)
    cout << "To " << i << " => " << dist[i] << "\n";
}

// Dijkstra's algorithm for a graph represented using adjacency matrix
void dijkstra(int graph[V][V], int src) {
  int dist[V];        // Output array. dist[i] will hold the shortest distance from src to i
  bool visited[V];    // visited[i] will be true if vertex i is included in shortest path tree

  // Initialize all distances as infinite and visited[] as false
  for (int i = 0; i < V; i++) {
    dist[i] = INT_MAX;
    visited[i] = false;
  }

  dist[src] = 0;  // Distance of source vertex from itself is always 0

  // Find shortest path for all vertices
  for (int count = 0; count < V - 1; count++) {
    int u = minDistance(dist, visited); // Pick the minimum distance vertex not yet processed
    visited[u] = true;

    // Update dist[v] only if there's a shorter path through u
    for (int v = 0; v < V; v++) {
      if (!visited[v] && graph[u][v] && (dist[u] != INT_MAX) && (dist[u] + graph[u][v] < dist[v])) {
        dist[v] = dist[u] + graph[u][v];
      }
    }
  }

  printSolution(dist, src);
}

int main() {
  // Example graph represented as adjacency matrix
  int graph[V][V] = {
    {0, 4, 0, 0, 8},
    {4, 0, 8, 0, 0},
    {0, 8, 0, 7, 2},
    {0, 0, 7, 0, 6},
    {8, 0, 2, 6, 0}
  };

  int startVertex = 0;
  dijkstra(graph, startVertex);

  return 0;
}
//GRAPH_TAKEN:
//
//    [0]
// 4 __|__8
//  |    |
// [1]  [4]
//  |   /|
// 8| 2/ |6
//  | /  |
//  |/ 7 |
// [2]---[3]
//

