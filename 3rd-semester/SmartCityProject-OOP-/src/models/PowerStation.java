// models/PowerStation.java
package models;

import interfaces.Alertable;
import interfaces.Reportable;
import utils.Metrics;

public class PowerStation extends CityResource implements Alertable, Reportable {
  private double energyOutputRate; // MW/hour
  private boolean isOutageProne; // matlb output ni aa ri

  public PowerStation(String resourceID, String location, String status,
    double energyOutputRate, boolean isOutageProne) {
    super(resourceID, location, status);
    // this.energyOutputRate = energyOutputRate;
    this.energyOutputRate = status.equalsIgnoreCase("active") ? energyOutputRate : 0.0;
    this.isOutageProne = isOutageProne;
    if (status.equalsIgnoreCase("active")) {
      Metrics.totalEnergyOutput += energyOutputRate; // Update city-wide metric
    }
  }

  @Override
  public double calculateMaintenanceCost() {
    return energyOutputRate * 200; // dummy formula
  }

  public double getEnergyOutputRate() {
    return energyOutputRate;
  }

  public void setEnergyOutputRate(double energyOutputRate) {
    this.energyOutputRate = energyOutputRate;
  }

  public boolean isOutageProne() {
    return isOutageProne;
  }

  public void setOutageProne(boolean outageProne) {
    isOutageProne = outageProne;
  }

  @Override
  public String toString() {
    return super.toString() + ", Output Rate: " + energyOutputRate + " MW/hr";
  }

  @Override
  public void sendEmergencyAlert() {
    if (isOutageProne) {
      System.out.println("Outage Alert: PowerStation at " + location + " is offline.");
    }
  }

  @Override
  public String generateUsageReport() {
    return "Energy Output: " + energyOutputRate + " MW/hr, Outage Prone: " + isOutageProne;
  }

  @Override
  public void setStatus(String newStatus) {
    boolean wasActive = this.status.equalsIgnoreCase("active");
    boolean willBeActive = newStatus.equalsIgnoreCase("active");

    if (wasActive && !willBeActive) {
      this.energyOutputRate = 0.0;
        Metrics.totalEnergyOutput -= this.energyOutputRate;
    } else if (!wasActive && willBeActive) {
      this.energyOutputRate = 500.0;
        Metrics.totalEnergyOutput += this.energyOutputRate;
    }

    this.status = newStatus;
  }

}


