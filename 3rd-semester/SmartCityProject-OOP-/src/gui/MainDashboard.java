// gui/MainDashboard.java
package gui;

import javax.swing.*;
import java.awt.*;

public class MainDashboard extends JFrame {

  public MainDashboard() {
    setTitle("Smart City Resource Management System");
    setSize(1000, 700);
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setLocationRelativeTo(null); // center screen

    // Main tabbed pane
    JTabbedPane tabs = new JTabbedPane();

    // Add tabs
    tabs.addTab("Admin Panel", new AdminPanel());
    tabs.addTab("Public View", new PublicPanel());

    add(tabs);
    setVisible(true);
  }

  public static void main(String[] args) {
    SwingUtilities.invokeLater(MainDashboard::new);
  }
}

