import java.util.Scanner;

public class Vigenere {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String dic = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "; // Valid characters
        boolean continueProgram = true;

        while (continueProgram) {
            System.out.println("Welcome to Vigenère Cipher Encryptor and Decryptor!");
            System.out.println("Press 1 for Encryption\nPress 2 for Decryption\nPress 3 to Exit\nSelect: ");
            int choice = sc.nextInt();
            sc.nextLine();
            System.out.println();

            switch (choice) {
                case 1:
                    String textToEncrypt = isValidInput("Enter the text to encrypt: ", dic, sc);
                    String encryptionKey = isValidInput("Enter the encryption key: ", dic, sc);

                    String encryptedText = encrypt(textToEncrypt, encryptionKey, dic);
                    System.out.println("Encrypted text: " + encryptedText);
                    break;

                case 2:
                    String textToDecrypt = isValidInput("Enter the text to decrypt: ", dic, sc);
                    String decryptionKey = isValidInput("Enter the decryption key: ", dic, sc);

                    String decryptedText = decrypt(textToDecrypt, decryptionKey, dic);
                    System.out.println("Decrypted text: " + decryptedText);
                    break;

                case 3:
                    continueProgram = false;
                    break;

                default:
                    System.out.println("Invalid choice! Please try again.");
            }
        }
        sc.close();
        System.out.println("Thank you for using Vigenère Cipher. Goodbye!");
    }

    public static String encrypt(String text, String key, String dic) {
        StringBuilder encryptedText = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            int textIndex = dic.indexOf(text.charAt(i));
            int keyIndex = dic.indexOf(key.charAt(i % key.length())); 
            int encryptedIndex = (textIndex + keyIndex) % dic.length(); 
            encryptedText.append(dic.charAt(encryptedIndex));
        }
        return encryptedText.toString();
    }

    public static String decrypt(String text, String key, String dic) {
        StringBuilder decryptedText = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            int textIndex = dic.indexOf(text.charAt(i));
            int keyIndex = dic.indexOf(key.charAt(i % key.length())); 
            int decryptedIndex = (textIndex - keyIndex + dic.length()) % dic.length(); 
            decryptedText.append(dic.charAt(decryptedIndex));
        }
        return decryptedText.toString().toLowerCase(); 
    }

    public static String isValidInput(String prompt, String dic, Scanner sc) {
        String input;
        while (true) {
            System.out.print(prompt);
            input = sc.nextLine().toUpperCase();
            if (isValidCharacter(input, dic)) {
                return input;
            } else {
                System.out.println("Invalid input! Only valid characters (A-Z, 0-9, and space) are allowed. Please try again.");
            }
        }
    }

    public static boolean isValidCharacter(String input, String dic) {
        for (int i = 0; i < input.length(); i++) {
            if (dic.indexOf(input.charAt(i)) == -1) {
                return false;
            }
        }
        return true;
    }    
}
