// Task-6: Dijkstra's Algorithm
// Real-World Scenario: GPS Navigation System — Finding the shortest path from one location to another on a map.

#include <iostream>
#include <climits>
using namespace std;

#define V 5  // Number of vertices (locations)

// Find vertex with minimum distance not yet processed
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

// Print shortest distances from source to all vertices
void printSolution(int dist[], int src) {
  cout << "Shortest distances from location " << src << ":\n";
  for (int i = 0; i < V; i++)
    cout << "To " << i << " => " << dist[i] << "\n";
}

// Dijkstra's algorithm to find shortest path from src
void dijkstra(int graph[V][V], int src) {
  int dist[V];        // shortest distances
  bool visited[V];    // processed vertices

  for (int i = 0; i < V; i++) {
    dist[i] = INT_MAX;
    visited[i] = false;
  }

  dist[src] = 0;  // distance to source itself

  for (int count = 0; count < V - 1; count++) {
    int u = minDistance(dist, visited);
    visited[u] = true;

    for (int v = 0; v < V; v++) {
      if (!visited[v] && graph[u][v] && dist[u] != INT_MAX &&
        dist[u] + graph[u][v] < dist[v]) {
        dist[v] = dist[u] + graph[u][v];
      }
    }
  }

  printSolution(dist, src);
}

int main() {
  // Example map graph: adjacency matrix with distances
  int graph[V][V] = {
    {0, 10, 0, 0, 5},
    {0, 0, 1, 0, 2},
    {0, 0, 0, 4, 0},
    {7, 0, 6, 0, 0},
    {0, 3, 9, 2, 0}
  };

  int startLocation = 0; // GPS start point
  dijkstra(graph, startLocation);

  return 0;
}

