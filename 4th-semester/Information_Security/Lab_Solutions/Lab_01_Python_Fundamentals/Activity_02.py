# Write a Python code to keep accepting integer values from user until 0 is entered. 
# Display sum of the given values.

sum = 0
s = int (input("Enter an integer value: "))
while s != 0:
    sum += s
    s = int (input("Enter an integer value: "))
print("Sum of given values is", sum)
