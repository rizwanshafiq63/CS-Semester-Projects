/* Run and understand the below code. Basically this code sets the text in label on button press event. Any text entered in the textfield is copied into the label. Ensure that it is so and understand how it works. */

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class Activity02 extends JFrame {
  private JTextField tf1;
  private JLabel label;
  private JButton b;

  public Activity02() {
    this.setLayout(new FlowLayout(FlowLayout.LEFT, 10, 20));
    tf1 = new JTextField(8);
    this.add(tf1);
    label = new JLabel("New Text");
    this.add(label);
    b = new JButton("Change");
    b.addActionListener(new myHandler());
    add(b);
  }

  class myHandler implements ActionListener {
    public void actionPerformed(ActionEvent e) {
      String s = tf1.getText();
      label.setText(s);
      tf1.setText("");
    }
  }

  public static void main(String[] args) {
    Activity02 f = new Activity02();
    f.setTitle("Copy Text");
    f.setSize(400, 150);
    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    f.setLocationRelativeTo(null);;
    f.setVisible(true);
  }
}


