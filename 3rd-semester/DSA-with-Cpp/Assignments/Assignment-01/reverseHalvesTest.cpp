#include <iostream>
using namespace std;

struct Singly {
    int data;
    Singly* snext;
};

// Function to insert a node at the end
void insert(Singly*& sfirst, int val) {
    Singly* newNode = new Singly{val, NULL};
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

// Function to print the list
void printList(Singly* sfirst) {
    while (sfirst != NULL) {
        cout << sfirst->data << " -> ";
        sfirst = sfirst->snext;
    }
    cout << "NULL" << endl;
}
void reverseHalves(Singly*& sfirst) {
    if (sfirst == NULL) {
        cout << "List is Empty." << endl;
        return;
    }
    if (sfirst->snext == NULL) { // Only one node in the list
        cout << "Only one node in the List. No reverse needed." << endl;
        return;
    }

    // Step 1: Find the middle of the linked list
    Singly *slow = sfirst, *fast = sfirst, *firstHalfEnd = NULL;
    while (fast != NULL && fast->snext != NULL) {
        firstHalfEnd = slow; // Store the last node of first half
        slow = slow->snext;
        fast = fast->snext->snext;
    }

    // Step 2: Break the list into two halves
    firstHalfEnd->snext = NULL; // First half ends here, second half starts from slow

    // Step 3: Reverse the first half (and track its last node)
    Singly *prev = NULL, *curr = sfirst, *next = NULL;
    while (curr != NULL) {
        next = curr->snext;
        curr->snext = prev;
        prev = curr;
        curr = next;
    }
    firstHalfEnd = sfirst; // firstHalfEnd is actually the last node of reversed first half
    sfirst = prev; // New head of reversed first half
    // Step 4: Reverse the second half
    prev = NULL, curr = slow, next = NULL;
    while (curr != NULL) {
        next = curr->snext;
        curr->snext = prev;
        prev = curr;
        curr = next;
    }

    // Step 5: Directly connect firstHalfEnd to the reversed second half
    firstHalfEnd->snext = prev;

    cout << "List after reversing halves: ";
    printList(sfirst);
    cout << endl;
}

int main() {
    Singly* sfirst = NULL;

    insert(sfirst, 1);
    insert(sfirst, 2);
    insert(sfirst, 3);
    insert(sfirst, 4);
    insert(sfirst, 5);
    insert(sfirst, 6);
    insert(sfirst, 7);
    insert(sfirst, 8);

    cout << "Original List: ";
    printList(sfirst);

    reverseHalves(sfirst);

    return 0;
}
