package demo.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridLayout;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

import demo.dao.AccountDAO;
import demo.dao.CustomerDAO;
import demo.dao.TransactionDAO;
import demo.models.Transaction;

public class MainDashboard extends JFrame {

    private JPanel statsPanel;
    private JLabel lastUpdatedLabel;

    public MainDashboard() {
        setTitle("myABL Smart Banking System - Dashboard");
        setSize(1000, 600);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout(10, 10));

        // Stats Panel (card style)
        statsPanel = new JPanel(new GridLayout(2, 4, 15, 15));
        statsPanel.setBorder(BorderFactory.createTitledBorder("📊 Real-Time Statistics"));
        statsPanel.setBackground(new Color(30, 30, 30));

        add(statsPanel, BorderLayout.NORTH);

        // Navigation Panel
        JPanel navPanel = new JPanel(new GridLayout(5, 1, 15, 15));
        navPanel.setBorder(BorderFactory.createTitledBorder("🧭 Navigation"));

        JButton customerBtn = new JButton("Manage Customers");
        JButton accountBtn = new JButton("Manage Accounts");
        JButton transactionsBtn = new JButton("Manage Transactions");
        JButton exitBtn = new JButton("Exit Application");

        JButton[] navButtons = { customerBtn, accountBtn, transactionsBtn, exitBtn };
        for (JButton btn : navButtons) {
            btn.setFocusable(false);
            navPanel.add(btn);
        }

        add(navPanel, BorderLayout.CENTER);

        customerBtn.addActionListener(e -> new MainCustomerPanel().setVisible(true));
        accountBtn.addActionListener(e -> new MainAccountPanel().setVisible(true));
        transactionsBtn.addActionListener(e -> new MainTransactionPanel().setVisible(true));
        exitBtn.addActionListener(e -> System.exit(0));

        // Footer - last update
        lastUpdatedLabel = new JLabel("Last Updated: --", SwingConstants.CENTER);
        lastUpdatedLabel.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        add(lastUpdatedLabel, BorderLayout.SOUTH);

        updateStats(); // Load initially

        // Refresh every 10 sec
        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            public void run() {
                updateStats();
            }
        }, 0, 10000);

        setVisible(true);
        this.requestFocusInWindow();
    }

    private JPanel createStatCard(String title, String emoji, String value, Color bgColor) {
        JPanel card = new JPanel(new BorderLayout());
        card.setBackground(bgColor);
        card.setBorder(BorderFactory.createTitledBorder(title));

        JLabel iconLabel = new JLabel(emoji, SwingConstants.CENTER);
        iconLabel.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 30));
        JLabel valueLabel = new JLabel(value, SwingConstants.CENTER);
        valueLabel.setFont(new Font("Segoe UI", Font.BOLD, 20));
        valueLabel.setForeground(Color.WHITE);

        card.add(iconLabel, BorderLayout.NORTH);
        card.add(valueLabel, BorderLayout.CENTER);

        return card;
    }

    private void updateStats() {
        CustomerDAO customerDAO = new CustomerDAO();
        AccountDAO accountDAO = new AccountDAO();
        TransactionDAO transactionDAO = new TransactionDAO();

        int totalCustomers = customerDAO.getAllCustomers().size();
        int totalAccounts = accountDAO.getAllAccounts().size();
        double totalBalance = accountDAO.getAllAccounts().stream()
                .mapToDouble(acc -> acc.getBalance()).sum();
        long activeAccounts = accountDAO.getAllAccounts().stream()
                .filter(acc -> acc.getStatus().equalsIgnoreCase("Active")).count();

        List<Transaction> transactions = transactionDAO.getAllTransactions();
        int totalTransactions = transactions.size();
        double avgBalance = totalAccounts > 0 ? totalBalance / totalAccounts : 0.0;
        double lastTxnAmount = transactions.isEmpty() ? 0.0 :
                transactions.get(transactions.size() - 1).getAmount();

        // Remove all and rebuild cards
        statsPanel.removeAll();

        statsPanel.add(createStatCard("👥 Customers", "👥", String.valueOf(totalCustomers), new Color(59, 130, 246)));
        statsPanel.add(createStatCard("💼 Accounts", "💼", String.valueOf(totalAccounts), new Color(34, 197, 94)));
        statsPanel.add(createStatCard("💰 Total Balance", "💰", "Rs. " + String.format("%.2f", totalBalance), new Color(234, 179, 8)));
        statsPanel.add(createStatCard("✅ Active Accounts", "✅", String.valueOf(activeAccounts), new Color(239, 68, 68)));
        statsPanel.add(createStatCard("🔁 Transactions", "🔁", String.valueOf(totalTransactions), new Color(132, 204, 22)));
        statsPanel.add(createStatCard("📊 Avg. Balance", "📊", "Rs. " + String.format("%.2f", avgBalance), new Color(16, 185, 129)));
        statsPanel.add(createStatCard("💸 Last Txn Amount", "💸", "Rs. " + String.format("%.2f", lastTxnAmount), new Color(250, 204, 21)));

        // Revalidate & repaint UI
        statsPanel.revalidate();
        statsPanel.repaint();

        lastUpdatedLabel.setText("🕒 Last Updated: " + new java.util.Date().toString());
    }

    public static void main(String[] args) {
        // Optional: FlatLaf setup if you want dark mode
        // FlatDarkLaf.setup();
        SwingUtilities.invokeLater(MainDashboard::new);
    }
}
