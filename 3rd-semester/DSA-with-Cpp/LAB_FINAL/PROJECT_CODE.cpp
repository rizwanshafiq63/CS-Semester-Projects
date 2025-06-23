#include <algorithm>
#include <climits>
#include <functional>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <map>
#include <numeric>
#include <queue>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

// ===========================
//     STRUCT FOR DATASET
// ===========================
struct Route {
  int routeID;
  string train_name;
  string operators;
  float average_rating;
  string train_code;
  string route_code;
  string language_code;
  int num_stations;
  int passenger_count;
  int reviews_count;
  string start_date;
  string company;
  string fromLocation;
  string toLocation;

  Route* next;
  Route* prev;

  Route() : next(nullptr), prev(nullptr) {}
};
Route* head = nullptr;
Route* tail = nullptr;

// ====================================
//     STACK & QUEUE IMPLEMENTATION
// ====================================
template<typename T>
struct Node {
  T data;
  Node* next;
  Node(T val) : data(val), next(nullptr) {}
};

template<typename T>
class Stack {
private:
  Node<T>* top;

public:
  Stack() : top(nullptr) {}

  bool isEmpty() {
    return top == nullptr;
  }

  void push(T val) {
    Node<T>* newNode = new Node<T>(val);
    newNode->next = top;
    top = newNode;
  }

  T pop() {
    if (isEmpty()) throw runtime_error("Stack Underflow");
    T val = top->data;
    Node<T>* temp = top;
    top = top->next;
    delete temp;
    return val;
  }

  T peek() {
    if (isEmpty()) throw runtime_error("Stack is empty");
    return top->data;
  }

  ~Stack() {
    while (!isEmpty()) pop();
  }
};

template<typename T>
class Queue {
private:
  Node<T>* front;
  Node<T>* rear;

public:
  Queue() : front(nullptr), rear(nullptr) {}

  bool isEmpty() {
    return front == nullptr;
  }

  void enqueue(T val) {
    Node<T>* newNode = new Node<T>(val);
    if (rear) {
      rear->next = newNode;
      rear = newNode;
    } else {
      front = rear = newNode;
    }
  }

  T dequeue() {
    if (isEmpty()) throw runtime_error("Queue Underflow");
    T val = front->data;
    Node<T>* temp = front;
    front = front->next;
    if (!front) rear = nullptr;
    delete temp;
    return val;
  }

  T peek() {
    if (isEmpty()) throw runtime_error("Queue is empty");
    return front->data;
  }

  ~Queue() {
    while (!isEmpty()) dequeue();
  }
};

// ====================================
//     GENERAL & HELPING METHODS
// ====================================
void addRoute(int routeID, string train_name, string operators, float avg_rating,
              string train_code, string route_code, string lang_code,
              int num_stations, int passenger_count, int reviews_count,
              string start_date, string company, string fromLocation, string toLocation) {

  Route* newNode = new Route;
  newNode->routeID = routeID;
  newNode->train_name = train_name;
  newNode->operators = operators;
  newNode->average_rating = avg_rating;
  newNode->train_code = train_code;
  newNode->route_code = route_code;
  newNode->language_code = lang_code;
  newNode->num_stations = num_stations;
  newNode->passenger_count = passenger_count;
  newNode->reviews_count = reviews_count;
  newNode->start_date = start_date;
  newNode->company = company;
  newNode->fromLocation = fromLocation;
  newNode->toLocation = toLocation;


  if (!head) {
    head = tail = newNode;
  } else {
    tail->next = newNode;
    newNode->prev = tail;
    tail = newNode;
  }
}

void printAllRoutes() {
  Route* temp = head;
  cout << "Train Name | Operator | Rating | Passengers | Stations | Company | From_Loc | To_Loc \n";
  while (temp) {
    cout << temp->train_name << " | " << temp->operators << " | " << temp->average_rating
      << " | " << temp->passenger_count << " | " << temp->num_stations
      << " | " << temp->company << " | " << temp->fromLocation << " | " << temp->toLocation << "\n";
    temp = temp->next;
  }
}

// ====================================
//  METHODS USING THE DATA STRUCTURES
// ====================================

