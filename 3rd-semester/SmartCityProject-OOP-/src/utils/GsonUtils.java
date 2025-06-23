// utils/GsonUtils.java
package utils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import utils.RuntimeTypeAdapterFactory;
import models.*;

public class GsonUtils {

  public static Gson createGsonWithTypeAdapter() {
    RuntimeTypeAdapterFactory<CityResource> typeFactory =
    RuntimeTypeAdapterFactory.of(CityResource.class, "type")
    .registerSubtype(TransportUnit.class, "TransportUnit")
    .registerSubtype(PowerStation.class, "PowerStation")
    .registerSubtype(EmergencyService.class, "EmergencyService");

    return new GsonBuilder().registerTypeAdapterFactory(typeFactory).setPrettyPrinting().create();
  }
}

