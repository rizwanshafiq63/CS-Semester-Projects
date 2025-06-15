// UpdateAccountDialog.java
package demo.gui;

import java.awt.GridLayout;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;

import demo.dao.AccountDAO;
import demo.models.Account;

public class UpdateAccountDialog extends JDialog {

    private JTextField accountIdField;
    private JTextField customerIdField;
    private JTextField typeField;
    private JTextField balanceField;
    private JTextField openDateField;
    private JTextField statusField;

    public UpdateAccountDialog(JFrame parent) {
        super(parent, "Update Account", true);
        setSize(500, 400);
        setLocationRelativeTo(parent);
        setLayout(new GridLayout(7, 2, 10, 10));

        accountIdField = new JTextField();
        customerIdField = new JTextField();
        typeField = new JTextField();
        balanceField = new JTextField();
        openDateField = new JTextField();
        statusField = new JTextField();

        JButton updateButton = new JButton("Update Account");

        add(new JLabel("Account ID:")); add(accountIdField);
        add(new JLabel("Customer ID:")); add(customerIdField);
        add(new JLabel("Type:")); add(typeField);
        add(new JLabel("Balance:")); add(balanceField);
        add(new JLabel("Open Date (yyyy-MM-dd):")); add(openDateField);
        add(new JLabel("Status:")); add(statusField);
        add(new JLabel()); add(updateButton);

        updateButton.addActionListener(e -> {
            try {
                int aid = Integer.parseInt(accountIdField.getText().trim());
                int cid = Integer.parseInt(customerIdField.getText().trim());
                String type = typeField.getText().trim();
                double balance = Double.parseDouble(balanceField.getText().trim());
                String openDate = openDateField.getText().trim();
                String status = statusField.getText().trim();

                Account updatedAccount = new Account(aid, cid, type, balance, openDate, status);

                boolean success = new AccountDAO().updateAccount(updatedAccount);
                if (success) {
                    JOptionPane.showMessageDialog(this, "Account updated successfully!");
                    dispose();
                } else {
                    JOptionPane.showMessageDialog(this, "Update failed. No matching account found.", "Error", JOptionPane.ERROR_MESSAGE);
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Please enter valid numeric values for Account ID, Customer ID, and Balance.", "Input Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        setVisible(true);
    }
}
