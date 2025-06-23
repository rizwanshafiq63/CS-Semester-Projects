package demo.dao;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Updates;

import demo.MongoConnector;
import demo.models.Account;

public class AccountDAO {
    private final MongoCollection<Document> collection;

    public AccountDAO() {
        MongoDatabase db = MongoConnector.getDatabase();
        this.collection = db.getCollection("accounts");
    }

    public void insertAccount(Account account) {
        Document doc = new Document("accountid", account.getAccountId())
                .append("customerid", account.getCustomerId())
                .append("type", account.getType())
                .append("balance", account.getBalance())
                .append("opendate", account.getOpenDate())
                .append("status", account.getStatus());

        collection.insertOne(doc);
    }

    public List<Account> getAllAccounts() {
        List<Account> list = new ArrayList<>();
        for (Document doc : collection.find()) {
            list.add(documentToAccount(doc));
        }
        list.sort(Comparator.comparingInt(Account::getAccountId));
        return list;
    }

    public Account getAccountById(int accountId) {
        Document doc = collection.find(Filters.eq("accountid", accountId)).first();
        return doc != null ? documentToAccount(doc) : null;
    }

    public boolean updateAccount(Account account) {
        Bson filter = Filters.eq("accountid", account.getAccountId());
        Bson update = Updates.combine(
                Updates.set("customerid", account.getCustomerId()),
                Updates.set("type", account.getType()),
                Updates.set("balance", account.getBalance()),
                Updates.set("opendate", account.getOpenDate()),
                Updates.set("status", account.getStatus())
        );
        return collection.updateOne(filter, update).getModifiedCount() > 0;
    }

    public Account deleteAccountById(int accountId) {
        Document deleted = collection.findOneAndDelete(Filters.eq("accountid", accountId));
        return deleted != null ? documentToAccount(deleted) : null;
    }

    public List<Account> filterAccounts(String field, String value) {
        List<Account> list = new ArrayList<>();
        Bson filter = Filters.eq(field, value);
        for (Document doc : collection.find(filter)) {
            list.add(documentToAccount(doc));
        }
        list.sort(Comparator.comparingInt(Account::getAccountId));
        return list;
    }

    public int getNextAccountId() {
        Document doc = collection.find().sort(new Document("accountid", -1)).limit(1).first();
        return doc != null ? doc.getInteger("accountid") + 1 : 101;
    }

    public boolean updateAccountBalance(int accountId, double newBalance) {
    return collection.updateOne(
            Filters.eq("accountid", accountId),
            Updates.set("balance", newBalance)
    ).getModifiedCount() > 0;
}


    private Account documentToAccount(Document doc) {
    int accountid = doc.getInteger("accountid");
    int customerid = doc.getInteger("customerid");
    String type = doc.getString("type");

    // Fix for balance type casting (Double or Integer)
    double balance = 0.0;
    Object balanceObj = doc.get("balance");
    if (balanceObj instanceof Number number) {
        balance = number.doubleValue(); // safe casting
    }
    // if (balanceObj instanceof Number) {
    //     balance = ((Number) balanceObj).doubleValue(); // safe casting
    // }

    String opendate = doc.getString("opendate");
    String status = doc.getString("status");

    return new Account(accountid, customerid, type, balance, opendate, status);
}

}
