# Write a program that takes a number from user and calculate the factorial of that number.

num = int(input("Enter a number: "))
fact = 1

for i in range(1, num + 1):
    fact *= i

print("Factorial of", num, "is:", fact)
