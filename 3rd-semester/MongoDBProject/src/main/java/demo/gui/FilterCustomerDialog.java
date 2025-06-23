package demo.gui;

import demo.dao.CustomerDAO;
import demo.models.Customer;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.List;

public class FilterCustomerDialog extends JDialog {
    private JComboBox<String> fieldComboBox;
    private JTextField valueField;
    private JButton filterButton;
    private JTable table;
    private DefaultTableModel model;

    public FilterCustomerDialog(JFrame parent) {
        super(parent, "Filter Customers", true);
        setLayout(new BorderLayout());
        setSize(800, 400);
        setLocationRelativeTo(parent);

        // Top Panel for Filters
        JPanel topPanel = new JPanel(new FlowLayout());

        fieldComboBox = new JComboBox<>(new String[]{"Name", "Email", "CNIC", "Phone", "Address"});
        valueField = new JTextField(15);
        filterButton = new JButton("Filter");

        topPanel.add(new JLabel("Filter By:"));
        topPanel.add(fieldComboBox);
        topPanel.add(valueField);
        topPanel.add(filterButton);

        add(topPanel, BorderLayout.NORTH);

        // Table with full customer fields
        model = new DefaultTableModel(new String[]{
            "Customer ID", "Name", "Email", "CNIC", "Phone", "Address"
        }, 0);
        table = new JTable(model);
        add(new JScrollPane(table), BorderLayout.CENTER);

        // Button Logic
        filterButton.addActionListener((ActionEvent e) -> {
            String selectedField = ((String) fieldComboBox.getSelectedItem()).toLowerCase();
            String value = valueField.getText().trim();

            if (value.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter a value to filter.", "Warning", JOptionPane.WARNING_MESSAGE);
                return;
            }

            CustomerDAO dao = new CustomerDAO();
            List<Customer> results = dao.filterCustomers(selectedField, value);

            model.setRowCount(0); // clear table
            for (Customer c : results) {
                model.addRow(new Object[]{
                    c.getCustomerid(),
                    c.getName(),
                    c.getEmail(),
                    c.getCnic(),
                    c.getPhone(),
                    c.getAddress()
                });
            }
        });

        setVisible(true);
    }
}
