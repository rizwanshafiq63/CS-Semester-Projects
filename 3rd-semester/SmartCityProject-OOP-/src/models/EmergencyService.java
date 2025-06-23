// models/EmergencyService.java
package models;

// Importing interfaces
import interfaces.Alertable;
import interfaces.Reportable;
import utils.Metrics;

public class EmergencyService extends CityResource implements Alertable, Reportable {
  private String serviceType; // e.g., "Fire", "Police"
  private double responseTime; // in minutes

  public EmergencyService(String resourceID, String location, String status,
    String serviceType, double responseTime) {
    super(resourceID, location, status);
    this.serviceType = serviceType;
    this.responseTime = responseTime;
  }

  @Override
  public double calculateMaintenanceCost() {
    return responseTime * 100; // dummy formula
  }

  public String getServiceType() {
    return serviceType;
  }

  public void setServiceType(String serviceType) {
    this.serviceType = serviceType;
  }

  public double getResponseTime() {
    return responseTime;
  }

  public void setResponseTime(double responseTime) {
    this.responseTime = responseTime;
  }

  @Override
  public String toString() {
    return super.toString() + ", Service: " + serviceType + ", Response Time: " + responseTime + " min";
  }

  @Override
  public void sendEmergencyAlert() {
    System.out.println("Emergency Alert sent from " + serviceType + " Unit at " + location);
    Metrics.totalAlertsSent++;
    Metrics.totalEmergencyResponseTime += responseTime;
  }

  @Override
  public String generateUsageReport() {
    return "Service: " + serviceType + ", Avg Response Time: " + responseTime + " minutes";
  }
}


