// zones/ResourceHub.java
package zones;

import models.TransportUnit;
import java.util.ArrayList;
import java.util.List;

public class ResourceHub {
  private String hubName;
  private List<TransportUnit> transportUnits;

  public ResourceHub(String hubName) {
    this.hubName = hubName;
    this.transportUnits = new ArrayList<>();
  }

  public void addTransportUnit(TransportUnit unit) {
    transportUnits.add(unit);
  }

  public List<TransportUnit> getTransportUnits() {
    return transportUnits;
  }

  public String getHubName() {
    return hubName;
  }

  public void displayHubInfo() {
    System.out.println("Resource Hub: " + hubName);
    for (TransportUnit t : transportUnits) {
      System.out.println(t);
    }
  }
}


