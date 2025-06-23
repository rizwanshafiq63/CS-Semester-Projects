#include <iostream>
#include <queue>
#include <unordered_set>
using namespace std;

#define MAX 5

struct Vertex {
  char label;
  bool visited;
};

Vertex* lstVertices[MAX];
int adjMatrix[MAX][MAX];
int vertexCount = 0;

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

void suggestFriendsBFS(int startVertex) {
  queue<int> q;
  vector<bool> visited(vertexCount, false);
  unordered_set<int> directFriends;
  unordered_set<int> suggestions;
  int level = 0;
  int nodesInCurrentLevel = 1;
  int nodesInNextLevel = 0;

  visited[startVertex] = true;
  q.push(startVertex);

  while (!q.empty() && level < 2) {
    int currentVertex = q.front();
    q.pop();
    nodesInCurrentLevel--;

    int unvisitedVertex;
    while ((unvisitedVertex = getAdjUnvisitedVertex(currentVertex)) != -1) {
      lstVertices[unvisitedVertex]->visited = true;
      q.push(unvisitedVertex);
      nodesInNextLevel++;
      if (level == 0) {
        directFriends.insert(unvisitedVertex);
      } else if (level == 1 && unvisitedVertex != startVertex && directFriends.find(unvisitedVertex) == directFriends.end()) {
        suggestions.insert(unvisitedVertex);
      }
    }

    if (nodesInCurrentLevel == 0) {
      level++;
      nodesInCurrentLevel = nodesInNextLevel;
      nodesInNextLevel = 0;
    }
  }

  cout << "Friend suggestions for user " << lstVertices[startVertex]->label << ": ";
  if (suggestions.empty()) {
    cout << "No suggestions found." << endl;
  } else {
    for (int s : suggestions) {
      displayVertex(s);
    }
    cout << endl;
  }

  for (int i = 0; i < vertexCount; i++) {
    lstVertices[i]->visited = false;
  }
}

int main() {
  for (int i = 0; i < MAX; i++) {
    for (int j = 0; j < MAX; j++) {
      adjMatrix[i][j] = 0;
    }
  }

  addVertex('A'); // 0
  addVertex('B'); // 1
  addVertex('C'); // 2
  addVertex('D'); // 3
  addVertex('E'); // 4

  addEdge(0, 1); // A-B
  addEdge(0, 2); // A-C
  addEdge(1, 3); // B-D
  addEdge(1, 4); // B-E

  cout << "BFS Friend Suggestions for user A: ";
  suggestFriendsBFS(0);

  return 0;
}