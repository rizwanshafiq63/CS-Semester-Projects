// utils/ResourceIDGenerator
package utils;

import java.util.HashMap;
import java.util.Map;

public class ResourceIDGenerator {
  private static Map<String, Integer> counters = new HashMap<>();

  static {
    counters.put("TransportUnit", 0);
    counters.put("PowerStation", 0);
    counters.put("EmergencyService", 0);
  }

  public static String generateID(String type) {
    int count = counters.getOrDefault(type, 0) + 1;
    counters.put(type, count);

    String prefix;
    switch (type) {
      case "TransportUnit":
      prefix = "TRANS";
      break;
      case "PowerStation":
      prefix = "PWR";
      break;
      case "EmergencyService":
      prefix = "EMER";
      break;
      default:
      prefix = "GEN";
    }

    return prefix + String.format("-%04d", count);
  }
}