// ====================================
//         BINARY SEARCH TREE
// ====================================
class BST {
private:
  struct BSTNode {
    Route* data;
    BSTNode* left;
    BSTNode* right;

    BSTNode(Route* route) : data(route), left(nullptr), right(nullptr) {}
  };

  BSTNode* root;

  BSTNode* insert(BSTNode* node, Route* route) {
    if (!node) return new BSTNode(route);
    if (route->train_code < node->data->train_code)
      node->left = insert(node->left, route);
    else if (route->train_code > node->data->train_code)
      node->right = insert(node->right, route);
    return node;
  }

  Route* search(BSTNode* node, const string& code) {
    if (!node) return nullptr;
    if (code == node->data->train_code) return node->data;
    if (code < node->data->train_code) return search(node->left, code);
    return search(node->right, code);
  }

  void inorder(BSTNode* node) {
    if (!node) return;
    inorder(node->left);
    cout << "\tTrain Code: " << node->data->train_code
      << " | Train Name: " << node->data->train_name
      << " | Route ID: " << node->data->routeID << endl;
    inorder(node->right);
  }

public:
  BST() : root(nullptr) {}

  void insert(Route* route) {
    root = insert(root, route);
  }

  Route* search(const string& code) {
    return search(root, code);
  }

  void display() {
    inorder(root);
  }
};

// ====================================
//     AVL TREE IMPLEMENTATION
// ====================================
struct AVLNode {
  Route* routeData;
  AVLNode* left;
  AVLNode* right;
  int height;

  AVLNode(Route* data) {
    routeData = data;
    left = right = nullptr;
    height = 1;
  }
};

class AVLTree {
private:
  AVLNode* root;

  int computeHeight(AVLNode* p) {
    if (!p) return 0;
    int leftHeight = computeHeight(p->left);
    int rightHeight = computeHeight(p->right);
    return max(leftHeight, rightHeight) + 1;
  }

  int getBalance(AVLNode* node) {
    return node ? computeHeight(node->left) - computeHeight(node->right) : 0;
  }

  AVLNode* rotateRight(AVLNode* y) {
    AVLNode* x = y->left;
    AVLNode* T2 = x->right;
    x->right = y;
    y->left = T2;
    y->height = computeHeight(y);
    x->height = computeHeight(x);
    return x;
  }

  AVLNode* rotateLeft(AVLNode* x) {
    AVLNode* y = x->right;
    AVLNode* T2 = y->left;
    y->left = x;
    x->right = T2;
    x->height = computeHeight(x);
    y->height = computeHeight(y);
    return y;
  }

  AVLNode* insert(AVLNode* node, Route* route) {
    if (!node) return new AVLNode(route);

    if (route->routeID < node->routeData->routeID)
      node->left = insert(node->left, route);
    else if (route->routeID > node->routeData->routeID)
      node->right = insert(node->right, route);
    else
      return node;

    node->height = computeHeight(node);

    int balance = getBalance(node);

    if (balance > 1 && route->routeID < node->left->routeData->routeID)
      return rotateRight(node);

    if (balance < -1 && route->routeID > node->right->routeData->routeID)
      return rotateLeft(node);

    if (balance > 1 && route->routeID > node->left->routeData->routeID) {
      node->left = rotateLeft(node->left);
      return rotateRight(node);
    }

    if (balance < -1 && route->routeID < node->right->routeData->routeID) {
      node->right = rotateRight(node->right);
      return rotateLeft(node);
    }

    return node;
  }

  void inorder(AVLNode* node) {
    if (!node) return;
    inorder(node->left);
    cout << "RouteID: " << node->routeData->routeID << " | Train: " << node->routeData->train_name << endl;
    inorder(node->right);
  }

public:
  AVLTree() : root(nullptr) {}

  void insert(Route* route) {
    root = insert(root, route);
  }

  void buildFromLinkedList(Route* head) {
    Route* temp = head;
    while (temp) {
      insert(temp);
      temp = temp->next;
    }
  }

  void printInorder() {
    inorder(root);
  }
};

// ====================================
//  HEAP IMPLEMENTATION (MAX-HEAP BY RATING)
// ====================================
class MaxHeap {
private:
  vector<Route*> heap;

