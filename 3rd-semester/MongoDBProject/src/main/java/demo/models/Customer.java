package demo.models;

public class Customer {
    private int customerid;
    private String name;
    private String cnic;
    private String email;
    private String phone;
    private String address;

    public Customer(int customerid, String name, String cnic, String email, String phone, String address) {
        this.customerid = customerid;
        this.name = name;
        this.cnic = cnic;
        this.email = email;
        this.phone = phone;
        this.address = address;
    }

    // Getters & setters
    public int getCustomerid() { return customerid; }
    public String getName() { return name; }
    public String getCnic() { return cnic; }
    public String getEmail() { return email; }
    public String getPhone() { return phone; }
    public String getAddress() { return address; }

    public void setCustomerid(int customerid) { this.customerid = customerid; }
    public void setName(String name) { this.name = name; }
    public void setCnic(String cnic) { this.cnic = cnic; }
    public void setEmail(String email) { this.email = email; }
    public void setPhone(String phone) { this.phone = phone; }
    public void setAddress(String address) { this.address = address; }
}
