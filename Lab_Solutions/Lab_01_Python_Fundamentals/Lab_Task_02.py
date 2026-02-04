# Write a program that reads a set of integers, and then prints the sum of the even and odd integers.

numbers = input("Enter integers separated by spaces: ")
numbers = [int(x) for x in numbers.split()]

even_sum = 0
odd_sum = 0

for n in numbers:
    if n % 2 == 0:
        even_sum += n
    else:
        odd_sum += n

print("Sum of even numbers:", even_sum)
print("Sum of odd numbers:", odd_sum)
