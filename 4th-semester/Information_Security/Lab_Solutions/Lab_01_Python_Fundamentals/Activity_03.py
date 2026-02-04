# Write a Python code to accept an integer value from user and check that whether the given value is prime number or not.

isPrime = True
i = 2
n = int (input("Enter a number: "))
while i < n:
    remainder = n % i
    if remainder == 0:
        isPrime = False
        break
    else:
        i += 1
    
if isPrime:
    print(n, "is a Prime Number...")
else:
    print(n, "is NOT a Prime Number...")
