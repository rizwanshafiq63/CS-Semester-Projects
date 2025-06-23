#include <iostream>
#include <string>

using namespace std;

// Structure
struct Person {
    string name;
    int age;
    float salary;
};

int main() {
    // Variables
    int myInt = 10;
    double myDouble = 5.5;
    char myChar = 'A';
    string myString = "Hello World!";
    bool myBool = true;

    // Output
    cout << "Integer: " << myInt << endl;
    cout << "Double: " << myDouble << endl;
    cout << "Character: " << myChar << endl;
    cout << "String: " << myString << endl;
    cout << "Boolean: " << myBool << endl;

    // Constants
    const int myConst = 100;
    cout << "Constant: " << myConst << endl;

    // User Input
    int userNum;
    cout << "Enter a number: ";
    cin >> userNum;
    cout << "You entered: " << userNum << endl;

    // Arrays
    int myArray[3] = {1, 2, 3};
    cout << "Array elements: ";
    for (int i = 0; i < 3; i++) {
        cout << myArray[i] << " ";
    }
    cout << endl;

    // Switch Case
    int day = 2;
    switch (day) {
        case 1:
            cout << "Monday" << endl;
            break;
        case 2:
            cout << "Tuesday" << endl;
            break;
        default:
            cout << "Another day" << endl;
    }

    // Loops
    cout << "Loop Output: ";
    for (int i = 0; i < 5; i++) {
        cout << i << " ";
    }
    cout << endl;

    // Function
    int add(int, int);
    
    // Function Call
    cout << "Addition of 5 and 10: " << add(5, 10) << endl;

    // Structure Example
    Person p1;
    cout << "Enter your name: ";
    cin.ignore(); // To clear previous input buffer
    getline(cin, p1.name);
    cout << "Enter your age: ";
    cin >> p1.age;
    cout << "Enter your salary: ";
    cin >> p1.salary;

    // Display Structure Data
    cout << "\nDisplaying Information:" << endl;
    cout << "Name: " << p1.name << endl;
    cout << "Age: " << p1.age << endl;
    cout << "Salary: " << p1.salary << endl;

    return 0;
}

// Function Definition
int add(int a, int b) {
    return a + b;
}
