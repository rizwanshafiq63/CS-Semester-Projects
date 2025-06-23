import javax.swing.*;
import java.awt.*;

public class Lab12_Task_02 {

  public static void main(String[] args) {
    createPanelDemoGUI();
  }

  public static void createPanelDemoGUI() {
    // Create frame
    JFrame frame = new JFrame("Panel Demonstration");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(400, 400);
    frame.setLayout(new BorderLayout());

    // Create colored panel section (center)
    JPanel colorPanel = new JPanel();
    colorPanel.setLayout(new GridLayout(1, 3));

    JPanel cyanPanel = new JPanel();
    cyanPanel.setBackground(Color.CYAN);

    JPanel whitePanel = new JPanel();
    whitePanel.setBackground(Color.WHITE);

    JPanel grayPanel = new JPanel();
    grayPanel.setBackground(Color.GRAY);

    colorPanel.add(cyanPanel);
    colorPanel.add(whitePanel);
    colorPanel.add(grayPanel);

    // Create button panel (south)
    JPanel buttonPanel = new JPanel();
    buttonPanel.setLayout(new FlowLayout());

    JButton btnCyan = new JButton("Cyan");
    JButton btnWhite = new JButton("White");
    JButton btnGray = new JButton("Gray");

    buttonPanel.add(btnCyan);
    buttonPanel.add(btnWhite);
    buttonPanel.add(btnGray);

    // Add panels to frame
    frame.add(colorPanel, BorderLayout.CENTER);
    frame.add(buttonPanel, BorderLayout.SOUTH);

    // Make frame visible
    frame.setVisible(true);
  }
}

