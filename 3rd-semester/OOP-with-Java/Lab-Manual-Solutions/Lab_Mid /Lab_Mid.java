import java.util.ArrayList;
import java.util.Scanner;

// Hospital Class
class Hospital {
  private ArrayList<Department> departments = new ArrayList<>();
  private static final int MAX_CAPACITY = 100;
  private static int totalPatients = 0;

  public void addDepartment(String name) {
    departments.add(new Department(name));
  }

  public void removeDepartment(String name) {
    departments.removeIf(dept -> dept.getName().equalsIgnoreCase(name));
  }

  public void addDoctor(String deptName, String doctorName) {
    for (Department dept : departments) {
      if (dept.getName().equalsIgnoreCase(deptName)) {
        dept.addDoctor(new Doctor(doctorName));
        return;
      }
    }
  }

  public void admitPatient(String deptName, String patientName, String doctorName) {
    if (totalPatients >= MAX_CAPACITY) {
      System.out.println("Hospital is at full capacity!");
      return;
    }
    for (Department dept : departments) {
      if (dept.getName().equalsIgnoreCase(deptName)) {
        Doctor doctor = dept.getDoctor(doctorName);
        if (doctor != null) {
          dept.addPatient(new Patient(patientName, doctor));
          totalPatients++;
          return;
        }
      }
    }
  }

  public void dischargePatient(String patientName) {
    for (Department dept : departments) {
      if (dept.removePatient(patientName)) {
        totalPatients--;
        return;
      }
    }
  }

  public void displayPatients() {
    for (Department dept : departments) {
      dept.displayPatients();
    }
  }
}

// Department Class
class Department {
  private String name;
  private ArrayList<Doctor> doctors = new ArrayList<>();
  private ArrayList<Patient> patients = new ArrayList<>();

  public Department(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }

  public void addDoctor(Doctor doctor) {
    doctors.add(doctor);
  }

  public Doctor getDoctor(String name) {
    for (Doctor doc : doctors) {
      if (doc.getName().equalsIgnoreCase(name)) {
        return doc;
      }
    }
    return null;
  }

  public void addPatient(Patient patient) {
    patients.add(patient);
  }

  public boolean removePatient(String name) {
    return patients.removeIf(patient -> patient.getName().equalsIgnoreCase(name));
  }

  public void displayPatients() {
    System.out.println("Department: " + name);
    for (Patient patient : patients) {
      System.out.println("Patient: " + patient.getName() + ", Doctor: " + patient.getDoctor().getName());
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

// Menu System
public class Lab_mid {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
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
      System.out.print("Enter choice: ");
      int choice = scanner.nextInt();
      scanner.nextLine();

      switch (choice) {
        case 1:
        System.out.print("Enter department name: ");
        hospital.addDepartment(scanner.nextLine());
        break;
        case 2:
        System.out.print("Enter department name: ");
        hospital.removeDepartment(scanner.nextLine());
        break;
        case 3:
        System.out.print("Enter department name: ");
        String deptName = scanner.nextLine();
        System.out.print("Enter doctor name: ");
        hospital.addDoctor(deptName, scanner.nextLine());
        break;
        case 4:
        System.out.print("Enter department name: ");
        deptName = scanner.nextLine();
        System.out.print("Enter patient name: ");
        String patientName = scanner.nextLine();
        System.out.print("Enter doctor name: ");
        hospital.admitPatient(deptName, patientName, scanner.nextLine());
        break;
        case 5:
        System.out.print("Enter patient name: ");
        hospital.dischargePatient(scanner.nextLine());
        break;
        case 6:
        hospital.displayPatients();
        break;
        case 7:
        System.out.println("Exiting...");
        scanner.close();
        return;
        default:
        System.out.println("Invalid choice!");
      }
    }
  }
}

