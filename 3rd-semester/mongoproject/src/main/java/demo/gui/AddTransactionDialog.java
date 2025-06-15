// AddTransactionDialog.java
package demo.gui;

import demo.dao.TransactionDAO;
import demo.models.Transaction;

import javax.swing.*;
import java.awt.*;
import java.util.Date;

public class AddTransactionDialog extends JDialog {
    public AddTransactionDialog(JFrame parent) {
        super(parent, "Add Transaction", true);
        setSize(400, 400);
        setLocationRelativeTo(parent);
        setLayout(new GridLayout(8, 2, 10, 10));

        JTextField accountIdField = new JTextField();
        JComboBox<String> typeDropdown = new JComboBox<>(new String[]{"Deposit", "Withdrawal", "Transfer"});
        JTextField amountField = new JTextField();
        JTextField channelField = new JTextField();
        JTextField receiverAccountField = new JTextField();
        receiverAccountField.setEnabled(false); // disabled by default

        JButton addButton = new JButton("Add Transaction");

        add(new JLabel("Account ID:")); add(accountIdField);
        add(new JLabel("Type:")); add(typeDropdown);
        add(new JLabel("Amount:")); add(amountField);
        add(new JLabel("Channel:")); add(channelField);
        add(new JLabel("Receiver Account (for Transfer only):")); add(receiverAccountField);
        add(new JLabel()); add(addButton);

        // Enable/disable receiver field based on type selection
        typeDropdown.addActionListener(e -> {
            String selected = (String) typeDropdown.getSelectedItem();
            receiverAccountField.setEnabled("Transfer".equalsIgnoreCase(selected));
        });

        addButton.addActionListener(e -> {
            try {
                int aid = Integer.parseInt(accountIdField.getText().trim());
                String type = (String) typeDropdown.getSelectedItem();
                double amount = Double.parseDouble(amountField.getText().trim());
                String channel = channelField.getText().trim();
                String receiverText = receiverAccountField.getText().trim();
                Integer receiver = receiverText.isEmpty() ? null : Integer.parseInt(receiverText);

                Transaction t = new Transaction();
                t.setAccountid(aid);
                t.setType(type);
                t.setAmount(amount);
                t.setChannel(channel);
                t.setDatetime(new Date());

                if ("Transfer".equalsIgnoreCase(type)) {
                    t.setReceiver_account(receiver);
                }

                boolean success = new TransactionDAO().addTransaction(t);
                String result = success ? "Transaction successful!" : "Transaction failed!";
                JOptionPane.showMessageDialog(this, result);
                if (success) dispose();

            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Invalid input: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        setVisible(true);
    }
}
