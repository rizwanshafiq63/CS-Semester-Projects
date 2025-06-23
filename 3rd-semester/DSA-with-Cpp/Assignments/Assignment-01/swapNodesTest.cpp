#include <iostream>
using namespace std;

struct Singly {
    int sdata;
    Singly* snext;
};

// Global head pointer
Singly* sfirst = NULL;

// Function to swap two nodes by changing links
void swapNodes(int key1, int key2) {
    if (sfirst == NULL) {
        cout << "List is Empty." << endl;
        return;
    }
    if (sfirst->snext == NULL) { // Only one node in the list
        cout << "Only one node. No swap possible." << endl;
        return;
    }
    if (key1 == key2) {
        cout << "Both keys are the same, no swap needed." << endl;
        return;
    }

    // Find x and y along with their previous nodes
    Singly *prevX = NULL, *prevY = NULL, *x = sfirst, *y = sfirst;
    while (x && x->sdata != key1) {
        prevX = x;
        x = x->snext;
    }
    while (y && y->sdata != key2) {
        prevY = y;
        y = y->snext;
    }

    // If either node is not found, return
    if (!x || !y) {
        cout << "One or both keys are not in the list." << endl;
        return;
    }

    // If x is not the head, update its previous node to point to y
    if (prevX != NULL)
        prevX->snext = y;
    else // Make y the new head
        sfirst = y;

    // If y is not the head, update its previous node to point to x
    if (prevY != NULL)
        prevY->snext = x;
    else // Make x the new head
        sfirst = x;

    // Swap next pointers
    Singly *temp = x->snext;
    x->snext = y->snext;
    y->snext = temp;

    cout << "Nodes swapped successfully." << endl;
}

// Function to insert a new node at the end of the list
void insertNode(int data) {
    Singly* newNode = new Singly{data, NULL};
    if (sfirst == NULL) {
        sfirst = newNode;
        return;
    }
    Singly* temp = sfirst;
    while (temp->snext != NULL) {
        temp = temp->snext;
    }
    temp->snext = newNode;
}

// Function to print the linked list
void printList() {
    Singly* temp = sfirst;
    while (temp != NULL) {
        cout << temp->sdata << " → ";
        temp = temp->snext;
    }
    cout << "NULL" << endl;
}

// Main function to test swapping
int main() {
    insertNode(1);
    insertNode(2);
    insertNode(3);
    insertNode(4);
    insertNode(5);
    insertNode(6);

    cout << "Original List: ";
    printList();

    // Test swapping adjacent nodes (e.g., swapping 3 and 4)
    swapNodes(3, 4);
    cout << "After Swapping 3 and 4: ";
    printList();

    // Test swapping non-adjacent nodes (e.g., swapping 2 and 5)
    swapNodes(2, 5);
    cout << "After Swapping 2 and 5: ";
    printList();

    // Test case where both keys are the same
    swapNodes(2, 2);

    // Test case where one key is missing
    swapNodes(2, 10);

    // Test case where there is only one node
    sfirst = new Singly{7, NULL};
    swapNodes(7, 8);

    return 0;
}

