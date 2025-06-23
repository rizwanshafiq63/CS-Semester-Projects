import java.util.Scanner;

// Hospital Class
// Maximum capacity of the hospital is 100 patients
// Maximum number of departments is 10
// Each department can have a maximum of 10 doctors and 20 patients
class Hospital {
  private Department[] departments = new Department[10];
  private int departmentCount = 0;
  private static final int MAX_CAPACITY = 100;
  private static int totalPatients = 0;

  public void addDepartment(String name) {
    if (departmentCount < departments.length) {
      departments[departmentCount++] = new Department(name);
    } else {
      System.out.println("Maximum departments reached!");
    }
  }

  public void removeDepartment(String name) {
    boolean found = false;
    for (int i = 0; i < departmentCount; i++) {
      if (departments[i].getName().equalsIgnoreCase(name)) {
        found = true;
        if (i != departmentCount - 1) { // Only swap if it's not the last department
          departments[i] = departments[departmentCount - 1];
        }
        departments[--departmentCount] = null;
        return;
      }
    }
    if (!found) {
      System.out.println("Department not found!");
    } else {
      System.out.println("Department \"" +name+ "\" removed successfully!");
    }
  }

  public void addDoctor(String deptName, String doctorName) {
    boolean found = false;
    for (int i = 0; i < departmentCount; i++) {
      if (departments[i].getName().equalsIgnoreCase(deptName)) {
        found = true;
        departments[i].addDoctor(new Doctor(doctorName));
        return;
      }
    }
    if (!found) {
      System.out.println("Department not found!");
    } else {
      System.out.println("Doctor \"" +doctorName+ "\" added successfully to department \"" +deptName+ "\"!");
    }
  }

  public void admitPatient(String deptName, String patientName, String doctorName) {
    if (totalPatients >= MAX_CAPACITY) {
      System.out.println("Hospital is at full capacity!");
      return;
    }
    Doctor doctor = null;
    for (int i = 0; i < departmentCount; i++) {
      if (departments[i].getName().equalsIgnoreCase(deptName)) {
        doctor = departments[i].getDoctor(doctorName);
        if (doctor != null) {
          departments[i].addPatient(new Patient(patientName, doctor));
          totalPatients++;
          return;
        }
      }
    }
    if (doctor == null) {
      System.out.println("Doctor \"" +doctorName+ "\" not found in department \"" +deptName+ "\"!");
    } else {
      System.out.println("Department \"" +deptName+ "\" not found!");
    }
  }

  public void dischargePatient(String deptName, String patientName) {
    for (int i = 0; i < departmentCount; i++) {
      if (departments[i].getName().equalsIgnoreCase(deptName)) {
        if (departments[i].removePatient(patientName)) {
          System.out.println("Patient \"" + patientName + "\" discharged successfully from department \"" + deptName + "\"!");
          totalPatients--;
          return;
        } else {
          System.out.println("Patient \"" + patientName + "\" not found in department \"" + deptName + "\"!");
        }
        return;
      }
    }
    System.out.println("Department \"" + deptName + "\" not found!");
  }

  public void displayPatients() {
    for (int i = 0; i < departmentCount; i++) {
      departments[i].displayPatients();
    }
  }
}

// Department Class
class Department {
  private String name;
  private Doctor[] doctors = new Doctor[10];
  private Patient[] patients = new Patient[20];
  private int doctorCount = 0;
  private int patientCount = 0;

  public Department(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }

  public void addDoctor(Doctor doctor) {
    if (doctorCount < doctors.length) {
      doctors[doctorCount++] = doctor;
    } else {
      System.out.println("Maximum doctors reached in department \"" + name + "\"!");
    }
  }

  public Doctor getDoctor(String name) {
    for (int i = 0; i < doctorCount; i++) {
      if (doctors[i].getName().equalsIgnoreCase(name)) {
        return doctors[i];
      }
    }
    return null;
  }

