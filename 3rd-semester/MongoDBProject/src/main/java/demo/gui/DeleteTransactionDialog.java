// DeleteTransactionDialog.java
package demo.gui;

import java.awt.GridLayout;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;

import demo.dao.TransactionDAO;
import demo.models.Transaction;

public class DeleteTransactionDialog extends JDialog {
    public DeleteTransactionDialog(JFrame parent) {
        super(parent, "Delete Transaction", true);
        setSize(400, 200);
        setLocationRelativeTo(parent);
        setLayout(new GridLayout(3, 2, 10, 10));

        JTextField transactionIdField = new JTextField();
        JButton deleteButton = new JButton("Delete");

        add(new JLabel("Transaction ID:"));
        add(transactionIdField);
        add(new JLabel());
        add(deleteButton);

        deleteButton.addActionListener(e -> {
            int tid = Integer.parseInt(transactionIdField.getText().trim());
            Transaction t = new TransactionDAO().deleteTransaction(tid);
            if (t != null) {
                JOptionPane.showMessageDialog(this,
                        """
                        Deleted Transaction:
                        ID: """ + t.getTransactionid() +
                        ", Type: " + t.getType() +
                        ", Amount: " + t.getAmount());
                dispose();
            } else {
                JOptionPane.showMessageDialog(this, "Transaction not found.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        setVisible(true);
    }
}
