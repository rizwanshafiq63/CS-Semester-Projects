// AccountFormDialog.java
package demo.gui;

import demo.dao.AccountDAO;
import demo.models.Account;

import javax.swing.*;
import java.awt.*;

public class AccountFormDialog extends JDialog {
    public AccountFormDialog(JFrame parent) {
        super(parent, "Add Account", true);
        setSize(400, 400);
        setLocationRelativeTo(parent);
        setLayout(new GridLayout(7, 2, 10, 10));

        JTextField customerIdField = new JTextField();
        JTextField typeField = new JTextField();
        JTextField balanceField = new JTextField();
        JTextField openDateField = new JTextField();
        JTextField statusField = new JTextField();

        JButton addButton = new JButton("Add Account");

        add(new JLabel("Customer ID:")); add(customerIdField);
        add(new JLabel("Type:")); add(typeField);
        add(new JLabel("Balance:")); add(balanceField);
        add(new JLabel("Open Date (yyyy-mm-dd):")); add(openDateField);
        add(new JLabel("Status:")); add(statusField);
        add(new JLabel()); add(addButton);

        addButton.addActionListener(e -> {
            int cid = Integer.parseInt(customerIdField.getText().trim());
            String type = typeField.getText().trim();
            double balance = Double.parseDouble(balanceField.getText().trim());
            String date = openDateField.getText().trim();
            String status = statusField.getText().trim();

            Account account = new Account(0, cid, type, balance, date, status);
            new AccountDAO().insertAccount(account);
            JOptionPane.showMessageDialog(this, "Account added successfully!");
            dispose();
        });
    }
}