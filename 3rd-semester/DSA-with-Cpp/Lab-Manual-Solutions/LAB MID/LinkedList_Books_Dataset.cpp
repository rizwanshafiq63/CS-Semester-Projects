#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <stack>
#include <queue>
#include <string>
using namespace std;

struct Node {
    string title;
    string author;
    float rating;
    int pages;
    string language;
    string publisher;
    Node* next;
    Node* prev;
};

Node* head = NULL;
Node* tail = NULL;

// Stack to hold sets of deleted books for undo
stack<vector<Node*>> deletedBooksStack;

// Add a book to the linked list
void addBook(string title, string author, float rating, int pages, string language, string publisher) {
    Node* new_node = new Node{title, author, rating, pages, language, publisher, NULL, NULL};
    if (head == NULL) {
        head = tail = new_node;
    } else {
        new_node->prev = tail;
        tail->next = new_node;
        tail = new_node;
    }
}

// Print all books
void printAllBooks() {
    Node* ptr = head;
    cout << "Title | Author | Rating | Pages | Language | Publisher\n";
    while (ptr) {
        cout << ptr->title << " | " << ptr->author << " | " << ptr->rating << " | " << ptr->pages
             << " | " << ptr->language << " | " << ptr->publisher << "\n";
        ptr = ptr->next;
    }
}

// Print books by language
void printByLanguage(string lang) {
    Node* ptr = head;
    cout << "Books in language: " << lang << "\n";
    cout << "Title | Author | Rating | Pages | Language | Publisher\n";
    while (ptr) {
        if (ptr->language == lang) {
            cout << ptr->title << " | " << ptr->author << " | " << ptr->rating << " | " << ptr->pages
                 << " | " << ptr->language << " | " << ptr->publisher << "\n";
        }
        ptr = ptr->next;
    }
}

// Print books with rating greater than X
void printRatingGreater(float minRating) {
    Node* ptr = head;
    cout << "Books with rating > " << minRating << "\n";
    cout << "Title | Author | Rating | Pages | Language | Publisher\n";
    while (ptr) {
        if (ptr->rating > minRating) {
            cout << ptr->title << " | " << ptr->author << " | " << ptr->rating << " | " << ptr->pages
                 << " | " << ptr->language << " | " << ptr->publisher << "\n";
        }
        ptr = ptr->next;
    }
}

// Delete books with pages < minPages
void deleteLowPageBooks(int minPages) {
    Node* ptr = head;
    vector<Node*> deletedThisRound;

    while (ptr) {
        if (ptr->pages < minPages) {
            Node* toDelete = ptr;

            // Save copy for undo
            Node* backup = new Node{toDelete->title, toDelete->author, toDelete->rating,
                                    toDelete->pages, toDelete->language, toDelete->publisher, NULL, NULL};
            deletedThisRound.push_back(backup);

            // Delete logic
            if (ptr == head && ptr == tail) {
                head = tail = NULL;
            } else if (ptr == head) {
                head = head->next;
                if (head) head->prev = NULL;
            } else if (ptr == tail) {
                tail = tail->prev;
                if (tail) tail->next = NULL;
            } else {
                ptr->prev->next = ptr->next;
                ptr->next->prev = ptr->prev;
            }

            ptr = ptr->next;
            delete toDelete;
        } else {
            ptr = ptr->next;
        }
    }

    if (!deletedThisRound.empty()) {
        deletedBooksStack.push(deletedThisRound);
        cout << deletedThisRound.size() << " book(s) deleted and saved for undo.\n";
    }
}

void undoDelete() {
    if (deletedBooksStack.empty()) {
        cout << "No deleted books to undo.\n";
        return;
    }

    vector<Node*> lastDeleted = deletedBooksStack.top();
    deletedBooksStack.pop();

    for (Node* book : lastDeleted) {
        // Reinserting at the end
        book->next = NULL;
        book->prev = tail;
        if (tail) tail->next = book;
        else head = book;  // list was empty
        tail = book;
    }

    cout << lastDeleted.size() << " book(s) restored.\n";
}

// Print books by a specific author using a queue
void printByAuthor(string authorName) {
    Node* ptr = head;
    bool found = false;
    queue<Node*> booksQueue;  // Create a queue to hold books by the author

    cout << "Books by: " << authorName << "\n";
    cout << "Title | Author | Rating | Pages | Language | Publisher\n";

    // Traverse through the linked list and check for exact author match
    while (ptr) {
        if (ptr->author == authorName) { 
            booksQueue.push(ptr);  
            found = true;
        }
        ptr = ptr->next;
    }

    // If any books were found, print them from the queue
    if (found) {
        while (!booksQueue.empty()) {
            Node* book = booksQueue.front();
            booksQueue.pop();
            cout << book->title << " | " << book->author << " | " << book->rating << " | " << book->pages
                 << " | " << book->language << " | " << book->publisher << "\n";
        }
    } else {
        cout << "No books found by " << authorName << ".\n";
    }
}



int main() {
    ifstream fin("books.csv");
    string line;
    getline(fin, line);

    while (getline(fin, line)) {
        stringstream ss(line);
        string bookID, title, authors, avg_rating, isbn, isbn13, lang, pages, ratings, reviews, pub_date, publisher;

        getline(ss, bookID, ',');
        getline(ss, title, ',');
        getline(ss, authors, ',');
        getline(ss, avg_rating, ',');
        getline(ss, isbn, ',');
        getline(ss, isbn13, ',');
        getline(ss, lang, ',');
        getline(ss, pages, ',');
        getline(ss, ratings, ',');
        getline(ss, reviews, ',');
        getline(ss, pub_date, ',');
        getline(ss, publisher);

        float rating;
        int numPages;

        try {
            rating = stof(avg_rating);
            numPages = stoi(pages);
        } catch (invalid_argument& e) {
            // Skip rows with invalid numbers
            continue;
        }

        addBook(title, authors, rating, numPages, lang, publisher);
    }

    int choice;
    do {
        cout << "\nMenu:\n";
        cout << "1. Print all books\n";
        cout << "2. Print books by language\n";
        cout << "3. Print books with rating > X\n";
        cout << "4. Delete books with pages < Y\n";
        cout << "5. Print books by author\n";
        cout << "6. Undo last delete\n";
        cout << "0. Exit\n";
        cout << "Enter choice: ";
        cin >> choice;
        cin.ignore();

        switch (choice) {
            case 1:
                printAllBooks();
                break;
            case 2: {
                string lang;
                cout << "Enter language code (e.g., eng): ";
                cin >> lang;
                printByLanguage(lang);
                break;
            }
            case 3: {
                float rating;
                cout << "Enter minimum rating: ";
                cin >> rating;
                printRatingGreater(rating);
                break;
            }
            case 4: {
                int pages;
                cout << "Enter minimum number of pages: ";
                cin >> pages;
                deleteLowPageBooks(pages);
                break;
            }
            case 5: {
                string author;
                cout << "Enter author name: ";
                //cin.ignore();
                getline(cin, author);
                printByAuthor(author);
                break;
            }
            case 6:
                undoDelete();
                break;         
            case 0:
                cout << "Exiting...\n";
                break;
            default:
                cout << "Invalid choice!\n";
        }

    } while (choice != 0);

    return 0;
}
