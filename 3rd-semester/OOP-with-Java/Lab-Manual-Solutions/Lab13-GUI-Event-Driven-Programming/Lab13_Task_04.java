// Lab Task 4: Make a functional nonscientific calculator. Recall the last task of the previous lab.

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

// Simple Calculator
public class Lab13_Task_04 {

  private static double firstOperand = 0;
  private static String operator = "";
  private static boolean startNewInput = false;

  public static void main(String[] args) {
    createCalculatorGUI();
  }

  public static void createCalculatorGUI() {
    JFrame frame = new JFrame("Simple Calculator");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(300, 400);
    frame.setLayout(new BorderLayout());

    JTextField display = new JTextField();
    display.setEditable(false);
    display.setFont(new Font("Arial", Font.PLAIN, 24));
    frame.add(display, BorderLayout.NORTH);

    JPanel panel = new JPanel();
    panel.setLayout(new GridLayout(4, 4, 5, 5));

    String[] buttons = {
      "7", "8", "9", "/",
      "4", "5", "6", "*",
      "1", "2", "3", "-",
      "0", ".", "=", "+"
    };

    for (String text : buttons) {
      JButton button = new JButton(text);
      button.setFont(new Font("Arial", Font.BOLD, 18));
      panel.add(button);

      button.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          String btnText = button.getText();

          if (btnText.matches("[0-9\\.]")) {
            if (startNewInput) {
              display.setText("");
              startNewInput = false;
            }
            display.setText(display.getText() + btnText);
          } else if (btnText.matches("[\\+\\-\\*/]")) {
            try {
              firstOperand = Double.parseDouble(display.getText());
              operator = btnText;
              startNewInput = true;
            } catch (NumberFormatException ex) {
              display.setText("Error");
            }
          } else if (btnText.equals("=")) {
            try {
              double secondOperand = Double.parseDouble(display.getText());
              double result = performOperation(firstOperand, secondOperand, operator);
              display.setText(String.valueOf(result));
              startNewInput = true;
            } catch (Exception ex) {
              display.setText("Error");
            }
          }
        }
      });
    }

    frame.add(panel, BorderLayout.CENTER);
    frame.setVisible(true);
  }

  private static double performOperation(double a, double b, String op) {
    switch (op) {
      case "+": return a + b;
      case "-": return a - b;
      case "*": return a * b;
      case "/": return b != 0 ? a / b : 0; // Avoid divide-by-zero crash
      default: throw new IllegalArgumentException("Invalid operator");
    }
  }
}

