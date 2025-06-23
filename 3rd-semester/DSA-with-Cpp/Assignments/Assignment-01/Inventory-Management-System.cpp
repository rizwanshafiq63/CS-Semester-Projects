#include <iostream>
#include <string>
using namespace std;

// =============================
// Doubly Linked List for Items
// =============================
struct Item {
  string itemName;
  Item* prev = NULL;
  Item* next = NULL;
};

// =============================
// Doubly Linked List for Sections
// =============================
struct Section {
  string sectionName;
  Item* itemFirst = NULL;
  Item* itemLast = NULL;
  Section* prev = NULL;
  Section* next = NULL;
};

// =============================
// Doubly Linked List for Stores
// =============================
struct Store {
  string storeName;
  Section* sectionFirst = NULL;
  Section* sectionLast = NULL;
  Store* prev = NULL;
  Store* next = NULL;
};

Store* storeFirst = NULL;
Store* storeLast = NULL;

// ===========================================
// Function to Add a New Section in a Store
// ===========================================
void addSectionToStore(string storeName, string sectionName) {
  Store* storePtr = storeFirst;
  while (storePtr && storePtr->storeName != storeName)
    storePtr = storePtr->next;

  if (!storePtr) {
    cout << "Store not found!" << endl;
    return;
  }

  Section* newSection = new Section;
  newSection->sectionName = sectionName;

  if (!storePtr->sectionFirst) {
    storePtr->sectionFirst = storePtr->sectionLast = newSection;
  } else {
    storePtr->sectionLast->next = newSection;
    newSection->prev = storePtr->sectionLast;
    storePtr->sectionLast = newSection;
  }
  cout << "Section added successfully." << endl;
}

// ===========================================
// Function to Add Item to a Section in a Store
// ===========================================
void addItemToSection(string storeName, string sectionName, string itemName) {
  Store* storePtr = storeFirst;
  while (storePtr && storePtr->storeName != storeName)
    storePtr = storePtr->next;
  if (!storePtr) {
    cout << "Store not found!" << endl;
    return;
  }

  Section* sectionPtr = storePtr->sectionFirst;
  while (sectionPtr && sectionPtr->sectionName != sectionName)
    sectionPtr = sectionPtr->next;
  if (!sectionPtr) {
    cout << "Section not found!" << endl;
    return;
  }

  Item* newItem = new Item;
  newItem->itemName = itemName;

  if (!sectionPtr->itemFirst) {
    sectionPtr->itemFirst = sectionPtr->itemLast = newItem;
  } else {
    sectionPtr->itemLast->next = newItem;
    newItem->prev = sectionPtr->itemLast;
    sectionPtr->itemLast = newItem;
  }
  cout << "Item added successfully." << endl;
}

// ===========================================
// Function to Remove Item from Section
// ===========================================
void removeItemFromSection(string storeName, string sectionName, string itemName) {
  Store* storePtr = storeFirst;
  while (storePtr && storePtr->storeName != storeName)
    storePtr = storePtr->next;
  if (!storePtr) {
    cout << "Store not found!" << endl;
    return;
  }

  Section* sectionPtr = storePtr->sectionFirst;
  while (sectionPtr && sectionPtr->sectionName != sectionName)
    sectionPtr = sectionPtr->next;
  if (!sectionPtr) {
    cout << "Section not found!" << endl;
    return;
  }

  Item* itemPtr = sectionPtr->itemFirst;
  while (itemPtr && itemPtr->itemName != itemName)
    itemPtr = itemPtr->next;
  if (!itemPtr) {
    cout << "Item not found!" << endl;
    return;
  }

  if (itemPtr->prev)
    itemPtr->prev->next = itemPtr->next;
  else
    sectionPtr->itemFirst = itemPtr->next;

  if (itemPtr->next)
    itemPtr->next->prev = itemPtr->prev;
  else
    sectionPtr->itemLast = itemPtr->prev;

  delete itemPtr;
  cout << "Item removed successfully." << endl;
}