  void setHeap(const vector<Route*>& otherHeap) {
    heap = otherHeap;
  }

  vector<Route*> getHeap() const {
    return heap;
  }

  int parent(int i) { return (i - 1) / 2; }
  int leftChild(int i) { return (2 * i + 1); }
  int rightChild(int i) { return (2 * i + 2); }

  void shiftUp(int i) {
    while (i > 0 && heap[parent(i)]->average_rating < heap[i]->average_rating) {
      swap(heap[i], heap[parent(i)]);
      i = parent(i);
    }
  }

  void shiftDown(int i) {
    int maxIndex = i;
    int l = leftChild(i);
    int r = rightChild(i);

    if (l < heap.size() && heap[l]->average_rating > heap[maxIndex]->average_rating)
      maxIndex = l;
    if (r < heap.size() && heap[r]->average_rating > heap[maxIndex]->average_rating)
      maxIndex = r;

    if (i != maxIndex) {
      swap(heap[i], heap[maxIndex]);
      shiftDown(maxIndex);
    }
  }

public:
  void insert(Route* route) {
    heap.push_back(route);
    shiftUp(heap.size() - 1);
  }

  Route* extractMax() {
    if (heap.empty()) throw runtime_error("Heap is empty");
    AVLTree avl;
    avl.buildFromLinkedList(head);

    MaxHeap maxHeap;
    maxHeap.buildFromLinkedList(head);
    Route* result = heap[0];
    heap[0] = heap.back();
    heap.pop_back();
    shiftDown(0);
    return result;
  }

  void buildFromLinkedList(Route* head) {
    Route* temp = head;
    while (temp) {
      insert(temp);
      temp = temp->next;
    }
  }

  void printTopRatedTrains(int count) {
    if (heap.empty()) {
      cout << "\nNo trains available to display.\n";
      return;
    }

    if (count > heap.size()) {
      cout << "Only " << heap.size() << " trains available. Showing all.\n";
      count = heap.size();
    }

    // Create a copy of current MaxHeap object
    MaxHeap tempHeap;
    tempHeap.setHeap(this->getHeap());

    cout << "\nTop Rated Trains:\n";
    for (int i = 0; i < count; ++i) {
      Route* top = tempHeap.extractMax(); 
      cout << i + 1 << ". " << top->train_name << " (Rating: " << top->average_rating << ")\n";
    }
  }
};

// ====================================
//     SEARCHING METHODS
// ====================================
void displayTravelsByTrainName(const string& name) {
  Route* temp = head;
  bool found = false;
  int count = 0;

  cout << "\nTravels by Train \"" << name << "\":\n";
  while (temp) {
    if (temp->train_name == name) {
      cout << ++count << ". Route ID: " << temp->routeID
        << " | Train Code: " << temp->train_code
        << " | Rating: " << temp->average_rating
        << " | Start Date: " << temp->start_date
        << " | Company: " << temp->company << "\n";
      found = true;
    }
    temp = temp->next;
  }

  if (!found) {
    cout << "No travels found for train: " << name << "\n";
  }
}

Route* binarySearchByRouteID(vector<Route*>& sortedRoutes, int routeID) {
  int low = 0, high = sortedRoutes.size() - 1;
  while (low <= high) {
    int mid = low + (high - low) / 2;
    if (sortedRoutes[mid]->routeID == routeID)
      return sortedRoutes[mid];
    else if (sortedRoutes[mid]->routeID < routeID)
      low = mid + 1;
    else
      high = mid - 1;
  }
  return nullptr;
}

// ====================================
//     MERGE SORT BY PASSENGER COUNT
// ====================================
Route* merge(Route* left, Route* right) {
  if (!left) return right;
  if (!right) return left;
  if (left->passenger_count <= right->passenger_count) {
    left->next = merge(left->next, right);
    return left;
  } else {
    right->next = merge(left, right->next);
    return right;
  }
}

void split(Route* source, Route** frontRef, Route** backRef) {
  Route* fast = source->next;
  Route* slow = source;
  while (fast) {
    fast = fast->next;
    if (fast) {
      slow = slow->next;
      fast = fast->next;
    }
  }
  *frontRef = source;
  *backRef = slow->next;
  slow->next = nullptr;
}

