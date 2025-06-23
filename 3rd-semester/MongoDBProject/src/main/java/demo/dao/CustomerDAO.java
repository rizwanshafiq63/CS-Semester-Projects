package demo.dao;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;

import static com.mongodb.client.model.Filters.eq;

import demo.MongoConnector;
import demo.models.Customer;

public class CustomerDAO {
    private MongoCollection<Document> collection;

    public CustomerDAO() {
        MongoDatabase db = MongoConnector.getDatabase();
        this.collection = db.getCollection("customers");
    }

    public void insertCustomer(Customer customer) {
        int nextId = getNextCustomerId();
        customer.setCustomerid(nextId);
        Document doc = new Document("customerid", customer.getCustomerid())
                .append("name", customer.getName())
                .append("cnic", customer.getCnic())
                .append("email", customer.getEmail())
                .append("phone", customer.getPhone())
                .append("address", customer.getAddress());
        collection.insertOne(doc);
    }

    public int getNextCustomerId() {
    Document lastCustomer = collection.find()
        .sort(new Document("customerid", -1)) // sort descending by customerid
        .limit(1)
        .first();

        if (lastCustomer != null && lastCustomer.containsKey("customerid")) {
            return lastCustomer.getInteger("customerid") + 1;
        } else {
            return 1; // start from 1 if no customer exists
        }
    }


    public List<Customer> getAllCustomers() {
        List<Customer> customers = new ArrayList<>();
        for (Document doc : collection.find()) {
            customers.add(docToCustomer(doc));
        }
        return customers;
    }

    public void updateCustomer(Customer customer) {
        Bson filter = eq("customerid", customer.getCustomerid());
        Document update = new Document("$set", new Document()
                .append("name", customer.getName())
                .append("cnic", customer.getCnic())
                .append("email", customer.getEmail())
                .append("phone", customer.getPhone())
                .append("address", customer.getAddress()));
        collection.updateOne(filter, update);
    }

    public List<Customer> filterCustomers(String field, String value) {
    List<Customer> list = new ArrayList<>();
    MongoDatabase db = MongoConnector.getDatabase();
    MongoCollection<Document> collection = db.getCollection("customers");

    Bson filter = Filters.regex(field, Pattern.compile(Pattern.quote(value), Pattern.CASE_INSENSITIVE));

    for (Document doc : collection.find(filter)) {
        Customer c = new Customer(
            doc.getInteger("customerid"),
            doc.getString("name"),
            doc.getString("cnic"),
            doc.getString("email"),
            doc.getString("phone"),
            doc.getString("address")
        );
        list.add(c);
    }
    return list;
}

public Customer deleteCustomerById(int id) {
    Document query = new Document("customerid", id);
    Document deletedDoc = collection.find(query).first();

    if (deletedDoc != null) {
        collection.deleteOne(query);
        return new Customer(
            deletedDoc.getInteger("customerid"),
            deletedDoc.getString("name"),
            deletedDoc.getString("cnic"),
            deletedDoc.getString("email"),
            deletedDoc.getString("phone"),
            deletedDoc.getString("address")
        );
    }
    return null;
}


    private Customer docToCustomer(Document doc) {
        return new Customer(
            doc.getInteger("customerid"),
            doc.getString("name"),
            doc.getString("cnic"),
            doc.getString("email"),
            doc.getString("phone"),
            doc.getString("address")
        );
    }
}
