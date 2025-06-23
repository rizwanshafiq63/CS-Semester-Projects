// zones/Consumer.java
package zones;

import utils.Metrics;

public class Consumer {
  private String consumerID;
  private String type; // Household or Industry
  private double energyConsumed;

  public Consumer(String consumerID, String type, double energyConsumed) {
    this.consumerID = consumerID;
    this.type = type;
    this.energyConsumed = energyConsumed;
  }

  public double getEnergyConsumed() {
    return energyConsumed;
  }

  public void addConsumption(double amount) {
    energyConsumed += amount;
    Metrics.totalEnergyConsumed += amount;
  }

  public String toString() {
    return consumerID + " | " + type + " | " + energyConsumed + " kWh";
  }
}

