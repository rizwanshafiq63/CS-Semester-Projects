# Write a Python code to accept marks of a student from 1-100 and display the grade accordingly:
# Grade F if marks are less than 50 
# Grade E if marks are between 50 to 60 
# Grade D if marks are between 61 to 70 
# Grade C if marks are between 71 to 80 
# Grade B if marks are between 81 to 90 
# Grade A if marks are between 91 to 100

marks = int(input("Enter marks (0-100): "))

while marks > 100 or marks < 0:
    marks = int(input("Invalid Marks! Enter marks again (0-100): "))

if marks < 50:
    grade = "F"
elif marks <= 60:
    grade = "E"
elif marks <= 70:
    grade = "D"
elif marks <= 80:
    grade = "C"
elif marks <= 90:
    grade = "B"
elif marks <= 100:
    grade = "A"
else:
    grade = "Invalid Marks!"

print("Grade:", grade)
