import java.awt.BorderLayout;
import java.awt.FlowLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class Lab12_Task_04 {
    public static void main(String[] args) {
        // Create main frame
        JFrame frame = new JFrame("Panel Demo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(500, 300);

        // Create a panel for buttons
        JPanel panel = new JPanel();
        panel.setLayout(new FlowLayout()); // Align buttons in a row

        // Add buttons to the panel
        for (int i = 1; i <= 5; i++) {
            panel.add(new JButton("Button " + i));
        }

        // Add panel to the SOUTH of the frame
        frame.add(panel, BorderLayout.SOUTH);

        // Set frame visible
        frame.setVisible(true);
    }
}
