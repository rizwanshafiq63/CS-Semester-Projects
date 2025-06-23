// zones/CityZone.java
package zones;

import java.util.ArrayList;
import java.util.List;

public class CityZone {
  private String zoneName;
  private List<ResourceHub> resourceHubs;

  public CityZone(String zoneName) {
    this.zoneName = zoneName;
    this.resourceHubs = new ArrayList<>();
  }

  public void addResourceHub(ResourceHub hub) {
    resourceHubs.add(hub);
  }

  public List<ResourceHub> getResourceHubs() {
    return resourceHubs;
  }

  public String getZoneName() {
    return zoneName;
  }

  public void displayZoneInfo() {
    System.out.println("City Zone: " + zoneName);
    for (ResourceHub hub : resourceHubs) {
      hub.displayHubInfo();
    }
  }
}

