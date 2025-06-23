// Main.java
import gui.MainDashboard;
import javax.swing.SwingUtilities;

public class Main {
  public static void main(String[] args) {

    // Launch GUI
    SwingUtilities.invokeLater(() -> new MainDashboard());
  }
}

