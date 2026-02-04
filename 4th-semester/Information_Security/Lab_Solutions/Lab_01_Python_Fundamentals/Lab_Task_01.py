# Write a program that prompts the user to input an integer and then outputs the number with the digits reversed.
# For example, if the input is 12345, the output should be 54321.

n = int(input("Enter a number: "))

temp = n
rev = 0
while temp > 0:
    rev = rev * 10 + temp % 10
    temp //= 10
print(rev)
