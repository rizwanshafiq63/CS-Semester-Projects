// Lab Task 3: Font Style Changer using JCheckBox

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

// Check Box Font Changer
public class Lab13_Task_03 extends JFrame implements ItemListener {
  private JTextField textField;
  private JCheckBox boldBox, italicBox;

  public Lab13_Task_03() {
    setTitle("JCheckBox Test");
    setSize(400, 120);
    setDefaultCloseOperation(EXIT_ON_CLOSE);
    setLayout(new FlowLayout());

    textField = new JTextField("Watch the font style change", 25);
    textField.setFont(new Font("Serif", Font.PLAIN, 18));
    add(textField);

    boldBox = new JCheckBox("Bold");
    italicBox = new JCheckBox("Italic");

    boldBox.addItemListener(this);
    italicBox.addItemListener(this);

    add(boldBox);
    add(italicBox);

    setVisible(true);
  }

  public void itemStateChanged(ItemEvent e) {
    int style = Font.PLAIN;
    if (boldBox.isSelected()) style += Font.BOLD;
    if (italicBox.isSelected()) style += Font.ITALIC;
    textField.setFont(new Font("Serif", style, 18));
  }

  public static void main(String[] args) {
    new Lab13_Task_03();
  }
}

