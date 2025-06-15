package demo.gui;

import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import demo.MongoConnector;
import org.bson.Document;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class CustomerTableDialog extends JDialog {

    public CustomerTableDialog(JFrame parent) {
        super(parent, "All Customers", true);
        setSize(800, 400);
        setLocationRelativeTo(parent);

        String[] columns = {"Customer ID", "Name", "CNIC", "Email", "Phone", "Address"};
        DefaultTableModel model = new DefaultTableModel(columns, 0);
        JTable table = new JTable(model);
        table.setFillsViewportHeight(true);

        MongoCollection<Document> col = MongoConnector.getDatabase().getCollection("customers");
        FindIterable<Document> docs = col.find();

        for (Document doc : docs) {
            model.addRow(new Object[]{
                doc.get("customerid"),
                doc.get("name"),
                doc.get("cnic"),
                doc.get("email"),
                doc.get("phone"),
                doc.get("address")
            });
        }

        JScrollPane scroll = new JScrollPane(table);
        add(scroll, BorderLayout.CENTER);
    }
}