import java.awt.*;
import javax.swing.*;

public class Lab12_Task_05 {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Scroll Bars Demo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(530, 370);
        frame.setLayout(null);

        // Set a darker background like the image
        JPanel contentPanel = new JPanel();
        contentPanel.setLayout(null);
        contentPanel.setBackground(new Color(80, 80, 80));
        frame.setContentPane(contentPanel);

        // Create the text area
        JTextArea textArea = new JTextArea("Some people can write and write and write and write and write and write some more");
        textArea.setLineWrap(true);
        textArea.setWrapStyleWord(true);

        // Add to scroll pane with always visible scrollbars
        JScrollPane scrollPane = new JScrollPane(textArea,
                JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
                JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
        scrollPane.setBounds(60, 30, 400, 180);
        contentPanel.add(scrollPane);

        // Create and add buttons
        String[] buttonLabels = {"Save Memo 1", "Save Memo 2", "Clear", "Get Memo 1", "Get Memo 2"};
        int x = 30;
        for (String label : buttonLabels) {
            JButton button = new JButton(label);
            button.setBounds(x, 230, 90, 30);
            button.setFocusPainted(false);
            button.setFont(new Font("SansSerif", Font.PLAIN, 11));
            contentPanel.add(button);
            x += 95;  // Add spacing between buttons
        }

        frame.setResizable(false);
        frame.setVisible(true);
    }
}
