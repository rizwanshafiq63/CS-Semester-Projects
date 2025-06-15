package demo.gui;

import demo.dao.CustomerDAO;
import demo.models.Customer;

import javax.swing.*;
import java.awt.*;

public class CustomerFormDialog extends JDialog {
    public CustomerFormDialog(JFrame parent) {
        super(parent, "Add Customer", true);
        setSize(350, 300);
        setLayout(new GridBagLayout());
        setLocationRelativeTo(parent);

        JTextField nameField = new JTextField(20);
        JTextField emailField = new JTextField(20);
        JTextField cnicField = new JTextField(20);
        JTextField phoneField = new JTextField(20);
        JTextField addressField = new JTextField(20);
        JButton submit = new JButton("Submit");

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        String[] labels = {"Name", "Email", "CNIC", "Phone", "Address"};
        JTextField[] fields = {nameField, emailField, cnicField, phoneField, addressField};

        for (int i = 0; i < labels.length; i++) {
            gbc.gridx = 0; gbc.gridy = i;
            add(new JLabel(labels[i] + ":"), gbc);
            gbc.gridx = 1;
            add(fields[i], gbc);
        }

        gbc.gridx = 1; gbc.gridy = labels.length;
        add(submit, gbc);

        submit.addActionListener(e -> {
            CustomerDAO dao = new CustomerDAO();
            Customer c = new Customer(
                (int) (System.currentTimeMillis() % 100000),
                nameField.getText(),
                cnicField.getText(),
                emailField.getText(),
                phoneField.getText(),
                addressField.getText()
            );
            dao.insertCustomer(c);
            JOptionPane.showMessageDialog(this, "Customer Added!");
            dispose();
        });
    }
}