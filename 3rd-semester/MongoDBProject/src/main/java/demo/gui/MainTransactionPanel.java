package demo.gui;

import java.awt.Dimension;
import java.awt.FlowLayout;

import javax.swing.JButton;
import javax.swing.JFrame;

public class MainTransactionPanel extends JFrame {
    public MainTransactionPanel() {
        setTitle("Transaction Manager");
        setSize(600, 350); // Slightly wider for 6 buttons
        setLayout(new FlowLayout(FlowLayout.CENTER, 20, 30));
        setLocationRelativeTo(null);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE); // So it doesn’t close app

        JButton addButton = new JButton("Add Transaction");
        JButton viewButton = new JButton("View Transactions");
        JButton filterButton = new JButton("Filter Transactions");
        JButton deleteButton = new JButton("Delete Transaction");
        JButton summaryButton = new JButton("Transaction Summary");

        // Customize look
        JButton[] buttons = { addButton, viewButton, filterButton, deleteButton, summaryButton };
        for (JButton btn : buttons) {
            btn.setPreferredSize(new Dimension(200, 40));
            btn.setFocusable(false);
            add(btn);
        }

        // Actions
        addButton.addActionListener(e -> new AddTransactionDialog(this));
        viewButton.addActionListener(e -> new ViewTransactionsDialog(this));
        filterButton.addActionListener(e -> new FilterTransactionDialog(this));
        deleteButton.addActionListener(e -> new DeleteTransactionDialog(this));
        summaryButton.addActionListener(e -> new TransactionSummaryDialog(this));
    }
}