void mergeSortByPassengerCount(Route** headRef) {
  Route* head = *headRef;
  if (!head || !head->next) return;
  Route *a, *b;
  split(head, &a, &b);
  mergeSortByPassengerCount(&a);
  mergeSortByPassengerCount(&b);
  *headRef = merge(a, b);
}

void printSortedRoutes(Route* sortedHead) {
  Route* temp = sortedHead;
  while (temp) {
    cout << "RouteID: " << temp->routeID << " | Passengers: " << temp->passenger_count << endl;
    temp = temp->next;
  }
}

// ====================================
//     HASHING - LINEAR PROBING
// ====================================
const int tableSize = 101;  

class HashTable {
private:
  Route* table[tableSize];

  int hashFunc(const string& key) {
    int hash = 0;
    for (char c : key) {
      hash = (hash * 31 + c) % tableSize;
    }
    return hash;
  }

public:
  HashTable() {
    for (int i = 0; i < tableSize; ++i)
      table[i] = nullptr;
  }

  void insert(Route* route) {
    int idx = hashFunc(route->train_code);
    int startIdx = idx;

    while (table[idx] != nullptr) {
      idx = (idx + 1) % tableSize;
      if (idx == startIdx) {
        cout << "Hash table is full!\n";
        return;
      }
    }
    table[idx] = route;
  }

  Route* search(const string& code) {
    int idx = hashFunc(code);
    int startIdx = idx;

    while (table[idx] != nullptr) {
      if (table[idx]->train_code == code)
        return table[idx];
      idx = (idx + 1) % tableSize;
      if (idx == startIdx)
        break;
    }
    return nullptr;
  }

  void buildFromLinkedList(Route* head) {
    #include <iomanip>
    Route* temp = head;
    while (temp) {
      insert(temp);
      temp = temp->next;
    }
  }

  void displayTable() {
    cout << "\n--- Hash Table (train_code) ---\n";
    for (int i = 0; i < tableSize; ++i) {
      if (table[i])
        cout << "[" << i << "] -> " << table[i]->train_code << " (" << table[i]->train_name << ")\n";
    }
  }
};

// ====================================
//     HASHING - CHAINING (WITH BST)
// ====================================
class HashTableChainingBST {
private:
  static const int SIZE = 31;
  BST table[SIZE];

  int hashFunction(const string& key) {
    int hash = 0;
    for (char c : key) {
      hash = (hash * 31 + c) % SIZE;
    }
    return hash;
  }

public:
  void insert(Route* route) {
    int index = hashFunction(route->train_code);
    table[index].insert(route);
  }

  Route* search(const string& train_code) {
    int index = hashFunction(train_code);
    return table[index].search(train_code);
  }

  void displayTable() {
    for (int i = 0; i < SIZE; ++i) {
      cout << "Index " << i << ":\n";
      table[i].display();
    }
  }

  void buildFromLinkedList(Route* head) {
    Route* temp = head;
    while (temp) {
      insert(temp);
      temp = temp->next;
    }
  }
};

// ===========================================
// GRAPHS (Dijkstra, Prims, Kruskal, BFS, DFS)
// ===========================================
#define INF 1e9

class Graph {
private:
  map<string, int> locationIndex;
  vector<string> indexLocation;
  vector<vector<pair<int, double>>> adjList_rating; // for Dijkstra
  vector<vector<pair<int, int>>> adjList_passenger; // for MST
  int V;

public:
  Graph() {
    V = 0;
  }

  void addVertex(string loc) {
    if (locationIndex.find(loc) == locationIndex.end()) {
      locationIndex[loc] = V++;
      indexLocation.push_back(loc);
      adjList_rating.emplace_back();
      adjList_passenger.emplace_back();
    }
  }

