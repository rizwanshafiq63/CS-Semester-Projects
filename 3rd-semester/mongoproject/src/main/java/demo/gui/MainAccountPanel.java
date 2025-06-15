package demo.gui;

import java.awt.Dimension;
import java.awt.FlowLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;

public class MainAccountPanel extends JFrame {

    public MainAccountPanel() {
        setTitle("Account Management");
        setSize(600, 350);
        setLayout(new FlowLayout(FlowLayout.CENTER, 20, 30));
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);

        JButton addButton = new JButton("Add Account");
        JButton viewButton = new JButton("View Accounts");
        JButton updateButton = new JButton("Update Account");
        JButton deleteButton = new JButton("Delete Account");
        JButton filterButton = new JButton("Filter Account");

        Dimension btnSize = new Dimension(180, 40);
        addButton.setPreferredSize(btnSize);
        viewButton.setPreferredSize(btnSize);
        updateButton.setPreferredSize(btnSize);
        deleteButton.setPreferredSize(btnSize);
        filterButton.setPreferredSize(btnSize);

        add(addButton);
        add(viewButton);
        add(updateButton);
        add(deleteButton);
        add(filterButton);

        addButton.addActionListener(e -> new AccountFormDialog(this).setVisible(true));
        viewButton.addActionListener(e -> new AccountTableDialog(this).setVisible(true));
        updateButton.addActionListener(e -> new UpdateAccountDialog(this).setVisible(true));
        deleteButton.addActionListener(e -> new DeleteAccountDialog(this).setVisible(true));
        filterButton.addActionListener(e -> new FilterAccountDialog(this).setVisible(true));
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new MainAccountPanel().setVisible(true));
    }
}
