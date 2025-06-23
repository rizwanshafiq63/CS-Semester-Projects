package demo.gui;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;

import javax.swing.JButton;
import javax.swing.JFrame;

public class MainCustomerPanel extends JFrame {

    public MainCustomerPanel() {
        setTitle("Customer Management");
        setSize(600, 350);
        setLayout(new FlowLayout(FlowLayout.CENTER, 20, 40));
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);
        getContentPane().setBackground(new Color(245, 245, 245)); // light theme background

        Font buttonFont = new Font("Segoe UI", Font.PLAIN, 16);

        JButton addButton = new JButton("Add Customer");
        JButton viewButton = new JButton("View Customers");
        JButton updateButton = new JButton("Update Customer");
        JButton deleteButton = new JButton("Delete Customer");
        JButton filterButton = new JButton("Filter Customer");

        //Style buttons
        JButton[] buttons = {addButton, viewButton, updateButton, deleteButton, filterButton};
        for (JButton btn : buttons) {
            btn.setPreferredSize(new Dimension(200, 50));
            btn.setFont(buttonFont);
            btn.setFocusPainted(false);
        }

        add(addButton);
        add(viewButton);
        add(updateButton);
        add(deleteButton);
        add(filterButton);

        addButton.addActionListener(e -> new CustomerFormDialog(this).setVisible(true));
        viewButton.addActionListener(e -> new CustomerTableDialog(this).setVisible(true));
        updateButton.addActionListener(e -> new UpdateCustomerDialog(this));
        deleteButton.addActionListener(e -> new DeleteCustomerDialog(this));
        filterButton.addActionListener(e -> new FilterCustomerDialog(this));
    }
}