  void addEdge(string from, string to, int passenger_count, double average_rating) {
    addVertex(from);
    addVertex(to);
    int u = locationIndex[from];
    int v = locationIndex[to];

    double weight = 1.0 / average_rating; // For Dijkstra (inverse rating)
    adjList_rating[u].push_back({v, weight});
    adjList_rating[v].push_back({u, weight});

    adjList_passenger[u].push_back({v, passenger_count});
    adjList_passenger[v].push_back({u, passenger_count});
    //adjList_passenger[u].push_back({v, -passenger_count});
    //adjList_passenger[v].push_back({u, -passenger_count});
  }

  void dijkstra(string start) {
    vector<double> dist(V, INF);
    vector<int> prev(V, -1);
    priority_queue<pair<double, int>, vector<pair<double, int>>, greater<>> pq;

    int src = locationIndex[start];
    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
      int u = pq.top().second; pq.pop();
      for (auto &[v, w] : adjList_rating[u]) {
        if (dist[u] + w < dist[v]) {
          dist[v] = dist[u] + w;
          prev[v] = u;
          pq.push({dist[v], v});
        }
      }
    }

    cout << "\n=== Best-Rated Travel Routes from " << start << " ===\n";
    cout << "Destination\tTotal Route Score (lower = better-rated segments)\n";
    cout << "----------------------------------------------\n";
    for (int i = 0; i < V; ++i) {
      cout << indexLocation[i] << "\t\t" << fixed << setprecision(4) << dist[i] << endl;
    }
  }

  void primMST() {
    vector<int> parent(V, -1);
    vector<int> key(V, -1); // max passenger count
    vector<bool> inMST(V, false);

    key[0] = INF;

    for (int count = 0; count < V - 1; ++count) {
      int u = -1, maxKey = -1;
      for (int i = 0; i < V; ++i) {
        if (!inMST[i] && key[i] > maxKey) {
          maxKey = key[i];
          u = i;
        }
      }

      if (u == -1) break;

      inMST[u] = true;

      for (auto &[v, w] : adjList_passenger[u]) {
        if (!inMST[v] && w > key[v]) {
          key[v] = w;
          parent[v] = u;
        }
      }
    }

    cout << "\n=== Prim's MST (busiest connections by max passenger count) ===\n";
    cout << "Route\t\tPassenger Count\n";
    cout << "-------------------------------\n";
    for (int i = 1; i < V; ++i) {
      if (parent[i] != -1) {
        cout << indexLocation[parent[i]] << " - " << indexLocation[i]
          << "\t" << key[i] << endl;
      }
    }
  }

  void kruskalMST() {
    vector<tuple<int, int, int>> edges;
    for (int u = 0; u < V; ++u)
      for (auto &[v, w] : adjList_passenger[u])
      if (u < v) edges.emplace_back(w, u, v);

    sort(edges.rbegin(), edges.rend()); // Sort by max passenger count (descending)

    vector<int> parent(V);
    iota(parent.begin(), parent.end(), 0);

    function<int(int)> find = [&](int u) {
      return parent[u] == u ? u : parent[u] = find(parent[u]);
    };

    cout << "\n=== Kruskal's MST (busiest connections by max passenger count) ===\n";
    cout << "Route\t\tPassenger Count\n";
    cout << "-------------------------------\n";

    for (auto &[w, u, v] : edges) {
      int setU = find(u), setV = find(v);
      if (setU != setV) {
        cout << indexLocation[u] << " - " << indexLocation[v]
          << "\t" << w << endl;
        parent[setU] = setV;
      }
    }
  }

  void bfs(string start) {
    vector<bool> visited(V, false);
    Queue<int> q;

    int src = locationIndex[start];
    q.enqueue(src);
    visited[src] = true;

    cout << "\n=== Breadth-First Exploration from " << start << " ===\n";
    cout << "Visited Cities (Layer by Layer):\n";
    while (!q.isEmpty()) {
      int u = q.peek(); q.dequeue();
      cout << indexLocation[u] << " ";
      for (auto &[v, _] : adjList_passenger[u]) {
        if (!visited[v]) {
          visited[v] = true;
          q.enqueue(v);
        }
      }
    }
    cout << endl;
  }

  void dfsUtil(int u, vector<bool> &visited) {
    visited[u] = true;
    cout << indexLocation[u] << " ";
    for (auto &[v, _] : adjList_passenger[u]) {
      if (!visited[v])
        dfsUtil(v, visited);
    }
  }

  void dfs(string start) {
    vector<bool> visited(V, false);
    cout << "\n=== Depth-First Exploration from " << start << " ===\n";
    cout << "Visited Cities (Deep Dive Order):\n";
    dfsUtil(locationIndex[start], visited);
    cout << endl;
  }
};

