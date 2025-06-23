package demo.gui;

import demo.dao.CustomerDAO;
import demo.models.Customer;

import javax.swing.*;
import java.awt.*;

public class DeleteCustomerDialog extends JDialog {

    public DeleteCustomerDialog(JFrame parent) {
        super(parent, "Delete Customer", true);
        setLayout(new FlowLayout());
        setSize(400, 200);
        setLocationRelativeTo(parent);

        JLabel label = new JLabel("Enter Customer ID to Delete:");
        JTextField idField = new JTextField(10);
        JButton deleteBtn = new JButton("Delete");

        add(label);
        add(idField);
        add(deleteBtn);

        deleteBtn.addActionListener(e -> {
            String idText = idField.getText().trim();
            if (idText.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter a customer ID.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            int id;
            try {
                id = Integer.parseInt(idText);
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Invalid ID format.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            int confirm = JOptionPane.showConfirmDialog(this, "Are you sure you want to delete customer ID " + id + "?", "Confirm Deletion", JOptionPane.YES_NO_OPTION);
            if (confirm == JOptionPane.YES_OPTION) {
                CustomerDAO dao = new CustomerDAO();
                Customer deleted = dao.deleteCustomerById(id);
                if (deleted != null) {
                    JOptionPane.showMessageDialog(this,
                            "Customer deleted:\n\n" +
                            "ID: " + deleted.getCustomerid() + "\n" +
                            "Name: " + deleted.getName() + "\n" +
                            "Email: " + deleted.getEmail() + "\n" +
                            "CNIC: " + deleted.getCnic() + "\n" +
                            "Phone: " + deleted.getPhone() + "\n" +
                            "Address: " + deleted.getAddress(),
                            "Deleted Successfully",
                            JOptionPane.INFORMATION_MESSAGE);
                    dispose();
                } else {
                    JOptionPane.showMessageDialog(this, "No customer found with ID " + id, "Not Found", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        setVisible(true);
    }
}
