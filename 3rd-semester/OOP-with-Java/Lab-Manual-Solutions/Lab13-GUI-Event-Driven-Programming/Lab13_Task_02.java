// Lab Task 2: Font Style Changer using JRadioButton

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

// Radio Button Font Changer
public class Lab13_Task_02 extends JFrame implements ActionListener {
  private JTextField textField;
  private JRadioButton plainBtn, boldBtn, italicBtn, boldItalicBtn;
  private ButtonGroup group;

  public Lab13_Task_02() {
    setTitle("RadioButton Test");
    setSize(400, 120);
    setDefaultCloseOperation(EXIT_ON_CLOSE);
    setLayout(new FlowLayout());

    textField = new JTextField("Watch the font style change", 25);
    add(textField);

    plainBtn = new JRadioButton("Plain", true);
    boldBtn = new JRadioButton("Bold");
    italicBtn = new JRadioButton("Italic");
    boldItalicBtn = new JRadioButton("Bold/Italic");

    group = new ButtonGroup();
    group.add(plainBtn);
    group.add(boldBtn);
    group.add(italicBtn);
    group.add(boldItalicBtn);

    add(plainBtn); add(boldBtn); add(italicBtn); add(boldItalicBtn);

    plainBtn.addActionListener(this);
    boldBtn.addActionListener(this);
    italicBtn.addActionListener(this);
    boldItalicBtn.addActionListener(this);

    setVisible(true);
  }

  public void actionPerformed(ActionEvent e) {
    int style = Font.PLAIN;
    if (boldBtn.isSelected()) style = Font.BOLD;
    else if (italicBtn.isSelected()) style = Font.ITALIC;
    else if (boldItalicBtn.isSelected()) style = Font.BOLD + Font.ITALIC;
    textField.setFont(new Font("Serif", style, 18));
  }

  public static void main(String[] args) {
    new Lab13_Task_02();
  }
}

