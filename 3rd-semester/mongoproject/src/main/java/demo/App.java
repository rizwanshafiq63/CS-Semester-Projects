package demo;

import java.awt.Font;

import javax.swing.SwingUtilities;
import javax.swing.UIManager;

import com.formdev.flatlaf.FlatIntelliJLaf;

public class App {
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(new FlatIntelliJLaf()); // Modern theme
            UIManager.put("defaultFont", new Font("Segoe UI", Font.PLAIN, 14)); // Optional: unified font
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("Launching myABL Smart Banking Dashboard...");

        SwingUtilities.invokeLater(() -> new demo.gui.MainDashboard().setVisible(true));
    }
}
