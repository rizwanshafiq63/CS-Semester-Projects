/* The following activity explains the use of overriding for customizing the method of super class. The classes below include a CommisionEmployee class that has attributes of firstname, lastName, SSN, grossSales, CommisionRate. It has a constructor to initialize, set and get functions, and a function to display data members. The other class BasePlusCommisionEmployee is inherited from CommisionEmployee. It has additional attributes of Salary. It also has set and get functions and display function. The Earning method is overridden in this example. */

class commissionEmployee {
  protected String FirstName;
  protected String LastName;
  protected String SSN; 
  protected double grossSales; 
  protected double commonRate;

  public commissionEmployee() {
    FirstName = null;
    LastName = null;
    SSN = null;
    grossSales = 0.0;
    commonRate = 0.0;
  }
  public commissionEmployee (String a,String e,String b, double c, double d){
    FirstName = a;
    LastName = e; 
    SSN = b;
    grossSales = c; 
    commonRate = d;
  }

  public void setFN(String a) { FirstName=a;}
  public void setLN(String e) { LastName=e;}
  public void setSSN(String b) { SSN=b;}
  public void setGS(double c) { grossSales=c;}
  public void setCR(double d) { commonRate=d;}

  public String getFN() {return FirstName;}
  public String getSSN() {return SSN;}
  public double getGS() {return grossSales;}
  public double getCR() {return commonRate;}

  public double earnings(){
    return grossSales*commonRate;
  }

  public void display(){
    System.out.println("first name: "+FirstName+" last name: " +LastName+" SSN: "+SSN+" Gross Sale: "+grossSales+" and commonRate:"+commonRate);
  }
}

class BasePlusCommEmployee extends commissionEmployee {
  private double salary;
  BasePlusCommEmployee(){ salary = 0; }
  BasePlusCommEmployee(String A,String E,String B, double C, double D, double S) {
    super(A,E,B,C,D);
    salary=S;
  }

  //overridden method
  @Override
  public double earnings() {
    return super.earnings()+salary;
  }
  
  @Override
  public void display(){
    super.display();
    System.out.println("Salary : "+salary);
  }
}

public class Activity02 {
  public static void main(String args[]) {
    BasePlusCommEmployee b = new BasePlusCommEmployee("ali", "ahmed", "25-kkn", 100, 5.2, 25000);
    double earn = b.earnings();
    System.out.println("Earning of employee is " + earn);
  }
}

