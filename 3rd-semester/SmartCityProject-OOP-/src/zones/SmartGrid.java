// zones/SmartGrid.java
package zones;

import models.PowerStation;
import java.util.ArrayList;
import java.util.List;

public class SmartGrid {
  private List<PowerStation> powerStations;
  private List<Consumer> consumers;

  public SmartGrid() {
    this.powerStations = new ArrayList<>();
    this.consumers = new ArrayList<>();
  }

  public void addPowerStation(PowerStation station) {
    powerStations.add(station);
  }

  public void addConsumer(Consumer consumer) {
    consumers.add(consumer);
  }

  public double getTotalEnergyOutput() {
    return powerStations.stream().mapToDouble(PowerStation::getEnergyOutputRate).sum();
  }

  public double getTotalEnergyConsumed() {
    return consumers.stream().mapToDouble(Consumer::getEnergyConsumed).sum();
  }

  public void displaySmartGridStatus() {
    System.out.println("=== Power Stations ===");
    for (PowerStation ps : powerStations) {
      System.out.println(ps);
    }
    System.out.println("\n=== Consumers ===");
    for (Consumer c : consumers) {
      System.out.println(c);
    }

    System.out.println("\nTotal Output: " + getTotalEnergyOutput() + " MW/hr");
    System.out.println("Total Consumption: " + getTotalEnergyConsumed() + " kWh");
  }
}


