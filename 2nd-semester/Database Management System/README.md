# Database Management System (DBMS)

Welcome to the **Database Management System (DBMS)** project! This Java-based program simulates the core functionalities of a database, enabling users to manage their data efficiently. The project models data in the form of tables and stores it in `.txt` files using the **CSV** format. Designed with a command-line interface, this DBMS allows users to interact with data using a case-insensitive query language.

---

## 🌟 Key Features

### 1. **Data Modeling**
- Tables are created with specified columns, stored in `.txt` files with a header row.
- Data is stored in CSV format, ensuring readability and compatibility.

### 2. **Command-Line Interface**
- Interactive prompt (`>>`) for user inputs.
- Case-insensitive commands for easy usage.

### 3. **Supported Operations**
The program supports a variety of database operations:

| **Operation**   | **Syntax**                                                                                           | **Description**                                                                                         |
|------------------|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| **CREATE**      | `CREATE table_name HAVING column1, column2, ...`                                                    | Creates a new table with the specified columns.                                                        |
| **DROP**        | `DROP table_name TABLE`                                                                             | Deletes the specified table after user confirmation.                                                   |
| **SHOW**        | `SHOW TABLES`                                                                                       | Lists all available tables.                                                                             |
| **INSERT**      | `INSERT INTO table_name VALUES ("value1", "value2", ...)`                                         | Adds a new row to the table, ensuring no duplicate rows.                                                |
| **SELECT**      | `SELECT FROM table_name WHERE column="value" ORDER BY column`                                      | Retrieves rows based on optional filtering and sorting criteria.                                        |
| **UPDATE**      | `UPDATE TABLE table_name SET column TO "new_value" HAVING column="condition_value"`              | Modifies rows that match the given condition.                                                          |
| **DELETE**      | `DELETE FROM TABLE table_name HAVING column="value"`                                              | Removes rows that match the given condition.                                                           |
| **HELP**        | `HELP`                                                                                              | Displays syntax and usage for all commands.                                                            |
| **EXIT**        | `EXIT`                                                                                              | Exits the program gracefully.                                                                          |

---

## 🛠️ How It Works

1. **Table Storage**
   - Tables are stored as `.txt` files in the `DBMS_TABLES/` directory.
   - The first line of each file contains the column headers.

2. **CSV Format**
   - Data rows are separated by commas, adhering to the CSV standard.
   - This ensures compatibility with external tools like Excel.

3. **Error Handling**
   - Comprehensive checks for invalid commands, table names, and duplicate entries.
   - Detailed error messages guide users.

4. **Example Workflow**
   ```
   >> CREATE students HAVING name, age, grade
   Table created successfully: students

   >> INSERT INTO students VALUES ("Alice", "20", "A")
   Row inserted successfully into table: students

   >> SELECT FROM students
   name       age       grade    
   ------------------------------
   Alice      20        A        

   >> DROP students TABLE
   Please confirm to delete the Table students. Enter y/n: y
   Successfully Deleted the Table: students
   ```

---

## 📂 Folder Structure

```
Database Management System/
│
├── DatabaseManagementSystem.java  # Main Java program
├── User Manual.docx               # Detailed user guide
├── Project Question Files/
│   ├── CSC103 - PF Lab Project.pdf  # Original project requirements
│   ├── PF Lab Project Groups.xlsx   # Group and syntax assignments
├── DBMS_TABLES/                   # Directory for storing generated table files
│   ├── students.txt                 # Example of a created table
```

---

## ⚙️ Technologies Used

- **Programming Language**: Java
- **File Storage**: CSV-based `.txt` files
- **IDE**: IntelliJ IDEA / Eclipse (recommended for Java projects)

---

## 📌 Highlights

- **Real-world Application**: Simulates core DBMS functionality, such as CRUD operations and query processing.
- **Error Handling**: Ensures data integrity and provides clear error messages for invalid inputs.
- **Modular Code**: Each database operation is implemented as a separate method for maintainability and scalability.
- **Syntax-Driven Design**: Adheres to specific syntax constraints, ensuring a structured user experience.

---

## 🌱 Key Learnings

- Practical application of Java concepts like file I/O, string manipulation, and exception handling.
- Development of a custom query language.
- Understanding database fundamentals such as tables, rows, columns, and data retrieval.

---

## 🚀 Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/rizwanshafiq63/semester-projects-repo/tree/main/2nd-semester
   ```

2. Navigate to the project directory and open `DatabaseManagementSystem.java` in your Java IDE.

3. Run the program and start entering commands at the prompt (`>>`).

4. Explore the `DBMS_TABLES/` folder to see the tables created and modified during execution.

---

## 💡 Future Enhancements

- Support for advanced query features like joins and nested queries.
- Integration with a graphical user interface (GUI) for better user experience.
- Enhanced data storage using relational database systems like MySQL.

---

Feel free to explore, test, and provide feedback on this project. Your suggestions are always welcome!

**Repository Link**: [DBMS Project Repository](https://github.com/rizwanshafiq63/semester-projects-repo/tree/main/2nd-semester/Database%20Management%20System)
