// gui PublicPanel.java
package gui;

import java.awt.*;
import javax.swing.*;
import java.util.List;

import models.CityResource;
import models.PowerStation;
import repository.CityRepository;
import utils.Metrics;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.data.category.DefaultCategoryDataset;

public class PublicPanel extends JPanel {

  private JTextArea metricsArea;
  private Timer refreshTimer;
  private ChartPanel chartPanel;
  // Reference to the main CityResource repository
  private static CityRepository<CityResource> repository = new CityRepository<>();

  public PublicPanel() {
    setLayout(new BorderLayout());

    JLabel label = new JLabel("Public Resource Overview", JLabel.CENTER);
    label.setFont(new Font("Arial", Font.BOLD, 20));
    add(label, BorderLayout.NORTH);

    // === Metrics Area ===
    metricsArea = new JTextArea();
    metricsArea.setFont(new Font("Monospaced", Font.PLAIN, 14));
    metricsArea.setEditable(false);

    JScrollPane scrollPane = new JScrollPane(metricsArea);
    add(scrollPane, BorderLayout.CENTER);

    // === Chart Panel (Energy Output) ===
    chartPanel = new ChartPanel(createChart());
    chartPanel.setPreferredSize(new Dimension(500, 300));
    add(chartPanel, BorderLayout.SOUTH);

    // === Timer to refresh metrics every 2 seconds ===
    refreshTimer = new Timer(2000, e -> {
      updateMetrics();
      updateChart();
    });
    refreshTimer.start();

    // === Simulate energy consumption every 45 seconds IF at least one active PowerStation 
    Timer energySimTimer = new Timer(45000, e -> {
      List<CityResource> allResources = repository.getAll();
      boolean hasActivePowerStation = allResources.stream()
        .filter(r -> r instanceof PowerStation)
        .map(r -> (PowerStation) r)
        .anyMatch(ps -> ps.getStatus().equalsIgnoreCase("active"));

      if (hasActivePowerStation) {
        int usage = (int)(Math.random() * 15); // Random 0–20 kWh
        utils.Metrics.totalEnergyConsumed += usage;
      }
    });
    energySimTimer.start();

    updateMetrics(); // Initial update
  }

  private void updateMetrics() {
    StringBuilder sb = new StringBuilder();
    sb.append("Total Energy Consumed: ").append(Metrics.totalEnergyConsumed).append(" kWh\n");
    sb.append("Total Energy Output:   ").append(Metrics.totalEnergyOutput).append(" MW/hr\n");
    sb.append("Emergency Response:    ").append(Metrics.totalEmergencyResponseTime).append(" min\n");
    sb.append("Alerts Sent:           ").append(Metrics.totalAlertsSent).append("\n");
    sb.append("Transport Units:       ").append(Metrics.totalTransportUnits).append("\n");

    metricsArea.setText(sb.toString());
  }

  private JFreeChart createChart() {
    DefaultCategoryDataset dataset = new DefaultCategoryDataset();
    List<CityResource> allResources = repository.getAll();

    for (CityResource r : allResources) {
      if (r instanceof PowerStation ps) {
        dataset.addValue(ps.getEnergyOutputRate(), "MW/hr", ps.getResourceID());
      }
    }

    return ChartFactory.createBarChart(
      "Energy Output by Power Station",
      "Station ID",
      "MW/hr",
      dataset
    );
  }

  private void updateChart() {
    chartPanel.setChart(createChart());
  }

  // This method should be called from AdminPanel or Main to share the repository
  public static void setRepository(CityRepository<CityResource> sharedRepo) {
    repository = sharedRepo;
  }
}

