// TransactionDAO.java (MongoDB Version)
package demo.dao;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.bson.Document;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.model.Filters;

import demo.MongoConnector;
import demo.models.Transaction;

public class TransactionDAO {
    private final MongoCollection<Document> transactionCollection = MongoConnector.getDatabase().getCollection("transactions");
    private final AccountDAO accountDAO = new AccountDAO();

    public List<Transaction> getAllTransactions() {
        List<Transaction> transactions = new ArrayList<>();
        try (MongoCursor<Document> cursor = transactionCollection.find().iterator()) {
            while (cursor.hasNext()) {
                transactions.add(Transaction.fromDocument(cursor.next()));
            }
        }
        return transactions;
    }

    public boolean addTransaction(Transaction t) {
        if (t.getAmount() < 0) return false;

        double senderBalance = accountDAO.getAccountById(t.getAccountid()).getBalance();
        double receiverBalance = 0;

        if (t.getType().equalsIgnoreCase("Transfer") && t.getReceiverAccount() != null) {
            receiverBalance = accountDAO.getAccountById(t.getReceiverAccount()).getBalance();
        }

        switch (t.getType()) {
            case "Deposit":
                senderBalance += t.getAmount();
                break;
            case "Withdrawal":
                if (senderBalance < t.getAmount()) return false;
                senderBalance -= t.getAmount();
                break;
            case "Transfer":
                if (senderBalance < t.getAmount()) return false;
                senderBalance -= t.getAmount();
                receiverBalance += t.getAmount();
                break;
        }

        // Update balances in MongoDB
        if (!accountDAO.updateAccountBalance(t.getAccountid(), senderBalance)) return false;
        if (t.getType().equals("Transfer") && t.getReceiverAccount() != null) {
            if (!accountDAO.updateAccountBalance(t.getReceiverAccount(), receiverBalance)) return false;
        }

        // Generate next transaction id
        t.setTransactionid(getNextTransactionId());

        // Insert transaction into MongoDB
        try {
            transactionCollection.insertOne(t.toDocument());
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean updateTransaction(Transaction updated) {
        try {
            Document filter = new Document("transactionid", updated.getTransactionid());
            Document newDoc = updated.toDocument();
            return transactionCollection.replaceOne(filter, newDoc).getModifiedCount() > 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public Transaction deleteTransaction(int tid) {
    Document doc = transactionCollection.findOneAndDelete(Filters.eq("transactionid", tid));
    return doc != null ? Transaction.fromDocument(doc) : null;
}

    public List<Transaction> filterByField(String field, String value) {
        return getAllTransactions().stream()
                .filter(t -> {
                    switch (field) {
                        case "Type": return t.getType().equalsIgnoreCase(value);
                        case "Channel": return t.getChannel().equalsIgnoreCase(value);
                        case "Account ID": return String.valueOf(t.getAccountid()).equals(value);
                        default: return false;
                    }
                })
                .collect(Collectors.toList());
    }

    public Map<String, Double> getSummary() {
    Map<String, Double> summary = new HashMap<>();
    summary.put("Deposit", 0.0);
    summary.put("Withdrawal", 0.0);
    summary.put("Transfer", 0.0);

    for (Transaction t : getAllTransactions()) {
        String type = t.getType();
        if (summary.containsKey(type)) {
            summary.put(type, summary.get(type) + t.getAmount());
        }
    }

    return summary;
}

    private int getNextTransactionId() {
        List<Transaction> all = getAllTransactions();
        return all.stream().mapToInt(Transaction::getTransactionid).max().orElse(200) + 1;
    }
}
