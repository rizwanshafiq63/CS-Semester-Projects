/* Write a program that uses an ArrayList of parameter type Contact to store a database of contacts. The Contact class should store the contact’s first and last name, phone number, and email address. Add appropriate accessor and mutator methods. Your database program should present a menu that allows the user to add a contact, display all contacts, search for a specific contact and display it, or search for a specific contact and give the user the option to delete it. The searches should find any contact where any instance variable contains a target search string. For example, if “elmore” is the search target, then any contact where the first name, last name, phone number, or email address contains “elmore” should be returned for display or deletion. Use the “for-each” loop to iterate through the ArrayList */

import java.util.ArrayList;
import java.util.Scanner;

class Contact {
    private String firstName;
    private String lastName;
    private String phoneNumber;
    private String email;

    // Constructor
    public Contact(String firstName, String lastName, String phoneNumber, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.phoneNumber = phoneNumber;
        this.email = email;
    }

    // Accessor (Getter) methods
    public String getFirstName() {
        return firstName;
    }
    public String getLastName() {
        return lastName;
    }
    public String getPhoneNumber() {
        return phoneNumber;
    }
    public String getEmail() {
        return email;
    }

    // Mutator (Setter) methods
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }
    public void setEmail(String email) {
        this.email = email;
    }

    // Display method
    public void displayContact() {
        System.out.println("Name: " + firstName + " " + lastName);
        System.out.println("Phone: " + phoneNumber);
        System.out.println("Email: " + email);
        System.out.println("-----------------------------");
    }

    // Check if any field contains the search keyword (case insensitive)
    public boolean contains(String keyword) {
        keyword = keyword.toLowerCase();
        return firstName.toLowerCase().contains(keyword)
                || lastName.toLowerCase().contains(keyword)
                || phoneNumber.toLowerCase().contains(keyword)
                || email.toLowerCase().contains(keyword);
    }
}

public class Lab10_Task_01 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayList<Contact> contacts = new ArrayList<>();
        int choice;

        do {
            System.out.println("\n====== Contact Manager ======");
            System.out.println("1. Add Contact");
            System.out.println("2. Display All Contacts");
            System.out.println("3. Search Contact");
            System.out.println("4. Search and Delete Contact");
            System.out.println("5. Exit");
            System.out.print("Choose an option: ");
            choice = scanner.nextInt();
            scanner.nextLine();  // consume newline

            switch (choice) {
                case 1:
                    System.out.print("Enter First Name: ");
                    String firstName = scanner.nextLine();
                    System.out.print("Enter Last Name: ");
                    String lastName = scanner.nextLine();
                    System.out.print("Enter Phone Number: ");
                    String phone = scanner.nextLine();
                    System.out.print("Enter Email Address: ");
                    String email = scanner.nextLine();
                    contacts.add(new Contact(firstName, lastName, phone, email));
                    System.out.println("Contact added successfully!");
                    break;

                case 2:
                    if (contacts.isEmpty()) {
                        System.out.println("No contacts to display.");
                    } else {
                        for (Contact c : contacts) {
                            c.displayContact();
                        }
                    }
                    break;

                case 3:
                    System.out.print("Enter search keyword: ");
                    String keyword = scanner.nextLine();
                    boolean found = false;
                    for (Contact c : contacts) {
                        if (c.contains(keyword)) {
                            c.displayContact();
                            found = true;
                        }
                    }
                    if (!found) {
                        System.out.println("No matching contact found.");
                    }
                    break;

                case 4:
                    System.out.print("Enter keyword to search for deletion: ");
                    String deleteKeyword = scanner.nextLine();
                    boolean deleted = false;
                    for (Contact c : contacts) {
                        if (c.contains(deleteKeyword)) {
                            c.displayContact();
                            System.out.print("Do you want to delete this contact? (yes/no): ");
                            String confirm = scanner.nextLine();
                            if (confirm.equalsIgnoreCase("yes")) {
                                contacts.remove(c);
                                System.out.println("Contact deleted.");
                                deleted = true;
                                break; // prevent ConcurrentModificationException
                            }
                        }
                    }
                    if (!deleted) {
                        System.out.println("No matching contact was deleted.");
                    }
                    break;

                case 5:
                    System.out.println("Exiting... Goodbye!");
                    break;

                default:
                    System.out.println("Invalid choice. Try again.");
            }

        } while (choice != 5);

        scanner.close();
    }
}

