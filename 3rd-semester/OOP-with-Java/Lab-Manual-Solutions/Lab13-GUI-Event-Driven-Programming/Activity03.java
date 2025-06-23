/* Run and understand the below code. We now first see which button triggered the event through the getSource event and then either disapper one button or copy text in the TextField into the label. */

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class Activity03 extends JFrame {
  private JTextField tf1;
  private JLabel label;
  private JButton b;
  private JButton b1;

  public Activity03() {
    this.setLayout(new FlowLayout(FlowLayout.LEFT, 10, 20));
    tf1 = new JTextField(8);
    this.add(tf1);
    label = new JLabel("New Text");
    this.add(label);
    b = new JButton("Change");
    b.addActionListener(new myHandler());
    add(b);
    b1 = new JButton("Disappear");
    b1.addActionListener(new myHandler());
    add(b1);
  }

  class myHandler implements ActionListener {
    public void actionPerformed(ActionEvent e) {
      if (e.getSource() == b) {
        String s = tf1.getText();
        label.setText(s);
        tf1.setText("");
      }
      if (e.getSource() == b1) {
        b.setVisible(false);
      }
    }
  }

  public static void main(String[] args) {
    Activity03 f = new Activity03();
    f.setTitle("Copy Text");
    f.setSize(400, 150);
    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    f.setLocationRelativeTo(null);;
    f.setVisible(true);
  }
}