// ====================================
//     MAIN METHOD: MENU DRIVEN
// ====================================

// --- Helper Function for Train Code Lookup ---
void handleTrainCodeLookup(HashTable& hashTable, HashTableChainingBST& chainingHashTable) {
  int methodChoice;
  do {
    cout << "\n--- Select Hashing Method ---\n";
    cout << "1. Linear Probing\n";
    cout << "2. Chaining (with BST)\n";
    cout << "3. Return to Main Menu\n";
    cout << "Enter your choice: ";
    cin >> methodChoice;

    if (methodChoice == 1) {
      int subChoice;
      do {
        cout << "\n--- Train Code Lookup (Linear Probing) ---\n";
        cout << "1. Lookup Train by train_code\n";
        cout << "2. Display Hash Table\n";
        cout << "3. Return\n";
        cout << "Enter your choice: ";
        cin >> subChoice;

        if (subChoice == 1) {
          string code;
          cout << "Enter train_code to lookup: ";
          cin >> code;
          Route* found = hashTable.search(code);
          if (found) {
            cout << "Train: " << found->train_name
              << " | Route ID: " << found->routeID
              << " | Passengers: " << found->passenger_count
              << " | Rating: " << found->average_rating << endl;
          } else {
            cout << "Train code not found.\n";
          }
        } else if (subChoice == 2) {
          hashTable.displayTable();
        } else if (subChoice != 3) {
          cout << "Invalid option.\n";
        }
      } while (subChoice != 3);

    } else if (methodChoice == 2) {
      int subChoice;
      do {
        cout << "\n--- Train Code Lookup (Chaining - BST) ---\n";
        cout << "1. Lookup Train by train_code\n";
        cout << "2. Display Hash Table\n";
        cout << "3. Return\n";
        cout << "Enter your choice: ";
        cin >> subChoice;

        if (subChoice == 1) {
          string code;
          cout << "Enter train_code to lookup: ";
          cin >> code;
          Route* found = chainingHashTable.search(code);
          if (found) {
            cout << "\tTrain: " << found->train_name
              << " | Route ID: " << found->routeID
              << " | Passengers: " << found->passenger_count
              << " | Rating: " << found->average_rating << endl;
          } else {
            cout << "Train code not found.\n";
          }
        } else if (subChoice == 2) {
          chainingHashTable.displayTable();
        } else if (subChoice != 3) {
          cout << "Invalid option.\n";
        }
      } while (subChoice != 3);

    } else if (methodChoice != 3) {
      cout << "Invalid method option.\n";
    }

  } while (methodChoice != 3);
}

// --- GRAPH MENU FUNCTION ---
void GraphFeatures(Graph &graph) {
  int option;
  string start;
  do {
    cout << "\n===== GRAPH FEATURES =====\n";
    cout << "1. Dijkstra (Find Best-Rated Routes)\n2. Prim's MST (busiest connections - max passenger count)"
      <<"\n3. Kruskal's MST (busiest connections - max passenger count)"
      <<"\n4. BFS\n5. DFS\n0. Return\nChoice: ";
    cin >> option;
    if (option >= 1 && option <= 5) {
      cout << "Enter start location: ";
      cin >> start;
    }
    switch(option) {
      case 1: graph.dijkstra(start); break;
      case 2: graph.primMST(); break;
      case 3: graph.kruskalMST(); break;
      case 4: graph.bfs(start); break;
      case 5: graph.dfs(start); break;
      case 0: break;
      default: cout << "Invalid option.\n";
    }
  } while(option != 0);
}

