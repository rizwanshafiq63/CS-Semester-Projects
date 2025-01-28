import java.util.Scanner;

public class StringEncrypter {
    public static String encryptString(String input, byte key) {
        // String encrypted = ""; // Start with an empty string
        // Using StringBuilder is efficient because it lets us add characters to the string without creating a new string each time (which happens if you use +=).
        StringBuilder encrypted = new StringBuilder();
            for (int i = 0; i < input.length(); i++) {
                char currentChar = input.charAt(i);
                if (currentChar != ' ')
                    // encrypted += (char) (currentChar ^ key);
                    encrypted.append((char) (currentChar ^ key)); // XOR and append
                else
                    // encrypted += currentChar;
                    encrypted.append(currentChar); // Append space without encryption
            }
            //return encrypted;
            return encrypted.toString();
        }
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter the Message you want to Encrypt or Decrypt: ");
        String message = input.nextLine();
        // String message = "Hello World";
        byte key = 5; // Example key for encryption
    
        String encrypted = encryptString(message, key);
        System.out.println("Encrypted Message: " + encrypted);
    
        // Decrypting the message by applying the same method again
        String decrypted = encryptString(encrypted, key);
        System.out.println("Decrypted Message: " + decrypted);
        input.close();
    }
    
}
