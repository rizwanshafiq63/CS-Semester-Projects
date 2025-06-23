import java.awt.GridLayout;
import javax.swing.JButton;
import javax.swing.JFrame;

public class Lab12_Task_03 {
    public static void main(String[] args) {
        // Create the main frame
        JFrame frame = new JFrame("GridLayout Demo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(300, 200);  // Set frame size (adjust as needed)

        // Set GridLayout with 2 rows and 3 columns
        frame.setLayout(new GridLayout(2, 3, 10, 10)); // gaps between buttons

        // Create and add buttons
        frame.add(new JButton("one"));
        frame.add(new JButton("two"));
        frame.add(new JButton("three"));
        frame.add(new JButton("four"));
        frame.add(new JButton("five"));
        frame.add(new JButton("six"));

        // Make the frame visible
        frame.setVisible(true);
    }
}