int main() {
  ifstream file("Railway_DataSet_With_Locations.csv");
  string line;
  Graph graph;

  // Skip the header line
  getline(file, line);

  while (getline(file, line)) {
    stringstream ss(line);
    string routeID, train_name, operators, avg_rating, train_code, route_code;
    string lang_code, num_stations, passenger_count, reviews_count, start_date, company, fromLocation, toLocation;

    // Read and split the line
    getline(ss, routeID, ',');
    getline(ss, train_name, ',');
    getline(ss, operators, ',');
    getline(ss, avg_rating, ',');
    getline(ss, train_code, ',');
    getline(ss, route_code, ',');
    getline(ss, lang_code, ',');
    getline(ss, num_stations, ',');
    getline(ss, passenger_count, ',');
    getline(ss, reviews_count, ',');
    getline(ss, start_date, ',');
    getline(ss, company, ',');
    getline(ss, fromLocation, ',');
    getline(ss, toLocation);

    // Convert necessary fields to int/float
    try {
      int rid = stoi(routeID);
      float rating = stof(avg_rating);
      int stations = stoi(num_stations);
      int passengers = stoi(passenger_count);
      int reviews = stoi(reviews_count);

      addRoute(rid, train_name, operators, rating, train_code, route_code, lang_code,
               stations, passengers, reviews, start_date, company, fromLocation, toLocation);
      graph.addEdge(fromLocation, toLocation, passengers, rating);
    } catch (invalid_argument& e) {
      // Skip if any conversion fails
      continue;
    }
  }

  // Build AVL and MaxHeap from the linked list
  AVLTree avl;
  avl.buildFromLinkedList(head);

  MaxHeap maxHeap;
  maxHeap.buildFromLinkedList(head);

  HashTable hashTable;
  hashTable.buildFromLinkedList(head);

  HashTableChainingBST chainingHashTable;
  chainingHashTable.buildFromLinkedList(head);

  // --------- MENU LOOP ----------
  int choice;
  do {
    cout << "\n--- Railway Management System ---\n";
    cout << "1. Print All Routes\n";
    cout << "2. Print AVL Inorder Traversal (by RouteID)\n";
    cout << "3. Show Top-Rated Trains (by Rating)\n";
    cout << "4. Display Travels by Train Name (Linear Search)\n";
    cout << "5. Search Route by RouteID (Binary Search)\n";
    cout << "6. Sort Routes by Passenger Count (Merge Sort)\n";
    cout << "7. Lookup Train by train_code (Choose Hashing Method)\n";
    cout << "8. Explore Graph Algorithms (Dijkstra, MST, BFS, DFS)\n";
    cout << "0. Exit\n";
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1:
        printAllRoutes();
        break;

      case 2:
        avl.printInorder();
        break;

      case 3: {
        int n;
        cout << "Enter how many top-rated trains to display: ";
        cin >> n;
        if (n <= 0) {
          cout << "Please enter a valid number greater than 0.\n";
          break;
        }
        maxHeap.printTopRatedTrains(n);
        break;
      }

      case 4: {
        string trainName;
        cout << "Enter train name to view its travels: ";
        cin.ignore();
        getline(cin, trainName);
        displayTravelsByTrainName(trainName);
        break;
      }

      case 5: {
        vector<Route*> sortedRoutes;
        Route* temp = head;
        while (temp) {
          sortedRoutes.push_back(temp);
          temp = temp->next;
        }
        sort(sortedRoutes.begin(), sortedRoutes.end(), [](Route* a, Route* b) {
          return a->routeID < b->routeID;
        });
        int id;
        cout << "Enter RouteID to search: ";
        cin >> id;
        Route* result = binarySearchByRouteID(sortedRoutes, id);
        if (result)
          cout << "Train Found: " << result->train_name << " (Passengers: " << result->passenger_count << ")\n";
        else
          cout << "Route not found.\n";
        break;
      }

      case 6: {
        Route* sorted = head;
        mergeSortByPassengerCount(&sorted);
        printSortedRoutes(sorted);
        break;
      }

      case 7:
        handleTrainCodeLookup(hashTable, chainingHashTable);
        break;

      case 8:
        GraphFeatures(graph);
        break;

      case 0:
        cout << "Exiting...\n";
        break;

      default:
        cout << "Invalid choice.\n";
    }

  } while (choice != 0);

  return 0;
}

