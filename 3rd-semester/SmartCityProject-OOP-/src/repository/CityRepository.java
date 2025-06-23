// repository/CityRepository.java
package repository;

import utils.GsonUtils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

public class CityRepository<T> {
  private List<T> items = new ArrayList<>();
  // private final Gson gson = new GsonBuilder().setPrettyPrinting().create();
  private final Gson gson = GsonUtils.createGsonWithTypeAdapter();

  public void add(T item) {
    items.add(item);
  }

  public void remove(T item) {
    items.remove(item);
  }

  public List<T> getAll() {
    return items;
  }

  public void saveToFile(String filePath) {
    try (Writer writer = new FileWriter(filePath)) {
      gson.toJson(items, writer);
      System.out.println("Saved to: " + filePath);
    } catch (IOException e) {
      System.err.println("Error saving data: " + e.getMessage());
    }
  }

  public void loadFromFile(String filePath, Class<T> clazz) {
    try (Reader reader = new FileReader(filePath)) {
      Type type = TypeToken.getParameterized(List.class, clazz).getType();
      items = gson.fromJson(reader, type);
      System.out.println("Loaded from: " + filePath);
    } catch (FileNotFoundException e) {
      System.err.println("File not found: " + filePath);
    } catch (Exception e) {
      System.err.println("Error loading data: " + e.getMessage());
    }
  }
}


