import models.EmergencyService;
import models.PowerStation;
import models.TransportUnit;
import repository.CityRepository;
import utils.Metrics;
import zones.CityZone;
import zones.Consumer;
import zones.ResourceHub;
import zones.SmartGrid;

public class CLI_Based_Tester {
      public static void main(String[] args) {
        System.out.println("🚀 Smart City Resource Management System - Test Run\n");

        // ==== Create Emergency Service ====
        EmergencyService fireDept = new EmergencyService(
                "EM001", "Sector A", "Active", "Fire", 5.5);
        EmergencyService policeDept = new EmergencyService(
                "EM002", "Sector B", "Active", "Police", 4.2);

        // ==== Create Power Stations ====
        PowerStation p1 = new PowerStation(
                "PS001", "Zone 1", "Online", 500, true);
        PowerStation p2 = new PowerStation(
                "PS002", "Zone 2", "Online", 400, false);

        // ==== Create Transport Units ====
        TransportUnit bus1 = new TransportUnit(
                "TU001", "Station 1", "Running", 45, 0.12, "B12");
        TransportUnit train1 = new TransportUnit(
                "TU002", "Central", "Running", 150, 0.30, "T9");

        // ==== Build Resource Hub ====
        ResourceHub hub = new ResourceHub("Central Hub");
        hub.addTransportUnit(bus1);
        hub.addTransportUnit(train1);

        // ==== Build City Zone ====
        CityZone zoneA = new CityZone("Zone A");
        zoneA.addResourceHub(hub);

        // ==== Build Smart Grid ====
        SmartGrid grid = new SmartGrid();
        grid.addPowerStation(p1);
        grid.addPowerStation(p2);
        grid.addConsumer(new Consumer("C001", "Household", 120.5));
        grid.addConsumer(new Consumer("C002", "Industry", 890.0));

        // ==== Simulate Alerts ====
        fireDept.sendEmergencyAlert();
        policeDept.sendEmergencyAlert();
        p1.sendEmergencyAlert(); // Only this is outage-prone

        // ==== Display Reports ====
        System.out.println("\n📄 Reports:");
        System.out.println(bus1.generateUsageReport());
        System.out.println(p1.generateUsageReport());
        System.out.println(fireDept.generateUsageReport());

        // ==== Display Zone Info ====
        System.out.println("\n🌐 City Zones:");
        zoneA.displayZoneInfo();

        // ==== Smart Grid Info ====
        System.out.println("\n🔌 Smart Grid Status:");
        grid.displaySmartGridStatus();

        // ==== Save data (demo only) ====
        CityRepository<TransportUnit> transportRepo = new CityRepository<>();
        transportRepo.add(bus1);
        transportRepo.add(train1);
        transportRepo.saveToFile("transport_units.json");

        // ==== Display Metrics ====
        Metrics.display();
    }
}
