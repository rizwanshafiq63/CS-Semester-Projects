package demo.gui;

import demo.dao.CustomerDAO;
import demo.models.Customer;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

public class UpdateCustomerDialog extends JDialog {
    private JTextField idField;
    private JTextField nameField;
    private JTextField emailField;
    private JTextField cnicField;
    private JButton updateButton;

    public UpdateCustomerDialog(JFrame parent) {
        super(parent, "Update Customer", true);
        setLayout(new GridLayout(5, 2, 10, 10));
        setSize(400, 300);
        setLocationRelativeTo(parent);

        idField = new JTextField();
        nameField = new JTextField();
        emailField = new JTextField();
        cnicField = new JTextField();
        updateButton = new JButton("Update");

        add(new JLabel("Customer ID:"));
        add(idField);
        add(new JLabel("Name:"));
        add(nameField);
        add(new JLabel("Email:"));
        add(emailField);
        add(new JLabel("CNIC:"));
        add(cnicField);
        add(new JLabel());
        add(updateButton);

        updateButton.addActionListener((ActionEvent e) -> {
            try {
                int id = Integer.parseInt(idField.getText().trim());
                String name = nameField.getText().trim();
                String email = emailField.getText().trim();
                String cnic = cnicField.getText().trim();

                if (name.isEmpty() || email.isEmpty() || cnic.isEmpty()) {
                    JOptionPane.showMessageDialog(this, "All fields are required.", "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                Customer updatedCustomer = new Customer(id, name, cnic, email, "", "");
                CustomerDAO dao = new CustomerDAO();
                dao.updateCustomer(updatedCustomer);
                JOptionPane.showMessageDialog(this, "Customer updated successfully.");
                dispose();
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Invalid ID", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        setVisible(true);
    }
}