// ===========================================
// Function to Display Items of a Section
// ===========================================
void displayItemsOfSection(string storeName, string sectionName) {
  Store* storePtr = storeFirst;
  while (storePtr && storePtr->storeName != storeName)
    storePtr = storePtr->next;
  if (!storePtr) {
    cout << "Store not found!" << endl;
    return;
  }

  Section* sectionPtr = storePtr->sectionFirst;
  while (sectionPtr && sectionPtr->sectionName != sectionName)
    sectionPtr = sectionPtr->next;
  if (!sectionPtr) {
    cout << "Section not found!" << endl;
    return;
  }

  cout << "Items in section '" << sectionName << "': " << endl;
  Item* itemPtr = sectionPtr->itemFirst;
  while (itemPtr) {
    cout << "  - " << itemPtr->itemName << endl;
    itemPtr = itemPtr->next;
  }
}

// ===========================================
// Function to Display Items of a Store
// ===========================================
void displayItemsOfStore(string storeName) {
  Store* storePtr = storeFirst;
  while (storePtr && storePtr->storeName != storeName)
    storePtr = storePtr->next;
  if (!storePtr) {
    cout << "Store not found!" << endl;
    return;
  }

  cout << "Items in store '" << storeName << "':" << endl;
  Section* sectionPtr = storePtr->sectionFirst;
  while (sectionPtr) {
    cout << "Section: " << sectionPtr->sectionName << endl;
    Item* itemPtr = sectionPtr->itemFirst;
    while (itemPtr) {
      cout << "  - " << itemPtr->itemName << endl;
      itemPtr = itemPtr->next;
    }
    sectionPtr = sectionPtr->next;
  }
}

// ===========================================
// Function to Add a New Store
// ===========================================
void addStore(string storeName) {
  Store* newStore = new Store;
  newStore->storeName = storeName;

  if (!storeFirst) {
    storeFirst = storeLast = newStore;
  } else {
    storeLast->next = newStore;
    newStore->prev = storeLast;
    storeLast = newStore;
  }
  cout << "Store added successfully." << endl;
}

// ===========================================
// Main Function
// ===========================================
/*
// MENU DRIVEN MAIN WITH TERMINATION CONDITION
void displayMenu() {
  cout << "\n=========== OPTIONS MENU ===========\n";
  cout << "1. Add Store\n";
  cout << "2. Add Section to Store\n";
  cout << "3. Add Item to Section\n";
  cout << "4. Remove Item from Section\n";
  cout << "5. Display Items of Section\n";
  cout << "6. Display Items of Store\n";
  cout << "0. Exit\n";
}
void menu() {
  int choice;
  while (true) {
    displayMenu();
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
      case 1: {
        string storeName;
        cout << "Enter store name: ";
        cin >> storeName;
        addStore(storeName);
        break;
      }
      case 2: {
        string storeName, sectionName;
        cout << "Enter store name: ";
        cin >> storeName;
        cout << "Enter section name: ";
        cin >> sectionName;
        addSectionToStore(storeName, sectionName);
        break;
      }
      case 3: {
        string storeName, sectionName, itemName;
        cout << "Enter store name: ";
        cin >> storeName;
        cout << "Enter section name: ";
        cin >> sectionName;
        cout << "Enter item name: ";
        cin >> itemName;
        addItemToSection(storeName, sectionName, itemName);
        break;
      }
      case 4: {
        string storeName, sectionName, itemName;
        cout << "Enter store name: ";
        cin >> storeName;
        cout << "Enter section name: ";
        cin >> sectionName;
        cout << "Enter item name to remove: ";
        cin >> itemName;
        removeItemFromSection(storeName, sectionName, itemName);
        break;
      }
      case 5: {
        string storeName, sectionName;
        cout << "Enter store name: ";
        cin >> storeName;
        cout << "Enter section name: ";
        cin >> sectionName;
        displayItemsOfSection(storeName, sectionName);
        break;
      }
      case 6: {
        string storeName;
        cout << "Enter store name: ";
        cin >> storeName;
        displayItemsOfStore(storeName);
        break;
      }
      case 0:
          return; // Exit the program
      default:
          cout << "Invalid choice! Please try again." << endl;
    }
  }
}
int main() {
  menu();
  return 0;
}
*/

// QUICK TEST
int main() {
  addStore("Lahore Store");
  addSectionToStore("Lahore Store", "Toys");
  addItemToSection("Lahore Store", "Toys", "Remote Car");
  addItemToSection("Lahore Store", "Toys", "Teddy Bear");
  displayItemsOfSection("Lahore Store", "Toys");
  displayItemsOfStore("Lahore Store");
  removeItemFromSection("Lahore Store", "Toys", "Remote Car");
  displayItemsOfSection("Lahore Store", "Toys");
  return 0;
} 

