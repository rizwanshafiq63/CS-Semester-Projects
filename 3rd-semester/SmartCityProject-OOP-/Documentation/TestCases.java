import models.*;
import utils.CityManager;
import java.util.*;
import interfaces.*;

public class TestCases {
    public static void main(String[] args) {
        System.out.println("===== Test Case 1: Emergency Alert Triggered =====");
        PowerStation ps1 = new PowerStation("PS-01", "Zone A", "Offline", 500.0, true);
        EmergencyService es1 = new EmergencyService("ES-01", "Zone A", "Active", "Fire", 4.5);
        CityManager.checkDependencies(Arrays.asList(ps1, es1));

        System.out.println("\n===== Test Case 2: No Alert — Different Zone =====");
        PowerStation ps2 = new PowerStation("PS-02", "Zone B", "Offline", 400.0, false);
        EmergencyService es2 = new EmergencyService("ES-02", "Zone C", "Active", "Medical", 5.0);
        CityManager.checkDependencies(Arrays.asList(ps2, es2));

        System.out.println("\n===== Test Case 3: Polymorphic Reports =====");
        Reportable r1 = new TransportUnit("TU-01", "Zone D", "Active", 50, 0.20, "R5");
        Reportable r2 = new PowerStation("PS-03", "Zone D", "Active", 600.0, false);
        System.out.println(r1.generateUsageReport());
        System.out.println(r2.generateUsageReport());
    }
}
