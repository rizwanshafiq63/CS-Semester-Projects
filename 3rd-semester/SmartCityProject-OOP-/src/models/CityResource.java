// models/CityResource.java
package models;

public abstract class CityResource {
  protected String resourceID;
  protected String location;
  protected String status;

  public CityResource(String resourceID, String location, String status) {
    this.resourceID = resourceID;
    this.location = location;
    this.status = status;
  }

  public String getResourceID() {
    return resourceID;
  }

  public void setResourceID(String resourceID) {
    this.resourceID = resourceID;
  }

  public String getLocation() {
    return location;
  }

  public void setLocation(String location) {
    this.location = location;
  }

  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }

  // Abstract method to be implemented by subclasses
  public abstract double calculateMaintenanceCost();

  @Override
  public String toString() {
    return "ResourceID: " + resourceID + ", Location: " + location + ", Status: " + status;
  }
}

