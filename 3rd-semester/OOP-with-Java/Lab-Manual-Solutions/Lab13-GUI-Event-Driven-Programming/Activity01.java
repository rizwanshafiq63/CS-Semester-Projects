/* Run the below code. It should create a label and a button. The label should have text “Hello” but when the button the pressed the text changes to “Bye” */

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class Activity01 extends JFrame {
  private JLabel label;
  private JButton b;

  public Activity01() {
    this.setLayout(new FlowLayout(FlowLayout.LEFT, 10, 20));
    label = new JLabel("Hello");
    this.add(label);
    b = new JButton("Toggle");
    b.addActionListener(new myHandler());
    add(b);
  }

  class myHandler implements ActionListener {
    public void actionPerformed(ActionEvent e) {
      label.setText("Bye");
    }
  }

  public static void main(String[] args) {
    Activity01 f = new Activity01();
    f.setTitle("Hi and Bye");
    f.setSize(400, 150);
    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    f.setLocationRelativeTo(null);
    f.setVisible(true);
  }
}

