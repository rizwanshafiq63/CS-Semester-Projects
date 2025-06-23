package demo.gui;

import java.awt.GridLayout;
import java.util.Map;

import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;

import demo.dao.TransactionDAO;

public class TransactionSummaryDialog extends JDialog {
    public TransactionSummaryDialog(JFrame parent) {
        super(parent, "Transaction Summary", true);
        setSize(400, 300);
        setLocationRelativeTo(parent);
        setLayout(new GridLayout(0, 2, 10, 10));

        JLabel typeLabel = new JLabel("Type");
        JLabel totalLabel = new JLabel("Total Amount");
        add(typeLabel); add(totalLabel);

        Map<String, Double> summary = new TransactionDAO().getSummary();
        for (Map.Entry<String, Double> entry : summary.entrySet()) {
            add(new JLabel(entry.getKey()));
            add(new JLabel(String.valueOf(entry.getValue())));
        }

        setVisible(true);
    }
}
