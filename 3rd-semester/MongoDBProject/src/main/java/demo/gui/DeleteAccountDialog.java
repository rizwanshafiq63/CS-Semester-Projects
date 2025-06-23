// DeleteAccountDialog.java
package demo.gui;

import demo.dao.AccountDAO;
import demo.models.Account;

import javax.swing.*;
import java.awt.*;

public class DeleteAccountDialog extends JDialog {
    public DeleteAccountDialog(JFrame parent) {
        super(parent, "Delete Account", true);
        setSize(400, 200);
        setLocationRelativeTo(parent);
        setLayout(new GridLayout(3, 2, 10, 10));

        JTextField accountIdField = new JTextField();
        JButton deleteButton = new JButton("Delete Account");

        add(new JLabel("Enter Account ID:"));
        add(accountIdField);
        add(new JLabel());
        add(deleteButton);

        deleteButton.addActionListener(e -> {
            int aid = Integer.parseInt(accountIdField.getText().trim());
            Account deleted = new AccountDAO().deleteAccountById(aid);
            if (deleted != null) {
                JOptionPane.showMessageDialog(this, "Deleted:\n" + deleted.toString());
            } else {
                JOptionPane.showMessageDialog(this, "Account not found.", "Error", JOptionPane.ERROR_MESSAGE);
            }
            dispose();
        });
    }
}