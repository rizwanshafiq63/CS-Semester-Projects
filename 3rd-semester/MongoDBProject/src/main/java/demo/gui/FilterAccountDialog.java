// FilterAccountDialog.java
package demo.gui;

import demo.dao.AccountDAO;
import demo.models.Account;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.util.List;

public class FilterAccountDialog extends JDialog {
    public FilterAccountDialog(JFrame parent) {
        super(parent, "Filter Accounts", true);
        setSize(700, 400);
        setLocationRelativeTo(parent);
        setLayout(new BorderLayout());

        JPanel filterPanel = new JPanel();
        String[] fields = {"type", "status"};
        JComboBox<String> fieldBox = new JComboBox<>(fields);
        JTextField valueField = new JTextField(15);
        JButton filterBtn = new JButton("Filter");
        filterPanel.add(new JLabel("Filter by:"));
        filterPanel.add(fieldBox);
        filterPanel.add(valueField);
        filterPanel.add(filterBtn);
        add(filterPanel, BorderLayout.NORTH);

        DefaultTableModel model = new DefaultTableModel(
            new String[]{"Account ID", "Customer ID", "Type", "Balance", "Open Date", "Status"}, 0);
        JTable table = new JTable(model);
        add(new JScrollPane(table), BorderLayout.CENTER);

        filterBtn.addActionListener(e -> {
            String field = (String) fieldBox.getSelectedItem();
            String value = valueField.getText().trim();
            List<Account> results = new AccountDAO().filterAccounts(field, value);
            model.setRowCount(0);
            for (Account acc : results) {
                model.addRow(new Object[]{
                    acc.getAccountId(), acc.getCustomerId(), acc.getType(),
                    acc.getBalance(), acc.getOpenDate(), acc.getStatus()
                });
            }
        });
    }
}