  public void addPatient(Patient patient) {
    if (patientCount < patients.length) {
      patients[patientCount++] = patient;
    } else {
      System.out.println("Maximum patients reached in department \"" + name + "\"!");
    }
  }

  public boolean removePatient(String name) {
    for (int i = 0; i < patientCount; i++) {
      if (patients[i].getName().equalsIgnoreCase(name)) {
        patients[i] = patients[--patientCount];
        patients[patientCount] = null;
        return true;
      }
    }
    return false;
  }

  public void displayPatients() {
    System.out.println("Department: " + name);
    for (int i = 0; i < patientCount; i++) {
      System.out.println(" " +(i+1)+ ". Patient: " + patients[i].getName() + ", Doctor: " + patients[i].getDoctor().getName());
    }
  }
}

// Doctor Class
class Doctor {
  private String name;

  public Doctor(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }
}

// Patient Class
class Patient {
  private String name;
  private Doctor doctor;

  public Patient(String name, Doctor doctor) {
    this.name = name;
    this.doctor = doctor;
  }

  public String getName() {
    return name;
  }

  public Doctor getDoctor() {
    return doctor;
  }
}

// Inheritance Example
// Base class
class Cardiology {
  protected String departmentName;

  public Cardiology() {
    this.departmentName = "Cardiology";
  }

  public void displayDepartmentInfo() {
    System.out.println("Department: " + departmentName);
  }
}

// Derived class
class CardiologyPatient extends Cardiology {
  private String patientName;

  public CardiologyPatient(String patientName) {
    super();  // Calls the constructor of Cardiology
    this.patientName = patientName;
  }

  public void displayPatientInfo() {
    displayDepartmentInfo();  // Method from parent class
    System.out.println("Patient Name: " + patientName);
  }
}

// Menu System
public class Lab_Mid_Array {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    Hospital hospital = new Hospital();

    while (true) {
      System.out.println("\nHospital Management System");
      System.out.println("1. Add Department");
      System.out.println("2. Remove Department");
      System.out.println("3. Add Doctor to Department");
      System.out.println("4. Admit Patient");
      System.out.println("5. Discharge Patient");
      System.out.println("6. Display Patients");
      System.out.println("7. Exit");

      // Prompting user for choice
      int choice = -1;
      while (choice < 1 || choice > 7) {
        System.out.print("Enter choice: ");
        try {
          choice = Integer.parseInt(sc.nextLine());  // Tries to read the input as an integer
          if (choice < 1 || choice > 7) {
            System.out.println("Invalid choice! Please enter a number between 1 and 7.");
          }
        } catch (NumberFormatException e) {
          System.out.println("Invalid input! Please enter a valid number.");
        }
      }

      switch (choice) {
        case 1:
        System.out.print("Enter department name: ");
        hospital.addDepartment(sc.nextLine());
        break;
        case 2:
        System.out.print("Enter department name: ");
        hospital.removeDepartment(sc.nextLine());
        break;
        case 3:
        System.out.print("Enter department name: ");
        String deptName = sc.nextLine();
        System.out.print("Enter doctor name: ");
        hospital.addDoctor(deptName, sc.nextLine());
        break;
        case 4:
        System.out.print("Enter department name: ");
        deptName = sc.nextLine();
        System.out.print("Enter patient name: ");
        String patientName = sc.nextLine();
        System.out.print("Enter doctor name: ");
        hospital.admitPatient(deptName, patientName, sc.nextLine());
        break;
        case 5:
        System.out.print("Enter department name: ");
        String dischargeDept = sc.nextLine();
        System.out.print("Enter patient name: ");
        String dischargePatient = sc.nextLine();
        hospital.dischargePatient(dischargeDept, dischargePatient);
        break;
        case 6:
        hospital.displayPatients();
        break;
        case 7:
        System.out.println("Exiting...");
        sc.close();
        return;
        default:
        System.out.println("Invalid choice!");
      }
    }
  }
}
// End of the program

