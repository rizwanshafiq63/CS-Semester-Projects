// FilterTransactionDialog.java
package demo.gui;

import java.awt.BorderLayout;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;

import demo.dao.TransactionDAO;
import demo.models.Transaction;

public class FilterTransactionDialog extends JDialog {
    public FilterTransactionDialog(JFrame parent) {
        super(parent, "Filter Transactions", true);
        setSize(700, 400);
        setLocationRelativeTo(parent);

        JPanel topPanel = new JPanel();
        JComboBox<String> criteriaBox = new JComboBox<>(new String[]{"Type", "Channel"});
        JTextField valueField = new JTextField(15);
        JButton filterButton = new JButton("Filter");

        topPanel.add(new JLabel("Filter by:"));
        topPanel.add(criteriaBox);
        topPanel.add(valueField);
        topPanel.add(filterButton);

        DefaultTableModel model = new DefaultTableModel(new String[]{
            "ID", "Account ID", "Type", "Amount", "Datetime", "Channel", "Receiver"
        }, 0);
        JTable table = new JTable(model);

        filterButton.addActionListener(e -> {
            String field = (String) criteriaBox.getSelectedItem();
            String value = valueField.getText().trim();
            List<Transaction> list = new TransactionDAO().filterByField(field, value);
            model.setRowCount(0);
            for (Transaction t : list) {
                model.addRow(new Object[]{
                    t.getTransactionid(), t.getAccountid(), t.getType(), t.getAmount(),
                    t.getDatetime(), t.getChannel(),
                    t.getReceiverAccount() != null ? t.getReceiverAccount() : "-"
                });
            }
        });

        add(topPanel, BorderLayout.NORTH);
        add(new JScrollPane(table), BorderLayout.CENTER);

        setVisible(true);
    }
}
