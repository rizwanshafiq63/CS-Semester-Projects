
class Employee { //Don't write public here bcz there can only be one public class in java file (Access Modifiers)
    int id; //Attribute 1
    String name; //Attribute 2
    private int salary;

    public void setInfo(int i, String n, int s){
        id = i;
        name = n;
        salary = s;
    }
    public void displayInfo(){
        System.out.println("Employee ID: " + id);
        System.out.println("Employee Name: " + name);
        System.out.println("Employee Salary: " + salary);
    }
    public void setSalary(int s2){
        salary = s2;
    }
    public int getSalary(){
        return salary;
    }

}

class CellPhone{
    public void ring(){
        System.out.println("Ringing...");
    }
    public void vibrate(){
        System.out.println("Vibrating...");
    }
    public void callFriend(){
        System.out.println("Calling Friend...");
    }
}

class Square{
    int side;
    public int area(){
        return (side*side);
    }
    public int perimeter(){
        return (4*side);
    }
}

class Student {
    private int id;
    private String name; //this help in data hiding..
    public void setId(int i){
        id = i;
    }
    public void setName (String n){
        //Benefit: you can put validation conditions here i.e if name starts with a number, it can't be a name...
        name = n;
    }
    public int getId(){
        return id;
    }
    public String getName(){
        return name;
    }
}


public class Lec01_CreatingClass {
    public static void main(String[] args) {
        Employee emp1 = new Employee(); //Instiationg a new Employee Object
        Employee emp2 = new Employee();

        //Setting Attributes emp1 = Method 1
        emp1.id = 1;
        emp1.name = "Rizwan";
        emp1.setSalary(1000); //since salary is kept pvt
        //Setting Attributes emp2 = Method 2
        emp2.setInfo(2,"Ali", 2000);


        // Printing Attributes 
        System.out.println(emp1.id); //Method 1
        System.out.println(emp1.name);
        emp1.displayInfo(); //Method 2
        emp2.displayInfo();

        //Example Problems
        CellPhone vivo = new CellPhone();
        vivo.callFriend();
        vivo.vibrate();
        vivo.ring();

        Square sq = new Square();
        sq.side = 3;
        System.out.println("Area of sq: " + sq.area());
        System.out.println("Perimeter of sq: "+sq.perimeter());

        //Access Modifiers, Getter and Setter
        Student s1 = new Student();
        // s1.id = 1; --> Throws an error due to private access modifier
        s1.setId(1);
        s1.setName("Hamza");
        System.out.println("S1 Name: " + s1.getName());



    }    
}
