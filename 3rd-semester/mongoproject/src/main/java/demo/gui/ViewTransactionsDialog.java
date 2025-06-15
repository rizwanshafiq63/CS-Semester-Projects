package demo.gui;

import java.awt.BorderLayout;
import java.util.List;

import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;

import demo.dao.TransactionDAO;
import demo.models.Transaction;

public class ViewTransactionsDialog extends JDialog {
    public ViewTransactionsDialog(JFrame parent) {
        super(parent, "All Transactions", true);
        setSize(700, 400);
        setLocationRelativeTo(parent);

        String[] cols = {"ID", "Account ID", "Type", "Amount", "Date", "Channel", "Receiver"};
        DefaultTableModel model = new DefaultTableModel(cols, 0);
        JTable table = new JTable(model);

        List<Transaction> transactions = new TransactionDAO().getAllTransactions();
        for (Transaction t : transactions) {
            model.addRow(new Object[]{
                t.getTransactionid(), t.getAccountid(), t.getType(), t.getAmount(),
                t.getDatetime(), t.getChannel(),
                t.getReceiverAccount() != null ? t.getReceiverAccount() : "-"
            });
        }

        add(new JScrollPane(table), BorderLayout.CENTER);
        setVisible(true);
    }
}
