import java.util.Scanner;

public class AddressBook {
    
    static String[] names = new String[100];
    static String[] emails = new String[100];
    static String[] phones = new String[100];
    static String[] notes = new String[100];
    static int contactCount = 0;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        boolean exit = false;

        while (!exit) {
            System.out.println("\nMain Window:\n=============\n(1) Add a new contact\n(2) Search for contact\n(3) Display all contacts\n(4) Quit");
            System.out.print("Enter your choice: ");
            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    System.out.println("\nMain Window --> Add a new contact Window: (Enter the following information)");
                    System.out.println("=============================================================================");
                    System.out.print("Name: ");
                    String name = sc.nextLine();
                    System.out.print("Email: ");
                    String email = sc.nextLine();
                    System.out.print("Phone: ");
                    String phone = sc.nextLine();
                    System.out.print("Notes: ");
                    String notes = sc.nextLine();
                    addContact(name, email, phone, notes);
                    sc.nextLine();
                    break;

                case 2:
                    System.out.println("\nMain Window --> Search for Contact Window:");
                    System.out.println("===========================================");
                    System.out.println("(1) Search by Name\n(2) Search by Email\n(3) Search by Phone\nEnter your choice: ");
                    int searchChoice = sc.nextInt();
                    sc.nextLine();  // Consume newline character

                    switch (searchChoice) {
                        case 1:
                            System.out.println("Main Window --> Search for Contact Window --> Search by Name");
                            System.out.println("=============================================================");
                            System.out.print("(1) Enter Name:   ");
                            String nameSearch = sc.nextLine();
                            searchByName(nameSearch, sc);
                            break;

                        case 2:
                            System.out.println("Main Window --> Search for Contact Window --> Search by Email");
                            System.out.println("=============================================================");
                            System.out.print("(2) Enter Email:   ");
                            String emailSearch = sc.nextLine();
                            searchByEmail(emailSearch, sc);
                            break;

                        case 3:
                            System.out.println("Main Window --> Search for Contact Window --> Search by Phone");
                            System.out.println("=============================================================");
                            System.out.print("(3) Enter phone:   ");
                            String phoneSearch = sc.nextLine();
                            searchByPhone(phoneSearch, sc);
                            break;

                        default:
                            System.out.println("Invalid choice.");
                            break;
                    }
                    break;

                case 3:
                    System.out.println("\nMain Window --> Display All Contacts");
                    System.out.println("=====================================");
                    displayAllContacts();
                    sc.nextLine();
                    break;

                case 4:
                    exit = true;
                    System.out.println("Have a nice day ahead. Bye...");
                    break;

                default:
                    System.out.println("Invalid input! Please try again.");
                    break;
            }
        }
        sc.close();
    }

    public static void addContact(String name, String email, String phone, String note) {
        if (contactCount < 100) {
            names[contactCount] = name;
            emails[contactCount] = email;
            phones[contactCount] = phone;
            notes[contactCount] = note;
            contactCount++;
            System.out.println("-----------------------------------------------------------------------------");
            System.out.println("Saved successfully... Press Enter to go back to the Main Window");
        } else {
            System.out.println("Address book is full.");
        }
    }

    public static void displayAllContacts() {
        if (contactCount == 0) {
            System.out.println("No contacts available.");
        } else {
            headerPrint();
            for (int i = 0; i < contactCount; i++) {
                System.out.printf("%-3d | %-20s | %-25s | %-20s | %-20s\n", i + 1, names[i], emails[i], phones[i], notes[i]);
            }
        }
        System.out.println("Press Enter to go back to the Main Window");
    }

    public static void searchByName(String name, Scanner sc) {
        boolean found = false;
        headerPrint();
        for (int i = 0; i < contactCount; i++) {
            if (names[i].toLowerCase().contains(name.toLowerCase())) {
                System.out.printf("%-3d | %-20s | %-25s | %-20s | %-20s\n", i + 1, names[i], emails[i], phones[i], notes[i]);
                found = true;
            }
        }
        if (!found) {
            System.out.println("No contact found.");
        } else {
            sc.nextLine();
            deleteOption(sc);
        }
    }

    public static void searchByEmail(String email, Scanner sc) {
        boolean found = false;
        headerPrint();
        for (int i = 0; i < contactCount; i++) {
            if (emails[i].toLowerCase().contains(email.toLowerCase())) {
                System.out.printf("%-3d | %-20s | %-25s | %-20s | %-20s\n", i + 1, names[i], emails[i], phones[i], notes[i]);
                found = true;
            }
        }
        if (!found) {
            System.out.println("No contact found.");
        } else {
            sc.nextLine();
            deleteOption(sc);
        }
    }

    public static void searchByPhone(String phone, Scanner sc) {
        boolean found = false;
        headerPrint();
        for (int i = 0; i < contactCount; i++) {
            if (phones[i].contains(phone)) {
                System.out.printf("%-3d | %-20s | %-25s | %-20s | %-20s\n", i + 1, names[i], emails[i], phones[i], notes[i]);
                found = true;
            }
        }
        if (!found) {
            System.out.println("No contact found.");
        } else {
            sc.nextLine();
            deleteOption(sc);
        }
    }

    public static void deleteContact(int id) {
        if (id <= 0 || id > contactCount) {
            System.out.println("Invalid ID.");
        } else {
            for (int i = id - 1; i < contactCount - 1; i++) {
                names[i] = names[i + 1];
                emails[i] = emails[i + 1];
                phones[i] = phones[i + 1];
                notes[i] = notes[i + 1];
            }
            contactCount--;
            System.out.println("Deleted... Press Enter to go back to the Main Window");
        }
    }

    public static void deleteOption(Scanner sc) {
        System.out.println("\nChoose one of these options:\n(1) To delete a contact\n(2) Back to main Window\nEnter your choice: ");
        int deleteChoice = sc.nextInt();
        sc.nextLine();
        switch (deleteChoice) {
            case 1:
                System.out.print("(1) Enter the Contact ID: ");
                int id = sc.nextInt();
                sc.nextLine();
                deleteContact(id);
                break;
            case 2:
                return;
            default:
                System.out.println("Invalid choice. Returning to main menu.");
        }
    }

    public static void headerPrint() {
        System.out.println("-----------------------------------------------------------------------------------------");
        System.out.printf("%-3s | %-20s | %-25s | %-20s | %-20s\n", "ID", "Name", "Email", "Phone", "Notes");
        System.out.println("-----------------------------------------------------------------------------------------");
    }
}
