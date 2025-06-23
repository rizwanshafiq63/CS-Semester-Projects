// Lab Task 1: Create a frame with one label, one textbox and a button. Display the information entered in textbox on button click.

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Lab13_Task_01 {

  public static void main(String[] args) {
    createTextDisplayGUI();
  }

  public static void createTextDisplayGUI() {
    // Create the frame
    JFrame frame = new JFrame("Text Display");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(350, 200);
    frame.setLayout(new FlowLayout());

    // Create label, text field, and button
    JLabel label = new JLabel("Enter something:");
    JTextField textField = new JTextField(20);
    JButton button = new JButton("Display");

    // ActionListener to display input
    button.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {
        String input = textField.getText();
        JOptionPane.showMessageDialog(frame, "You entered: " + input);
      }
    });

    // Add components to the frame
    frame.add(label);
    frame.add(textField);
    frame.add(button);

    // Make frame visible
    frame.setVisible(true);
  }
}


