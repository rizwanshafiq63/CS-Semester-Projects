/* ACTIVITY_01: The following example demonstrates polymorphism for a overridden method. */

abstract class Employee {
  private String firstName;
  private String lastName;
  private String socialSecurityNumber;
  public Employee( String first, String last, String ssn ) {
    firstName = first;
    lastName = last;
    socialSecurityNumber = ssn;
  }
  public String toString() {
    return String.format( "%s %s\nsocial security number: %s", firstName, lastName, socialSecurityNumber );
  } // end method toString
  public abstract double earnings();
}

class SalariedEmployee extends Employee {
  private double weeklySalary;
  // four-argument constructor
  public SalariedEmployee( String first, String last, String ssn,double salary ) {
    super( first, last, ssn ); // pass to Employee constructor
    weeklySalary = salary ;
  }
  @Override
  public double earnings() {
    return weeklySalary;
  }
}

class HourlyEmployee extends Employee {
  private double wage; // wage per hour
  private double hours; // hours worked for week
  // five-argument constructor
  public HourlyEmployee( String first, String last, String ssn,double hourlyWage, double hoursWorked ) {
    super( first, last, ssn );
    wage = hourlyWage;
    hours = hoursWorked;
  }
  @Override
  public double earnings() {
    if (hours <= 40 ) // no overtime
      return wage * hours ;
    else
      return 40 * wage + (hours - 40 ) * wage * 1.5;
  } 
}

class CommissionEmployee extends Employee {
  private double grossSales; // gross weekly sales
  private double commissionRate; // commission percentage
  // five-argument constructor
  public CommissionEmployee( String first, String last, String ssn,double sales, double rate ) {
    super( first, last, ssn );
    grossSales = sales ;
    commissionRate = rate;
  }
  @Override
  public double earnings() {
    return commissionRate * grossSales ;
  }
}

class BasePlusCommissionEmployee extends CommissionEmployee {
  private double baseSalary; // base salary per week
  public BasePlusCommissionEmployee( String first, String last,String ssn, double sales, double rate, double salary ) {
    super( first, last, ssn, sales, rate );
    baseSalary = salary; // validate and store base salary
  }
  public void setBaseSalary(double baseSalary) {
    this.baseSalary = baseSalary;
  }
  public double getBaseSalary() { 
    return baseSalary;
  }
  @Override
  public double earnings() {
    return baseSalary + super.earnings();
  } 
}

// Payroll System Test
public class Activities {
  public static void main( String[] args ) {
    SalariedEmployee salariedEmployee = new SalariedEmployee ("John", "Smith", "111-11-1111", 800.00 );
    HourlyEmployee hourlyEmployee= new HourlyEmployee( "Karen", "Price", "222-22-2222", 16.75, 40 );
    CommissionEmployee commissionEmployee = new CommissionEmployee( "Sue", "Jones", "333-33-3333", 10000, .06 );
    BasePlusCommissionEmployee basePlusCommissionEmployee = new BasePlusCommissionEmployee("Bob", "Lewis", "444-44-4444", 5000, .04, 300 );
    Employee[] employees = new Employee[ 4 ];
    // initialize array with Employees
    employees[ 0 ] = salariedEmployee;
    employees[ 1 ] = hourlyEmployee;
    employees[ 2 ] = commissionEmployee;
    employees[ 3 ] = basePlusCommissionEmployee;
    for (int i=0; i<4 ;i++) {
      System.out.println(employees[i].earnings()); //polymorphic call
    } 

    /* ACTIVITY_02: The following example demonstrates downcasting. */
    for (int i=0; i<4 ;i++) {
      if (employees [i] instanceof BasePlusCommissionEmployee) {
        BasePlusCommissionEmployee emp = (BasePlusCommissionEmployee )employees[i];
        emp.setBaseSalary( 1.10 * emp.getBaseSalary() );
        System.out.println("New base salary with 10 percent increase is " + emp.getBaseSalary() );
        employees[i] = emp;
      }
      System.out.println("Earning is " + employees[i].earnings());
    } //end for
  } 
}


