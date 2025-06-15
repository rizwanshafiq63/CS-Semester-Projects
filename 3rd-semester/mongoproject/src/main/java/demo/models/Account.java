package demo.models;

public class Account {
    private int accountid;
    private int customerid;
    private String type;
    private double balance;
    private String opendate;
    private String status;

    public Account(int accountid, int customerid, String type, double balance, String opendate, String status) {
        this.accountid = accountid;
        this.customerid = customerid;
        this.type = type;
        this.balance = balance;
        this.opendate = opendate;
        this.status = status;
    }

    // Getters
    public int getAccountId() {
        return accountid;
    }

    public int getCustomerId() {
        return customerid;
    }

    public String getType() {
        return type;
    }

    public double getBalance() {
        return balance;
    }

    public String getOpenDate() {
        return opendate;
    }

    public String getStatus() {
        return status;
    }

    // Setters
    public void setAccountid(int accountid) {
        this.accountid = accountid;
    }

    public void setCustomerid(int customerid) {
        this.customerid = customerid;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public void setOpendate(String opendate) {
        this.opendate = opendate;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    // toString
    @Override
    public String toString() {
        return "Account ID: " + accountid +
                ", Customer ID: " + customerid +
                ", Type: " + type +
                ", Balance: " + balance +
                ", Open Date: " + opendate +
                ", Status: " + status;
    }
}
