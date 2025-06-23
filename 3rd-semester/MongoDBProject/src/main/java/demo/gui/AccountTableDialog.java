// AccountTableDialog.java
package demo.gui;

import java.util.List;

import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;

import demo.dao.AccountDAO;
import demo.models.Account;

public class AccountTableDialog extends JDialog {
    public AccountTableDialog(JFrame parent) {
        super(parent, "All Accounts", true);
        setSize(700, 400);
        setLocationRelativeTo(parent);

        DefaultTableModel model = new DefaultTableModel(
            new String[]{"Account ID", "Customer ID", "Type", "Balance", "Open Date", "Status"}, 0);
        JTable table = new JTable(model);

        List<Account> accounts = new AccountDAO().getAllAccounts();
        for (Account acc : accounts) {
            model.addRow(new Object[]{
                acc.getAccountId(), acc.getCustomerId(), acc.getType(),
                acc.getBalance(), acc.getOpenDate(), acc.getStatus()
            });
        }

        add(new JScrollPane(table));
    }
}