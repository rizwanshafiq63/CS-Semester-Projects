// models/TransportUnit.java
package models;

import interfaces.Reportable;
import utils.Metrics;

public class TransportUnit extends CityResource implements Reportable, Runnable {
  private int passengerCount;
  private double fuelConsumptionRate; // liters/km
  private String routeNumber;
  private boolean active = true;

  public TransportUnit(String resourceID, String location, String status,
    int passengerCount, double fuelConsumptionRate, String routeNumber) {
    super(resourceID, location, status);
    this.passengerCount = passengerCount;
    this.fuelConsumptionRate = fuelConsumptionRate;
    this.routeNumber = routeNumber;
    Metrics.totalTransportUnits++;
  }

  @Override
  public double calculateMaintenanceCost() {
    return fuelConsumptionRate * 150; // dummy formula
  }

  // Getters & setters

  public int getPassengerCount() {
    return passengerCount;
  }

  public void setPassengerCount(int passengerCount) {
    this.passengerCount = passengerCount;
  }

  public double getFuelConsumptionRate() {
    return fuelConsumptionRate;
  }

  public void setFuelConsumptionRate(double fuelConsumptionRate) {
    this.fuelConsumptionRate = fuelConsumptionRate;
  }

  public String getRouteNumber() {
    return routeNumber;
  }

  public void setRouteNumber(String routeNumber) {
    this.routeNumber = routeNumber;
  }

  @Override
  public String toString() {
    return super.toString() + ", Route: " + routeNumber + ", Passengers: " + passengerCount;
  }

  @Override
  public String generateUsageReport() {
    return "Route: " + routeNumber + ", Passengers: " + passengerCount + ", Fuel Rate: " + fuelConsumptionRate;
  }

  @Override
  public void run() {
    while (active) {
      try {
        Thread.sleep(5000); // every 5 seconds
        System.out.println("[Route Update] " + resourceID + " adjusted route dynamically.");
        // Optionally: update routeNumber = "R" + new Random().nextInt(100)
      } catch (InterruptedException e) {
        System.out.println(resourceID + " thread interrupted.");
        active = false;
      }
    }
  }

  public void stopRouteThread() {
    active = false;
  }
}


