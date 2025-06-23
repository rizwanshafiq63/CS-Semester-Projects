// utils/Metrics.java
package utils;

import java.util.List;
import models.*;

public class Metrics {
  public static double totalEnergyConsumed = 0;
  public static double totalEnergyOutput = 0;
  public static double totalEmergencyResponseTime = 0;
  public static int totalAlertsSent = 0;
  public static int totalTransportUnits = 0;

  public static void reset() {
    totalEnergyConsumed = 0;
    totalEnergyOutput = 0;
    totalEmergencyResponseTime = 0;
    totalAlertsSent = 0;
    totalTransportUnits = 0;
  }

  public static void recalculateFrom(List<CityResource> resources) {
    reset();

    for (CityResource r : resources) {
      if (r instanceof PowerStation ps) {
        if (ps.getStatus().equalsIgnoreCase("active")) {
          totalEnergyOutput += ps.getEnergyOutputRate();
        }
      } else if (r instanceof EmergencyService es) {
        totalEmergencyResponseTime += es.getResponseTime();
        totalAlertsSent++; // Optional: count as "potential alert"
      } else if (r instanceof TransportUnit) {
        totalTransportUnits++;
      }
    }
  }

  public static void display() {
    System.out.println("\nCity-Wide Metrics:");
    System.out.println("Total Energy Consumed: " + totalEnergyConsumed + " kWh");
    System.out.println("Total Energy Output: " + totalEnergyOutput + " MW/hr");
    System.out.println("Total Emergency Response Time: " + totalEmergencyResponseTime + " min");
    System.out.println("Total Alerts Sent: " + totalAlertsSent);
    System.out.println("Total Transport Units: " + totalTransportUnits);
  }
}

