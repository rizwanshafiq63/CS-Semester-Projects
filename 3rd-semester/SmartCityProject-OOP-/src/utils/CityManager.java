// utils/CityManager.java
package utils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.swing.JOptionPane;
import models.CityResource;
import models.EmergencyService;
import models.PowerStation;

public class CityManager {
    private static final Set<String> alertedStations = new HashSet<>();
    private static final List<PowerStation> knownProblematicStations = new ArrayList<>();
    private static final List<EmergencyService> knownActiveEmergencyServices = new ArrayList<>();
    // Maps PowerStationID -> Set of EmergencyServiceIDs it has already alerted
private static final Map<String, Set<String>> stationAlertMap = new HashMap<>();

    public static void checkDependencies(List<CityResource> resources) {
        for (CityResource r : resources) {
            if (r instanceof PowerStation ps) {
                boolean isProblematic = ps.isOutageProne() || ps.getStatus().equalsIgnoreCase("offline");

                if (isProblematic && !alertedStations.contains(ps.getResourceID())) {
                    String warning = "[!] Warning: PowerStation ()" + ps.getResourceID()
                            + ") is " + (ps.isOutageProne() ? "outage-prone" : "")
                            + (ps.isOutageProne() && ps.getStatus().equalsIgnoreCase("offline") ? " and " : "")
                            + (ps.getStatus().equalsIgnoreCase("offline") ? "offline" : "")
                            + " at " + ps.getLocation();

                    System.out.println("\n" + warning);
                    JOptionPane.showMessageDialog(null, warning, "PowerStation Warning", JOptionPane.WARNING_MESSAGE);

                    knownProblematicStations.add(ps);
                    alertedStations.add(ps.getResourceID());
                }
            } else if (r instanceof EmergencyService es) {
                if (es.getStatus().equalsIgnoreCase("active") &&
                    !knownActiveEmergencyServices.contains(es)) {
                    knownActiveEmergencyServices.add(es);
                }
            }
        }

        // Now match problematic PowerStations with known active EmergencyServices
for (PowerStation ps : knownProblematicStations) {
    String stationId = ps.getResourceID();

    for (EmergencyService es : knownActiveEmergencyServices) {
        if (es.getLocation().equalsIgnoreCase(ps.getLocation())) {
            String emergencyId = es.getResourceID();

            // Check if this EmergencyService has already been alerted by this PowerStation
            Set<String> alertedSet = stationAlertMap.get(stationId);
            boolean notYetAlerted = (alertedSet == null || !alertedSet.contains(emergencyId));

            if (notYetAlerted) {
                String alert = "[!] Alert: EmergencyService (" + emergencyId + ") at " + es.getLocation()
                        + " has been notified due to PowerStation issue.";
                System.out.println(alert);
                es.sendEmergencyAlert();
                JOptionPane.showMessageDialog(null, alert, "Emergency Alert", JOptionPane.INFORMATION_MESSAGE);

                // Update map to mark this EmergencyService as alerted
                if (alertedSet == null) {
                    alertedSet = new HashSet<>();
                    stationAlertMap.put(stationId, alertedSet);
                }
                alertedSet.add(emergencyId);
            }
        }
    }
}

        // // Now match problematic PowerStations with known active EmergencyServices
        // for (PowerStation ps : knownProblematicStations) {
        //     for (EmergencyService es : knownActiveEmergencyServices) {
        //         if (es.getLocation().equalsIgnoreCase(ps.getLocation())) {
        //             String alert = "[!] Alert: EmergencyService (" +es.getResourceID()+") at " + es.getLocation()
        //                     + " has been notified due to PowerStation issue.";
        //             System.out.println(alert);
        //             es.sendEmergencyAlert();
        //             JOptionPane.showMessageDialog(null, alert, "Emergency Alert", JOptionPane.INFORMATION_MESSAGE);
        //         }
        //     }
        // }
    }

    public static void removeResource(CityResource resource) {
    if (resource instanceof PowerStation ps) {
        alertedStations.remove(ps.getResourceID());
        knownProblematicStations.removeIf(p -> p.getResourceID().equals(ps.getResourceID()));
    } else if (resource instanceof EmergencyService es) {
        knownActiveEmergencyServices.removeIf(e -> e.getResourceID().equals(es.getResourceID()));
    }
}

    public static void reset() {
        alertedStations.clear();
        knownProblematicStations.clear();
        knownActiveEmergencyServices.clear();
    }
}
// stationAlertMap = {
//   "PWR-0001": ["EMER-001", "EMER-002"],
//   "PWR-0002": ["EMER-003"]
// }

  // public static void checkDependencies(List<CityResource> resources) {
  //       for (CityResource r : resources) {
  //           if (r instanceof PowerStation ps) {

  //               // 1. Show warning in GUI if outage-prone or offline
  //               if (ps.isOutageProne() || ps.getStatus().equalsIgnoreCase("Offline")) {
  //                   String warning = "[!] Warning: PowerStation " + ps.getResourceID()
  //                                  + " is either outage-prone or offline at " + ps.getLocation();
  //                   System.out.println("\n" + warning);
  //                   JOptionPane.showMessageDialog(null, warning, "PowerStation Warning", JOptionPane.WARNING_MESSAGE);
  //               }

  //               // 2. Alert EmergencyService if located at same place
  //               for (CityResource e : resources) {
  //                   if (e instanceof EmergencyService es) {
  //                       if (es.getLocation().equalsIgnoreCase(ps.getLocation())) {
  //                           String alert = "[!] Alert: EmergencyService at " + es.getLocation()
  //                                        + " has been notified due to PowerStation presence.";
  //                           System.out.println(alert);
  //                           es.sendEmergencyAlert();

  //                           // Show GUI alert too
  //                           JOptionPane.showMessageDialog(null, alert, "Emergency Alert", JOptionPane.INFORMATION_MESSAGE);
  //                       }
  //                   }
  //               }
  //           }
  //         }
  //       }
      

  


