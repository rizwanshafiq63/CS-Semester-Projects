import javax.swing.*;
import java.awt.*;

// Calculator GUI
public class Lab12_Task_01 {
  public static void main(String[] args) {
    // Create the frame
    JFrame frame = new JFrame("Calculator");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(300, 400);
    frame.setLayout(new BorderLayout());

    // Create the display field
    JTextField display = new JTextField();
    display.setEditable(false);
    frame.add(display, BorderLayout.NORTH);

    // Create panel for buttons using GridLayout
    JPanel panel = new JPanel();
    panel.setLayout(new GridLayout(4, 4, 5, 5)); // 4 rows x 4 columns with spacing

    // Add buttons to the panel
    String[] buttons = {
      "7", "8", "9", "/",
      "4", "5", "6", "*",
      "1", "2", "3", "-",
      "0", ".", "=", "+"
    };

    for (String text : buttons) {
      panel.add(new JButton(text));
    }

    frame.add(panel, BorderLayout.CENTER);

    // Make it visible
    frame.setVisible(true);
  }
}

