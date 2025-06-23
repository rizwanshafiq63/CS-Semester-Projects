import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

// used Script Engine in this one

public class FunctionalCalculator {

  public static void main(String[] args) {
    createCalculatorGUI();
  }

  public static void createCalculatorGUI() {
    // Create frame
    JFrame frame = new JFrame("Calculator");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(300, 400);
    frame.setLayout(new BorderLayout());

    // Create display field
    JTextField display = new JTextField();
    display.setEditable(false);
    display.setFont(new Font("Arial", Font.PLAIN, 20));
    frame.add(display, BorderLayout.NORTH);

    // Create panel with grid layout for buttons
    JPanel panel = new JPanel();
    panel.setLayout(new GridLayout(4, 4, 5, 5));

    // Button labels
    String[] buttons = {
      "7", "8", "9", "/",
      "4", "5", "6", "*",
      "1", "2", "3", "-",
      "0", ".", "=", "+"
    };

    // Create and add buttons
    for (String text : buttons) {
      JButton button = new JButton(text);
      button.setFont(new Font("Arial", Font.BOLD, 18));
      panel.add(button);

      // Add action listeners
      button.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          String currentText = display.getText();
          String btnText = button.getText();

          if (btnText.equals("=")) {
            try {
              double result = eval(currentText);
              display.setText(String.valueOf(result));
            } catch (Exception ex) {
              display.setText("Error");
            }
          } else {
            display.setText(currentText + btnText);
          }
        }
      });
    }

    frame.add(panel, BorderLayout.CENTER);
    frame.setVisible(true);
  }

  // Basic expression evaluator (very simple)
  public static double eval(String expr) {
    ScriptEngineManager mgr = new ScriptEngineManager();
    ScriptEngine engine = mgr.getEngineByName("JavaScript");
    try {
      return Double.parseDouble(engine.eval(expr).toString());
    } catch (Exception e) {
      throw new RuntimeException("Invalid Expression");
    }
  }
}


