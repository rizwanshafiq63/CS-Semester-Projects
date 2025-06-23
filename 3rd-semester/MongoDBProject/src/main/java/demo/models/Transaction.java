package demo.models;

import java.util.Date;

import org.bson.Document;

public class Transaction {
    private int transactionid;
    private int accountid;
    private String type;
    private double amount;
    private Date datetime;
    private String channel;
    private Integer receiver_account;

    public Transaction() {
    }

    public Transaction(int transactionid, int accountid, String type, double amount,
                       Date datetime, String channel, Integer receiver_account) {
        this.transactionid = transactionid;
        this.accountid = accountid;
        this.type = type;
        this.amount = amount;
        this.datetime = datetime;
        this.channel = channel;
        this.receiver_account = receiver_account;
    }

    // Convert to MongoDB Document
    public Document toDocument() {
        Document doc = new Document("transactionid", transactionid)
                .append("accountid", accountid)
                .append("type", type)
                .append("amount", amount)
                .append("datetime", datetime)
                .append("channel", channel);

        if (receiver_account != null) {
            doc.append("receiver_account", receiver_account);
        }

        return doc;
    }

    // Convert from MongoDB Document (Safe casting for amount)
    public static Transaction fromDocument(Document doc) {
        Transaction t = new Transaction();
        t.setTransactionid(doc.getInteger("transactionid"));
        t.setAccountid(doc.getInteger("accountid"));
        t.setType(doc.getString("type"));

        Object amt = doc.get("amount");
        if (amt instanceof Integer) {
            t.setAmount(((Integer) amt).doubleValue());
        } else if (amt instanceof Double) {
            t.setAmount((Double) amt);
        }

        t.setDatetime(doc.getDate("datetime")); // Store/retrieve as Date
        t.setChannel(doc.getString("channel"));

        if (doc.containsKey("receiver_account")) {
            t.setReceiver_account(doc.getInteger("receiver_account"));
        }

        return t;
    }

    // Getters and Setters
    public int getTransactionid() {
        return transactionid;
    }

    public void setTransactionid(int transactionid) {
        this.transactionid = transactionid;
    }

    public int getAccountid() {
        return accountid;
    }

    public void setAccountid(int accountid) {
        this.accountid = accountid;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public Date getDatetime() {
        return datetime;
    }

    public void setDatetime(Date datetime) {
        this.datetime = datetime;
    }

    public String getChannel() {
        return channel;
    }

    public void setChannel(String channel) {
        this.channel = channel;
    }

    public Integer getReceiverAccount() {
        return receiver_account;
    }

    public void setReceiver_account(Integer receiver_account) {
        this.receiver_account = receiver_account;
    }
}
