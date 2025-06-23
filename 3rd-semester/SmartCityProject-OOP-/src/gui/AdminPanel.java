// gui/AdminPanel.java
package gui;

import java.awt.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import models.*;
import repository.CityRepository;
import utils.CityManager;
import utils.Metrics;
import utils.ResourceIDGenerator;

public class AdminPanel extends JPanel {

  private JComboBox<String> resourceTypeField;
  private JTextField locationField;
  private JComboBox<String> statusField;
  private JTextField extraInfoField;
  private CityRepository<CityResource> repository = new CityRepository<>();
  private StatusMapPanel statusMapPanel = new StatusMapPanel();
  private DefaultTableModel tableModel;
  private JTable table;

  public AdminPanel() {
    PublicPanel.setRepository(repository);
    setLayout(new BorderLayout());

    // ==== CRUD Panel ====
    JPanel crudPanel = new JPanel(new GridLayout(4, 2, 10, 10));
    crudPanel.setBorder(BorderFactory.createTitledBorder("Create/Update Resource"));

    resourceTypeField = new JComboBox<>(new String[]{"TransportUnit", "PowerStation", "EmergencyService"});
    locationField = new JTextField();
    statusField = new JComboBox<>(new String[]{"Active", "Offline", "Maintenance"});
    extraInfoField = new JTextField();

    crudPanel.add(new JLabel("Resource Type:"));
    crudPanel.add(resourceTypeField);

    crudPanel.add(new JLabel("Location:"));
    crudPanel.add(locationField);

    crudPanel.add(new JLabel("Status:"));
    crudPanel.add(statusField);

    crudPanel.add(new JLabel("Additional Info:"));
    crudPanel.add(extraInfoField);

    JButton saveBtn = new JButton("Add");
    JButton deleteBtn = new JButton("Delete");
    JButton filterBtn = new JButton("Status Filter");
    JButton updateBtn = new JButton("Update Status");
    JButton saveToFileBtn = new JButton("Save to File");
    JButton loadFromFileBtn = new JButton("Load from File");

    JPanel buttonPanel = new JPanel(new GridLayout(1, 6, 10, 0)); // Single row, 5 columns

    buttonPanel.add(saveBtn);
    buttonPanel.add(deleteBtn);
    buttonPanel.add(filterBtn);
    buttonPanel.add(updateBtn);
    buttonPanel.add(saveToFileBtn);
    buttonPanel.add(loadFromFileBtn);

    JPanel topPanel = new JPanel(new BorderLayout());
    topPanel.add(crudPanel, BorderLayout.CENTER);
    topPanel.add(buttonPanel, BorderLayout.SOUTH);
    add(topPanel, BorderLayout.NORTH);

    // ==== DefaultTableModel Setup ====
    tableModel = new DefaultTableModel(new String[]{"Type", "ID", "Location", "Status"}, 0);
    table = new JTable(tableModel);
    JScrollPane scrollPane = new JScrollPane(table);
    add(scrollPane, BorderLayout.CENTER);

    // ==== Scrollable Resource Map ====
    statusMapPanel.setPreferredSize(new Dimension(800, 600));
    JScrollPane scrollPaneMap = new JScrollPane(
      statusMapPanel,
      JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
      JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED
    );
    scrollPaneMap.setBorder(BorderFactory.createTitledBorder("Resource Map"));
    scrollPaneMap.setPreferredSize(new Dimension(250, 400)); // Container size
    add(scrollPaneMap, BorderLayout.EAST);

    // ==== Save Button Logic ====
    saveBtn.addActionListener(e -> {
      String type = (String) resourceTypeField.getSelectedItem();
      String location = locationField.getText();
      String status = (String) statusField.getSelectedItem();
      String extra = extraInfoField.getText();

      if (location.isEmpty()) {
        JOptionPane.showMessageDialog(this, "Location cannot be empty!", "Validation Error", JOptionPane.WARNING_MESSAGE);
        return;
      }

      CityResource resource = null;
      // String id = "R" + (int) (Math.random() * 10000);
      String id = ResourceIDGenerator.generateID(type);

      switch (type) {
        case "TransportUnit":
        resource = new TransportUnit(id, location, status, 40, 0.25, "B1");
        break;
        case "PowerStation":
        resource = new PowerStation(id, location, status, 500.0, false);
        break;
        case "EmergencyService":
        resource = new EmergencyService(id, location, status, "Fire", 6.0);
        break;
      }

      if (resource != null) {
        repository.add(resource);
        // Start dynamic scheduling thread for TransportUnit
        
        // if (resource instanceof TransportUnit tu) {
        //   new Thread(tu).start();
        // }
        
        tableModel.addRow(new Object[]{
          type, resource.getResourceID(), resource.getLocation(), resource.getStatus()
        });
        clearForm();
        CityManager.checkDependencies(repository.getAll());
        statusMapPanel.setResources(repository.getAll()); // Update map panel
      }
    });

    // ==== Delete Button Logic ====
    deleteBtn.addActionListener(e -> {
      int selectedRow = table.getSelectedRow();
      if (selectedRow == -1) {
        JOptionPane.showMessageDialog(this, "Please select a row to delete.", "No Selection", JOptionPane.WARNING_MESSAGE);
        return;
      }

      int confirm = JOptionPane.showConfirmDialog(this, "Are you sure you want to delete this resource?", "Confirm Delete", JOptionPane.YES_NO_OPTION);
      if (confirm == JOptionPane.YES_OPTION) {
        String resourceID = (String) tableModel.getValueAt(selectedRow, 1); // Column 1 = Resource ID

        CityResource toRemove = null;
        for (CityResource r : repository.getAll()) {
          if (r.getResourceID().equals(resourceID)) {
            toRemove = r;
            break;
          }
        }

        if (toRemove != null) {
          repository.remove(toRemove);
          CityManager.removeResource(toRemove);
          tableModel.removeRow(selectedRow); // Remove from JTable
          JOptionPane.showMessageDialog(this, "Resource " + resourceID + " deleted.");
        }
      }
    });

    // ==== Filter Button Logic ====
    filterBtn.addActionListener(e -> {
      String[] options = {"Active", "Offline", "Maintenance"};
      String selectedStatus = (String) JOptionPane.showInputDialog(
        this,
        "Select resource status to filter:",
        "Filter Resources",
        JOptionPane.QUESTION_MESSAGE,
        null,
        options,
        options[0]
      );
      if (selectedStatus != null) {
        tableModel.setRowCount(0);
        for (CityResource r : repository.getAll()) {
          String type = r.getClass().getName();
          String status = r.getStatus();
          if (status.equalsIgnoreCase(selectedStatus)) {
            tableModel.addRow(new Object[]{
              type,
              r.getResourceID(),
              r.getLocation(),
              status
            });
          }
        }
      }
      JOptionPane.showMessageDialog(this, "Showing only " + selectedStatus + " resources.");
    });

    // ==== Update Button Logic ====
    updateBtn.addActionListener(e -> {
      int selectedRow = table.getSelectedRow();
      if (selectedRow == -1) {
        JOptionPane.showMessageDialog(this, "Please select a row to update.", "No Selection", JOptionPane.WARNING_MESSAGE);
        return;
      }

      String resourceID = (String) table.getValueAt(selectedRow, 1);

      CityResource resourceToUpdate = null;
      for (CityResource r : repository.getAll()) {
        if (r.getResourceID().equals(resourceID)) {
          resourceToUpdate = r;
          break;
        }
      }

      if (resourceToUpdate != null) {
        // Show dropdown for new status
        String[] options = {"Active", "Offline", "Maintenance"};
        String newStatus = (String) JOptionPane.showInputDialog(
            this,
            "Select new status for " + resourceID + ":",
            "Update Status",
            JOptionPane.QUESTION_MESSAGE,
            null,
            options,
            resourceToUpdate.getStatus()
        );

        if (newStatus != null && !newStatus.isEmpty()) {
          // Update logic
          if (resourceToUpdate instanceof PowerStation ps) {
            ps.setStatus(newStatus); // Smart override
          } else {
            resourceToUpdate.setStatus(newStatus);
          }

          table.setValueAt(newStatus, selectedRow, 3); // Column 3 = Status

          Metrics.recalculateFrom(repository.getAll());
          statusMapPanel.setResources(repository.getAll());
          CityManager.checkDependencies(repository.getAll());

          JOptionPane.showMessageDialog(this, "Status updated for " + resourceID + " to " + newStatus);
        }
      }
    });

    // ==== SaveToFile Button Logic ====
    saveToFileBtn.addActionListener(e -> {
      repository.saveToFile("resources.json");
      JOptionPane.showMessageDialog(this, "Resources saved to file successfully.");
    });

    // ==== LoadFromFile Button Logic ====
    loadFromFileBtn.addActionListener(e -> {
      CityManager.reset();
      repository.loadFromFile("resources.json", CityResource.class);

      // Clear existing table
      tableModel.setRowCount(0);

      for (CityResource r : repository.getAll()) {
        String type = r.getClass().getSimpleName();

        // Start dynamic route thread for TransportUnit
        if (r instanceof TransportUnit tu) {
          new Thread(tu).start();
        }

        tableModel.addRow(new Object[]{
          type, r.getResourceID(), r.getLocation(), r.getStatus()
        });
      }

      Metrics.recalculateFrom(repository.getAll());
      CityManager.checkDependencies(repository.getAll());
      statusMapPanel.setResources(repository.getAll());
      JOptionPane.showMessageDialog(this, "Resources loaded from file.");
    });

  }

  private void clearForm() {
    locationField.setText("");
    extraInfoField.setText("");
    resourceTypeField.setSelectedIndex(0);
    statusField.setSelectedIndex(0);
  }
}

